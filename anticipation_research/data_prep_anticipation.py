"""
anticipation_research/data_prep_anticipation.py

Milestone 1 - Step 1: Build the FOG ANTICIPATION dataset.

Your original Stage-1 task asked: "is this window currently a freeze?"
This script builds windows that instead answer:

    "Given a 1.5s window of gait signal that ends `lead_time` seconds
     BEFORE a freeze starts, can we tell a freeze is coming?"

For lead_time = 0.0s the window ends exactly at the onset (upper bound,
easiest case). For lead_time = 3.0s the window ends a full 3 seconds
before the freeze (hardest, most clinically useful case, since it leaves
time for a cueing intervention).

KEY METHODOLOGICAL FIX vs. your original notebooks:
Your original DL.ipynb split data by CSV filename ("recording ID"), not
the true person. In tdcsfog, one person can have multiple recordings
(see tdcsfog_metadata.csv: Id -> Subject). Splitting by recording ID
risks the SAME PERSON appearing in both train and test, inflating your
reported F1. This script splits by the true `Subject` column instead.
Mention this explicitly in your paper's "Experimental Setup" section as
an improvement over a naive recording-level split.

Run:
    python anticipation_research/data_prep_anticipation.py

Requires (in your working directory):
    - tdcsfog.zip  (or an already-extracted tdcsfog_csvs/ folder — set
      FOG_DATA_DIR env var if it's named differently)
    - tdcsfog_metadata.csv  (already in your repo root)

Output:
    anticipation_outputs/anticipation_dataset.npz
    anticipation_outputs/dataset_summary.csv
    anticipation_outputs/split_subjects.json
"""

import os
import glob
import zipfile
import json

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from tqdm import tqdm

from config import (
    FS, WINDOW_SIZE, AXES, TRIGGER_COLS, LEAD_TIMES_S,
    NEG_STRIDE, NEG_MARGIN_S, NEG_MAX_RATIO,
    RANDOM_STATE, TEST_VAL_SIZE, VAL_OF_TEMP,
    DATA_DIR, ZIP_PATH, OUTPUT_DIR, DATASET_PATH,
)

METADATA_PATH = "../dataset/raw/tdcsfog_metadata.csv"   # already in your repo root


# ── Setup ────────────────────────────────────────────────────────────────

def ensure_data_dir():
    """Extract tdcsfog.zip into DATA_DIR if the CSVs aren't already there."""
    if os.path.isdir(DATA_DIR) and len(glob.glob(os.path.join(DATA_DIR, "*.csv"))) > 0:
        return
    if not os.path.exists(ZIP_PATH):
        raise FileNotFoundError(
            f"Neither '{DATA_DIR}' (extracted CSVs) nor '{ZIP_PATH}' (zip) were "
            f"found. Place tdcsfog.zip in the working directory, or set the "
            f"FOG_DATA_DIR environment variable to point at an already-extracted "
            f"folder of tdcsfog CSVs."
        )
    print(f"Extracting {ZIP_PATH} -> {DATA_DIR} ...")
    with zipfile.ZipFile(ZIP_PATH, "r") as zf:
        zf.extractall(DATA_DIR)


def load_subject_map():
    """Map recording Id -> true person Subject, using tdcsfog_metadata.csv."""
    if not os.path.exists(METADATA_PATH):
        print(f"WARNING: {METADATA_PATH} not found. Falling back to using the "
              f"recording filename as the subject ID (this reintroduces the "
              f"leakage risk described in this file's docstring).")
        return {}
    meta = pd.read_csv(METADATA_PATH)
    return dict(zip(meta["Id"], meta["Subject"]))


# ── Episode detection ────────────────────────────────────────────────────

def compute_fog_array(df):
    return (
        (df["StartHesitation"] == 1) |
        (df["Turn"]            == 1) |
        (df["Walking"]         == 1)
    ).astype(int).values


def find_fog_runs(fog_arr):
    """Contiguous runs of FOG==1. Returns list of (start_idx, end_idx)."""
    runs = []
    in_run = False
    start = 0
    for i, v in enumerate(fog_arr):
        if v == 1 and not in_run:
            start = i
            in_run = True
        elif v == 0 and in_run:
            runs.append((start, i))
            in_run = False
    if in_run:
        runs.append((start, len(fog_arr)))
    return runs


# ── Negative window pool ─────────────────────────────────────────────────

def get_negative_candidates(fog_arr, episodes, max_lead_samples, margin_samples):
    """
    Start indices of WINDOW_SIZE-length windows that are at least
    `margin_samples` away from any FOG episode AND at least
    (max_lead_samples + WINDOW_SIZE) before the next episode onset, so the
    same negative pool is valid for every lead time studied.
    """
    T = len(fog_arr)
    blocked = np.zeros(T, dtype=bool)
    for (s, e) in episodes:
        lo = max(0, s - max_lead_samples - WINDOW_SIZE - margin_samples)
        hi = min(T, e + margin_samples)
        blocked[lo:hi] = True

    candidates = []
    for start in range(0, T - WINDOW_SIZE, NEG_STRIDE):
        end = start + WINDOW_SIZE
        if not blocked[start:end].any():
            candidates.append(start)
    return candidates


# ── Positive (pre-onset) windows for one lead time ──────────────────────

def get_positive_starts(fog_arr, episodes, lead_samples):
    starts = []
    for (s, e) in episodes:
        end = s - lead_samples
        start = end - WINDOW_SIZE
        if start < 0:
            continue
        # The window itself must be FOG-free — a "clean" pre-onset window,
        # not accidentally overlapping this or an earlier episode.
        if fog_arr[start:end].any():
            continue
        starts.append(start)
    return starts


# ── Main extraction ──────────────────────────────────────────────────────

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    ensure_data_dir()
    subject_map = load_subject_map()

    csv_files = sorted(glob.glob(os.path.join(DATA_DIR, "*.csv")))
    if len(csv_files) == 0:
        raise RuntimeError(f"No CSV files found in {DATA_DIR}")
    print(f"Found {len(csv_files)} recordings in {DATA_DIR}")

    required_cols = set(AXES + TRIGGER_COLS)
    lead_samples_list = [int(round(L * FS)) for L in LEAD_TIMES_S]
    max_lead_samples = max(lead_samples_list)
    margin_samples = int(round(NEG_MARGIN_S * FS))

    # collectors[lead_time_s] = {"X": [...], "y": [...], "subj": [...]}
    collectors = {L: {"X": [], "y": [], "subj": []} for L in LEAD_TIMES_S}

    n_skipped_files = 0

    for path in tqdm(csv_files, desc="Extracting anticipation windows"):
        df = pd.read_csv(path)
        if not required_cols.issubset(df.columns):
            n_skipped_files += 1
            continue

        rec_id = os.path.basename(path).replace(".csv", "")
        subject = subject_map.get(rec_id, rec_id)   # true person if known, else fallback

        signals = df[AXES].values.astype(np.float32)
        fog_arr = compute_fog_array(df)
        episodes = find_fog_runs(fog_arr)

        if len(episodes) == 0:
            continue

        neg_candidates = get_negative_candidates(
            fog_arr, episodes, max_lead_samples, margin_samples
        )

        for L, lead_samples in zip(LEAD_TIMES_S, lead_samples_list):
            pos_starts = get_positive_starts(fog_arr, episodes, lead_samples)
            if len(pos_starts) == 0:
                continue

            n_neg_target = min(len(neg_candidates), max(1, int(len(pos_starts) * NEG_MAX_RATIO)))
            rng = np.random.RandomState(RANDOM_STATE + int(lead_samples))
            if len(neg_candidates) > 0:
                neg_idx = rng.choice(
                    len(neg_candidates),
                    size=min(n_neg_target, len(neg_candidates)),
                    replace=False,
                )
                neg_starts = [neg_candidates[i] for i in neg_idx]
            else:
                neg_starts = []

            for start in pos_starts:
                collectors[L]["X"].append(signals[start:start + WINDOW_SIZE])
                collectors[L]["y"].append(1)
                collectors[L]["subj"].append(subject)

            for start in neg_starts:
                collectors[L]["X"].append(signals[start:start + WINDOW_SIZE])
                collectors[L]["y"].append(0)
                collectors[L]["subj"].append(subject)

    if n_skipped_files:
        print(f"Skipped {n_skipped_files} files missing required columns.")

    # ── Subject-wise split (computed ONCE, shared across all lead times) ──
    all_subjects = sorted(set(
        s for L in LEAD_TIMES_S for s in collectors[L]["subj"]
    ))
    train_subj, temp_subj = train_test_split(
        all_subjects, test_size=TEST_VAL_SIZE, random_state=RANDOM_STATE
    )
    val_subj, test_subj = train_test_split(
        temp_subj, test_size=VAL_OF_TEMP, random_state=RANDOM_STATE
    )
    train_subj, val_subj, test_subj = set(train_subj), set(val_subj), set(test_subj)

    print(f"\nSubject-level split (true persons, not recordings):")
    print(f"  Train subjects: {len(train_subj)}")
    print(f"  Val   subjects: {len(val_subj)}")
    print(f"  Test  subjects: {len(test_subj)}")

    # ── Assemble arrays + save ─────────────────────────────────────────────
    npz_arrays = {}
    summary_rows = []

    for L in LEAD_TIMES_S:
        X = np.array(collectors[L]["X"], dtype=np.float32)
        y = np.array(collectors[L]["y"], dtype=np.int64)
        subj = np.array(collectors[L]["subj"], dtype="<U32")

        split = np.array(
            ["train" if s in train_subj else "val" if s in val_subj else "test"
             for s in subj],
            dtype="<U5",
        )

        key = f"{L:.1f}"
        npz_arrays[f"X_{key}"] = X
        npz_arrays[f"y_{key}"] = y
        npz_arrays[f"subj_{key}"] = subj
        npz_arrays[f"split_{key}"] = split

        for part in ["train", "val", "test"]:
            mask = split == part
            n_pos = int((y[mask] == 1).sum())
            n_neg = int((y[mask] == 0).sum())
            summary_rows.append({
                "lead_time_s": L, "split": part,
                "n_windows": int(mask.sum()), "n_pos": n_pos, "n_neg": n_neg,
            })

        print(f"Lead {L:>4.1f}s -> total windows: {len(y)}  "
              f"(pos={int((y == 1).sum())}, neg={int((y == 0).sum())})")

    np.savez_compressed(DATASET_PATH, **npz_arrays)
    summary_df = pd.DataFrame(summary_rows)
    summary_df.to_csv(os.path.join(OUTPUT_DIR, "dataset_summary.csv"), index=False)

    with open(os.path.join(OUTPUT_DIR, "split_subjects.json"), "w") as f:
        json.dump({
            "train": sorted(train_subj),
            "val": sorted(val_subj),
            "test": sorted(test_subj),
        }, f, indent=2)

    print(f"\nSaved dataset  -> {DATASET_PATH}")
    print(f"Saved summary  -> {OUTPUT_DIR}/dataset_summary.csv")
    print(f"Saved split    -> {OUTPUT_DIR}/split_subjects.json")


if __name__ == "__main__":
    main()