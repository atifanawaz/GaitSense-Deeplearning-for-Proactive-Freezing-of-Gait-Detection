# Milestone 1: FOG Anticipation Pipeline

Converts your Stage-1 FOG **detection** system into a genuine FOG
**anticipation** study: predicting a freeze *before* it starts, at several
lead times, and reporting how detection performance changes as lead time
increases. This is the "lead-time vs. accuracy curve" that makes the
"Proactive" part of your project title actually true, and it's the
centerpiece figure/table for your paper's Results section.

## Files

| File | Purpose |
|---|---|
| `config.py` | All signal/window/training parameters in one place. |
| `data_prep_anticipation.py` | Builds the anticipation dataset from tdcsfog CSVs, with a **true subject-level split** (fixes a leakage risk present in the original notebooks). |
| `models.py` | `AnticipationModel` — same CNN+BiLSTM backbone as your Stage-1 `FoGModel`, so results isolate the effect of the *task*, not the architecture. |
| `utils.py` | Reproducibility seeding, early stopping, bootstrap confidence intervals. |
| `train_anticipation.py` | Trains one model per lead time, picks the operating threshold on validation data only, evaluates on the held-out test set. |
| `evaluate_anticipation.py` | Adds 95% bootstrap CIs and produces the paper-ready figure + markdown table. |

## Nothing else in your repo changes

This milestone is purely additive — it does not modify `DL.ipynb`,
`FogEventDL.ipynb`, `Medication_Final.ipynb`, `clinical_portal/backend/*`, or
any existing `.pth` file. Your working clinician portal and Stage-1/Stage-2
models are untouched. Integrating the anticipation model into the portal
is a later milestone, once this one is validated.

## Run order

```
python anticipation_research/data_prep_anticipation.py
python anticipation_research/train_anticipation.py
python anticipation_research/evaluate_anticipation.py
```

See the accompanying chat message for exact setup steps, expected console
output, runtime estimates, and how each output file maps into the paper.