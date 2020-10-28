# Hacky way to allow for importing from parent folders
from sys import path
path.append('..')

from .moods.moods import raw_moods, moods
from config.config import config
import random

class Memory:
    def __init__(self):
        self.current_mood = moods[config.props['drone']['init_mood']]
        self.lost_cnt = 0
    
    def get_mood(self):
        return self.current_mood
    
    def set_mood(self, mood_name):
        self.current_mood = moods[mood_name]

    def select_random_mood(self):
        # Select random mood excluding the last mood, which is the 'confused' mood, which is only used when the drone is lost.
        id = random.randint(0, len(moods) - 1)
        self.set_mood(raw_moods[id].name)

    def found(self):
        self.lost_cnt = 0
        self.select_random_mood

    def lost(self):
        self.lost_cnt += 1

        if self.lost_cnt > config.props['drone']['lost_frame_cnt']:
            self.current_mood = moods['confused']
    
    def behave(self):
        return self.current_mood.get_move()

memory = Memory()