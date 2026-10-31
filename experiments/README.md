# Experiments

These notebooks document preprocessing, analysis, model training, and trigger prediction. They are research notebooks and are not run by the clinical portal.

## Notebook folders

- `data_preprocessing/`: `defog_preprocessing.ipynb` prepares DeFOG data; `tdcsfog_preprocessing.ipynb` and `tdcsfog_preprocessing_workflow.ipynb` prepare tDCS FOG data.
- `exploratory_analysis/`: `medication_analysis.ipynb` studies medication-related data; `explainable_ai_analysis.ipynb` explores model explanations.
- `model_training/`: `classical_machine_learning.ipynb` trains classical baselines; `deep_learning_fog_detection.ipynb` trains FoG detection; `fog_event_classification.ipynb` classifies FoG events; `machine_learning_feature_extraction_stage2.ipynb` performs stage-two feature extraction.
- `trigger_prediction/`: `trigger_classification.ipynb` trains and evaluates trigger classification.

## External data paths

The notebooks expect data outside this repository, including `tdcsfog.zip`, extracted `tdcsfog_csvs/` or `tdcsfog_data/`, `tlvmc-parkinsons-freezing-gait-prediction/train/defog/`, and `tlvmc-parkinsons-freezing-gait-prediction/defog_metadata.csv`. Some notebooks also reference a local Downloads folder and a Google Colab path. These paths are documented from the notebooks and are not changed here.

Raw data is not included in this repository.
