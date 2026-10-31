"""
anticipation_research/config.py

Central configuration for the FOG Anticipation research pipeline (Milestone 1).

This file is the single source of truth for signal parameters, paths, and
experiment settings used by:
    - data_prep_anticipation.py
    - train_anticipation.py
    - evaluate_anticipation.py

Keeping these values in one place means every script (and your paper's
methods section) references the exact same numbers.
"""

import os

# ── Signal parameters (match original Stage 1 pipeline) ────────────────────
FS           = 128     # Hz, tdcsfog sampling rate
WINDOW_SIZE  = 192     # samples = 1.5 s, same window length as Stage 1 detector
AXES         = ["AccV", "AccML", "AccAP"]
TRIGGER_COLS = ["StartHesitation", "Turn", "Walking"]

# ── Lead times studied (seconds before FOG onset) ───────────────────────────
# 0.0 s = window ends exactly at onset (upper bound / most reactive case)
# 3.0 s = window ends 3s before onset (hardest, most clinically useful case)
LEAD_TIMES_S = [0.0, 0.5, 1.0, 1.5, 2.0, 3.0]

# ── Negative-window sampling ─────────────────────────────────────────────────
NEG_STRIDE    = 64     # samples between candidate negative windows (0.5s)
NEG_MARGIN_S  = 1.0    # seconds of buffer kept clear around every FOG episode
NEG_MAX_RATIO = 3.0    # cap negatives at this multiple of positives per subject

# ── Reproducibility ──────────────────────────────────────────────────────────
RANDOM_STATE = 42      # identical to your original DL.ipynb split

# ── Subject-wise split ratios (identical proportions to original notebooks) ─
TEST_VAL_SIZE = 0.30   # 30% held out from train
VAL_OF_TEMP   = 0.50   # split that 30% into 15% val / 15% test

# ── Paths ─────────────────────────────────────────────────────────────────
# Directory that contains the extracted tdcsfog per-subject CSVs
# (same folder your original notebooks call "tdcsfog_csvs")
DATA_DIR = os.environ.get("FOG_DATA_DIR", "tdcsfog_csvs")
ZIP_PATH = os.environ.get("FOG_ZIP_PATH", "tdcsfog.zip")

OUTPUT_DIR   = "anticipation_outputs"
DATASET_PATH = os.path.join(OUTPUT_DIR, "anticipation_dataset.npz")

# ── Training hyperparameters ─────────────────────────────────────────────────
BATCH_SIZE           = 64
EPOCHS                = 40
LR                    = 1e-3
WEIGHT_DECAY          = 1e-4
EARLY_STOP_PATIENCE   = 10
EARLY_STOP_MIN_DELTA  = 0.002

N_BOOTSTRAP = 1000   # bootstrap resamples for confidence intervals