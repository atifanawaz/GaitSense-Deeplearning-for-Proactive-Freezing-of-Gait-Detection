"""
anticipation_research/evaluate_anticipation.py

Milestone 1 - Step 3: Add bootstrap confidence intervals to the results
table, and produce the headline "lead-time vs. performance" figure for
the paper.

Requires: outputs of train_anticipation.py
          (anticipation_outputs/results_summary.csv,
           anticipation_outputs/predictions_lead_*.npz)

Run:
    python anticipation_research/evaluate_anticipation.py

Output:
    anticipation_outputs/results_summary_with_ci.csv
    anticipation_outputs/lead_time_vs_performance.png   <- paper figure
    anticipation_outputs/results_table.md                <- paper table
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from config import OUTPUT_DIR, N_BOOTSTRAP, RANDOM_STATE
from utils import bootstrap_ci


def main():
    summary_path = os.path.join(OUTPUT_DIR, "results_summary.csv")
    if not os.path.exists(summary_path):
        raise FileNotFoundError(f"{summary_path} not found. Run train_anticipation.py first.")

    df = pd.read_csv(summary_path)

    ci_rows = []
    for _, row in df.iterrows():
        tag = str(row["lead_time_s"]).replace(".", "_")
        pred_path = os.path.join(OUTPUT_DIR, f"predictions_lead_{tag}s.npz")
        if not os.path.exists(pred_path):
            print(f"WARNING: missing predictions for lead={row['lead_time_s']}, skipping CI.")
            ci_rows.append({})
            continue

        preds = np.load(pred_path)
        ci = bootstrap_ci(
            preds["labels"], preds["probs"], float(preds["threshold"]),
            n_bootstrap=N_BOOTSTRAP, seed=RANDOM_STATE,
        )
        ci_rows.append(ci)

    ci_df = pd.DataFrame(ci_rows)
    full_df = pd.concat([df.reset_index(drop=True), ci_df.reset_index(drop=True)], axis=1)

    out_csv = os.path.join(OUTPUT_DIR, "results_summary_with_ci.csv")
    full_df.to_csv(out_csv, index=False)
    print(f"Saved -> {out_csv}")
    print(full_df.to_string(index=False))

    # ── Headline figure: lead time vs. F1 and AUPRC, with bootstrap CIs ────
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))

    x = full_df["lead_time_s"].values

    f1 = full_df["f1"].values
    f1_err_lo = f1 - full_df["f1_ci_lo"].values
    f1_err_hi = full_df["f1_ci_hi"].values - f1
    axes[0].errorbar(x, f1, yerr=[f1_err_lo, f1_err_hi], fmt="o-",
                      color="#e63946", capsize=4, linewidth=2)
    axes[0].set_xlabel("Lead time before FOG onset (s)")
    axes[0].set_ylabel("F1 score")
    axes[0].set_title("Anticipation F1 vs. lead time")
    axes[0].grid(True, alpha=0.3)
    axes[0].set_ylim(0, 1.05)

    auprc = full_df["auprc"].values
    ap_err_lo = auprc - full_df["auprc_ci_lo"].values
    ap_err_hi = full_df["auprc_ci_hi"].values - auprc
    axes[1].errorbar(x, auprc, yerr=[ap_err_lo, ap_err_hi], fmt="o-",
                      color="#457b9d", capsize=4, linewidth=2)
    axes[1].set_xlabel("Lead time before FOG onset (s)")
    axes[1].set_ylabel("AUPRC")
    axes[1].set_title("Anticipation AUPRC vs. lead time")
    axes[1].grid(True, alpha=0.3)
    axes[1].set_ylim(0, 1.05)

    plt.suptitle("FOG Anticipation Performance vs. Lead Time (95% bootstrap CI)",
                 fontsize=12, fontweight="bold")
    plt.tight_layout()
    fig_path = os.path.join(OUTPUT_DIR, "lead_time_vs_performance.png")
    plt.savefig(fig_path, dpi=150, bbox_inches="tight")
    plt.show()
    print(f"Saved figure -> {fig_path}")

    # ── Markdown table for the paper ────────────────────────────────────────
    md_cols = ["lead_time_s", "n_test_pos", "n_test_neg", "precision",
               "recall", "f1", "f1_ci_lo", "f1_ci_hi", "auprc",
               "auprc_ci_lo", "auprc_ci_hi", "roc_auc"]
    md_df = full_df[md_cols].copy()
    for c in md_df.columns:
        if md_df[c].dtype == float:
            md_df[c] = md_df[c].round(3)

    md_path = os.path.join(OUTPUT_DIR, "results_table.md")
    with open(md_path, "w") as f:
        f.write(md_df.to_markdown(index=False))
    print(f"Saved paper-ready table -> {md_path}")


if __name__ == "__main__":
    main()