# Hacky way to allow for importing from parent folders
from sys import path
path.append('..')

from .moods.moods import raw_moods, moods
from config.config import config
import random
import time

class Memory:
    def __init__(self):
        self.current_mood = moods[config.props['drone']['init_mood']]
        self.lost_state = 0, False
    
    def get_mood(self):
        return self.current_mood.name
    
    def set_mood(self, mood_name):
        self.current_mood = moods[mood_name]

    def select_random_mood(self):
        # Select random mood excluding the last mood, which is the 'confused' mood, which is only used when the drone is lost.
        id = random.randint(0, len(moods) - 1)
        self.set_mood(raw_moods[id].name)
        # self.set_mood('sad')

    def found(self):
        if self.lost_state[1]:
            # Found itself again
            self.lost_state = 0, False
            self.select_random_mood()
            self.apply_new_mood()
    
    def apply_new_mood(self):
        mood = self.get_mood()

        # Ensure that the drone is flying
        if not config.drone_flying:
            config.drone_takeoff()

        if mood == 'happy':
            config.drone.set_speed(100)
            config.drone.flip_back()
        elif mood == 'sad':
            config.drone.set_speed(10)
            if random.random() < 0.5:
                config.drone.flip_left()
                config.drone_emergency_stop()
                time.sleep(7)
                config.drone_takeoff()
        elif mood == 'no_mood':
            config.drone.set_speed(50)

    def lost(self):
        self.lost_state = self.lost_state[0] + 1, self.lost_state[1]

        # If the drone was not already lost and the # of frames in which no object has been found has exceeded the threshold 
        if not self.lost_state[1] and self.lost_state[0] > config.props['drone']['lost_frame_cnt']:
            self.lost_state = self.lost_state[0], True
            self.current_mood = moods['confused']
    
    def behave(self):
        return self.current_mood.get_move()

memory = Memory()