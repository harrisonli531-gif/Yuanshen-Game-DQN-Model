from collections import deque
import random
import math

class replay_buffer:

    def __init__(self, capacity: int):
        self.buffer = deque(maxlen=capacity)

    def push(self, prev_state, reward, card_played, next_state, next_hand, done):
        experience = (prev_state, reward, card_played, next_state, next_hand, done)
        self.buffer.append(experience)

    def sample(self, batch_size):
        # Sample returns a list of experiences.
        return random.sample(self.buffer, min(batch_size, len(self.buffer)))
    
    def print(self):
        for experience in self.buffer:
            print(experience)

    def __len__(self):
        return len(self.buffer)
    