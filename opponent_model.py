import torch
import torch.nn as nn

class opponent_model(nn.Module):
    '''The model uses 6 attributes to predict the outcome: life, opponent life, turn number, previous played card (or -1 for turn 1), current power bonus, current damage bonus'''

    def __init__(self, n):
        '''n must equal the number of unique cards in the deck, so the model generates one Q value 
        for each possible card it can choose to play'''
        super(opponent_model, self).__init__()
        self.layers = nn.Sequential(
            nn.Linear(6, 30),
            nn.ReLU(),
            nn.Linear(30, 15),
            nn.ReLU(),
            nn.Linear(15, n),
        )

    def forward(self, x):
        x = self.layers(x)
        return x

