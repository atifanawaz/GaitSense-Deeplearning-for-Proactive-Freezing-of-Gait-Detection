"""
anticipation_research/models.py

Model architecture for the FOG Anticipation study (Milestone 1).

AnticipationModel uses the same CNN + BiLSTM backbone as your original
Stage-1 FoGModel (dl_fog_model_best.pth), so any accuracy differences you
observe across lead times are attributable to the TASK (anticipation
horizon), not to a different architecture. This keeps the ablation clean
for the paper: "same backbone, harder task."
"""

import torch.nn as nn


class AnticipationModel(nn.Module):
    """
    Binary classifier: given a 1.5s (192-sample) 3-axis accelerometer window
    ending `lead_time` seconds before a FOG onset (or a matched non-FOG
    control window), predict whether a freeze is about to occur.

    Input : x (B, 192, 3)
    Output: logits (B, 1)  -- apply sigmoid for probability
    """

    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv1d(3, 32, kernel_size=5, padding=2)
        self.bn1 = nn.BatchNorm1d(32)
        self.conv2 = nn.Conv1d(32, 64, kernel_size=5, padding=2)
        self.bn2 = nn.BatchNorm1d(64)
        self.relu = nn.ReLU()
        self.pool = nn.MaxPool1d(2)
        self.drop = nn.Dropout(0.3)

        self.lstm = nn.LSTM(
            input_size=64, hidden_size=64,
            num_layers=2, batch_first=True,
            bidirectional=True, dropout=0.3
        )
        self.fc = nn.Linear(128, 1)

    def forward(self, x):
        x = x.permute(0, 2, 1)                # (B, 3, 192)
        x = self.relu(self.bn1(self.conv1(x)))
        x = self.pool(x)                      # (B, 32, 96)
        x = self.relu(self.bn2(self.conv2(x)))
        x = self.pool(x)                      # (B, 64, 48)
        x = self.drop(x)
        x = x.permute(0, 2, 1)                # (B, 48, 64)
        x, _ = self.lstm(x)                   # (B, 48, 128)
        x = x.mean(dim=1)                     # (B, 128)
        return self.fc(x)                     # (B, 1)