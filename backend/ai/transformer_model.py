import torch
import torch.nn as nn

class MarketTransformer(nn.Module):

    def __init__(self, input_dim=8, d_model=32, nhead=4, layers=2):
        super().__init__()

        self.embedding = nn.Linear(input_dim, d_model)

        self.transformer = nn.Transformer(
            d_model=d_model,
            nhead=nhead,
            num_encoder_layers=layers
        )

        self.fc = nn.Linear(d_model, 1)

    def forward(self, x):

        x = self.embedding(x)
        x = self.transformer(x, x)
        x = self.fc(x[-1])

        return x
