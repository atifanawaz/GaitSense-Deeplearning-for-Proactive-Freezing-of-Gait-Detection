"""
anticipation_research/train_anticipation.py

Milestone 1 - Step 2: Train one AnticipationModel per lead time and
evaluate on the held-out (subject-independent) test set.

Requires: anticipation_outputs/anticipation_dataset.npz
          (produced by data_prep_anticipation.py)

Run:
    python anticipation_research/train_anticipation.py

Output (per lead time L, e.g. L=1.5):
    anticipation_outputs/model_lead_1_5s.pth
    anticipation_outputs/predictions_lead_1_5s.npz    (test probs + labels)
    anticipation_outputs/training_history_lead_1_5s.json

Also produces the master table:
    anticipation_outputs/results_summary.csv
"""

import os
import json

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from sklearn.metrics import (
    precision_recall_curve, precision_recall_fscore_support,
    average_precision_score, roc_auc_score,
)

from config import (
    LEAD_TIMES_S, DATASET_PATH, OUTPUT_DIR,
    BATCH_SIZE, EPOCHS, LR, WEIGHT_DECAY,
    EARLY_STOP_PATIENCE, EARLY_STOP_MIN_DELTA, RANDOM_STATE,
)
from models import AnticipationModel
from utils import set_seed, EarlyStopping


class WindowDataset(Dataset):
    """Per-channel z-score normalisation applied per window, identical
    convention to your original Stage-1 FoGDataset."""

    def __init__(self, X, y):
        self.X = torch.tensor(X, dtype=torch.float32)
        self.y = torch.tensor(y, dtype=torch.float32).view(-1, 1)

    def __len__(self):
        return len(self.y)

    def __getitem__(self, idx):
        x = self.X[idx]
        mean = x.mean(dim=0, keepdim=True)
        std = x.std(dim=0, keepdim=True) + 1e-8
        x = (x - mean) / std
        return x, self.y[idx]


def best_threshold_from_val(y_val, probs_val):
    if len(np.unique(y_val)) < 2:
        return 0.5
    precision, recall, thresholds = precision_recall_curve(y_val, probs_val)
    f1s = 2 * precision * recall / (precision + recall + 1e-12)
    if len(thresholds) == 0:
        return 0.5
    best_idx = int(np.argmax(f1s[:-1])) if len(f1s) > 1 else 0
    return float(thresholds[best_idx])


def run_epoch_train(model, loader, optimizer, criterion, device):
    model.train()
    total_loss = 0.0
    for Xb, yb in loader:
        Xb, yb = Xb.to(device), yb.to(device)
        optimizer.zero_grad()
        logits = model(Xb)
        loss = criterion(logits, yb)
        loss.backward()
        nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        optimizer.step()
        total_loss += loss.item()
    return total_loss / max(1, len(loader))


def run_epoch_eval(model, loader, device):
    model.eval()
    probs, labels = [], []
    with torch.no_grad():
        for Xb, yb in loader:
            Xb = Xb.to(device)
            p = torch.sigmoid(model(Xb)).cpu().numpy().flatten()
            probs.extend(p)
            labels.extend(yb.numpy().flatten())
    return np.array(probs), np.array(labels)


def train_one_lead_time(L, data, device):
    key = f"{L:.1f}"
    X, y, split = data[f"X_{key}"], data[f"y_{key}"], data[f"split_{key}"]

    X_train, y_train = X[split == "train"], y[split == "train"]
    X_val, y_val = X[split == "val"], y[split == "val"]
    X_test, y_test = X[split == "test"], y[split == "test"]

    print(f"\n{'=' * 60}\nLead time {L:.1f}s | "
          f"train={len(y_train)} (pos={int(y_train.sum())})  "
          f"val={len(y_val)} (pos={int(y_val.sum())})  "
          f"test={len(y_test)} (pos={int(y_test.sum())})\n{'=' * 60}")

    if len(y_train) < 20 or len(np.unique(y_train)) < 2:
        print(f"SKIPPING lead={L}s: not enough training data / only one class present.")
        return None

    train_loader = DataLoader(WindowDataset(X_train, y_train), batch_size=BATCH_SIZE, shuffle=True)
    val_loader = DataLoader(WindowDataset(X_val, y_val), batch_size=BATCH_SIZE, shuffle=False)
    test_loader = DataLoader(WindowDataset(X_test, y_test), batch_size=BATCH_SIZE, shuffle=False)

    model = AnticipationModel().to(device)

    n_pos, n_neg = (y_train == 1).sum(), (y_train == 0).sum()
    pos_weight = torch.tensor([n_neg / max(1, n_pos)], dtype=torch.float32).to(device)
    criterion = nn.BCEWithLogitsLoss(pos_weight=pos_weight)
    optimizer = optim.Adam(model.parameters(), lr=LR, weight_decay=WEIGHT_DECAY)
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode="max", factor=0.5, patience=5)

    early_stopper = EarlyStopping(patience=EARLY_STOP_PATIENCE, min_delta=EARLY_STOP_MIN_DELTA)
    history = {"train_loss": [], "val_f1": []}

    for epoch in range(1, EPOCHS + 1):
        train_loss = run_epoch_train(model, train_loader, optimizer, criterion, device)
        val_probs, val_labels = run_epoch_eval(model, val_loader, device)

        val_preds = (val_probs > 0.5).astype(int)
        _, _, val_f1, _ = precision_recall_fscore_support(
            val_labels, val_preds, average="binary", zero_division=0
        )

        scheduler.step(val_f1)
        history["train_loss"].append(train_loss)
        history["val_f1"].append(float(val_f1))

        print(f"Epoch {epoch:02d}/{EPOCHS} | Loss: {train_loss:.4f} | Val F1: {val_f1:.4f}")

        early_stopper.step(val_f1, model)
        if early_stopper.stop:
            print(f"Early stopping at epoch {epoch}.")
            break

    model.load_state_dict(early_stopper.best_state)
    model.to(device)

    # Pick the operating threshold on VAL data only (never touch test for this).
    val_probs, val_labels = run_epoch_eval(model, val_loader, device)
    threshold = best_threshold_from_val(val_labels, val_probs)

    test_probs, test_labels = run_epoch_eval(model, test_loader, device)
    test_preds = (test_probs >= threshold).astype(int)

    precision, recall, f1, _ = precision_recall_fscore_support(
        test_labels, test_preds, average="binary", zero_division=0
    )
    auprc = average_precision_score(test_labels, test_probs) if len(np.unique(test_labels)) > 1 else float("nan")
    roc_auc = roc_auc_score(test_labels, test_probs) if len(np.unique(test_labels)) > 1 else float("nan")

    tag = str(L).replace(".", "_")
    torch.save(model.state_dict(), os.path.join(OUTPUT_DIR, f"model_lead_{tag}s.pth"))
    np.savez(
        os.path.join(OUTPUT_DIR, f"predictions_lead_{tag}s.npz"),
        probs=test_probs, labels=test_labels, threshold=threshold,
    )
    with open(os.path.join(OUTPUT_DIR, f"training_history_lead_{tag}s.json"), "w") as f:
        json.dump(history, f, indent=2)

    print(f"Lead {L:.1f}s TEST -> Precision: {precision:.3f}  Recall: {recall:.3f}  "
          f"F1: {f1:.3f}  AUPRC: {auprc:.3f}  ROC-AUC: {roc_auc:.3f}  (threshold={threshold:.3f})")

    return {
        "lead_time_s": L,
        "n_train": len(y_train), "n_val": len(y_val), "n_test": len(y_test),
        "n_test_pos": int(y_test.sum()), "n_test_neg": int((y_test == 0).sum()),
        "threshold": threshold,
        "precision": precision, "recall": recall, "f1": f1,
        "auprc": auprc, "roc_auc": roc_auc,
    }


def main():
    set_seed(RANDOM_STATE)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device: {device}")

    if not os.path.exists(DATASET_PATH):
        raise FileNotFoundError(
            f"{DATASET_PATH} not found. Run data_prep_anticipation.py first."
        )

    data = np.load(DATASET_PATH, allow_pickle=False)

    results = []
    for L in LEAD_TIMES_S:
        r = train_one_lead_time(L, data, device)
        if r is not None:
            results.append(r)

    results_df = pd.DataFrame(results)
    out_path = os.path.join(OUTPUT_DIR, "results_summary.csv")
    results_df.to_csv(out_path, index=False)
    print(f"\nSaved results summary -> {out_path}")
    print(results_df.to_string(index=False))


if __name__ == "__main__":
    main()