"""
anticipation_research/utils.py

Shared helpers for the FOG Anticipation study: reproducibility, early
stopping, and bootstrap confidence intervals. Used by both
train_anticipation.py and evaluate_anticipation.py so the methodology is
identical everywhere it's applied (and in your paper's reported numbers).
"""

import random
import numpy as np
import torch
from sklearn.metrics import f1_score, average_precision_score


def set_seed(seed):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


class EarlyStopping:
    """Same early-stopping logic used in your original FogEventDL.ipynb
    trigger classifier, kept consistent across the project."""

    def __init__(self, patience=10, min_delta=0.002, verbose=True):
        self.patience = patience
        self.min_delta = min_delta
        self.verbose = verbose
        self.counter = 0
        self.best_score = None
        self.best_state = None
        self.stop = False

    def step(self, score, model):
        if self.best_score is None or score > self.best_score + self.min_delta:
            self.best_score = score
            self.best_state = {k: v.cpu().clone() for k, v in model.state_dict().items()}
            self.counter = 0
            if self.verbose:
                print(f"  New best: {score:.4f}")
        else:
            self.counter += 1
            if self.verbose:
                print(f"  No improvement ({self.counter}/{self.patience})  best={self.best_score:.4f}")
            if self.counter >= self.patience:
                self.stop = True


def bootstrap_ci(y_true, y_prob, threshold, n_bootstrap=1000, seed=42, alpha=0.05):
    """
    Bootstrap 95% CI for F1 (at the given threshold) and AUPRC, resampling
    the test set with replacement. Returns a dict of CIs.
    """
    rng = np.random.RandomState(seed)
    y_true = np.asarray(y_true)
    y_prob = np.asarray(y_prob)
    n = len(y_true)

    f1_samples, auprc_samples = [], []
    for _ in range(n_bootstrap):
        idx = rng.randint(0, n, size=n)
        yt, yp = y_true[idx], y_prob[idx]
        if len(np.unique(yt)) < 2:
            continue
        preds = (yp >= threshold).astype(int)
        f1_samples.append(f1_score(yt, preds, zero_division=0))
        auprc_samples.append(average_precision_score(yt, yp))

    def ci(samples):
        if len(samples) == 0:
            return (float("nan"), float("nan"))
        lo = float(np.percentile(samples, 100 * alpha / 2))
        hi = float(np.percentile(samples, 100 * (1 - alpha / 2)))
        return lo, hi

    f1_lo, f1_hi = ci(f1_samples)
    ap_lo, ap_hi = ci(auprc_samples)

    return {
        "f1_ci_lo": f1_lo, "f1_ci_hi": f1_hi,
        "auprc_ci_lo": ap_lo, "auprc_ci_hi": ap_hi,
        "n_bootstrap_valid": len(f1_samples),
    }