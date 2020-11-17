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
        # Start out not having found your friend
        self.lost_state = config.props['drone']['lost_frame_cnt'] + 1, True
    
    def get_mood(self):
        return self.current_mood.name
    
    def set_mood(self, mood_name):
        self.current_mood = moods[mood_name]

    def select_random_mood(self):
        # Select random mood excluding the last mood, which is the 'confused' mood, which is only used when the drone is lost.
        id = random.randint(0, len(raw_moods) - 2)
        self.set_mood(raw_moods[id].name)
        # self.set_mood("sad")
        self.current_mood.reapply()
        # self.set_mood('sad')

    def found(self):
        if self.lost_state[1]:
            # Just take off in case it broke down before
            if config.use_drone and not config.drone_flying:
                config.drone_takeoff()
                config.drone.move_down(30)

            # Found itself again
            self.lost_state = 0, False
            self.select_random_mood()
    
    def lost(self):
        self.lost_state = self.lost_state[0] + 1, self.lost_state[1]

        # If the drone was not already lost and the # of frames in which no object has been found has exceeded the threshold 
        if not self.lost_state[1] and self.lost_state[0] > config.props['drone']['lost_frame_cnt']:
            self.lost_state = config.props['drone']['lost_frame_cnt'] + 1, True
            self.set_mood('confused')
    
    def behave(self):
        if config.use_drone and config.drone_flying:
            config.drone_takeoff()
            config.drone.move_up(30)

        self.current_mood.do_behavior()
        return self.current_mood.get_move()

memory = Memory()