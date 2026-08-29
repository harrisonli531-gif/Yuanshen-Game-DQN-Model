from collections import deque
import random
import math

class replay_buffer:

    def __init__(self, capacity: int):
        self.buffer = deque(maxlen=capacity)

    def push(self, prev_state, reward, card_played, next_state, next_hand, done):
        experience = (prev_state, reward, card_played, next_state, next_hand, done)
        self.buffer.append(experience)

    def sample(self, batch_percent):
        batch_size = math.floor(len(self.buffer) * batch_percent)

        #sample returns as a list of experiences
        return random.sample(self.buffer, batch_size)
    def print(self):
        for experience in self.buffer:
            print(experience)
    