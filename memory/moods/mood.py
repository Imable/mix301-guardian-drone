from sys import path
path.append('..')

import time
import random
from config.config import config

class Mood:
    def __init__(self, name, drone_behavior, start_drone_behavior, animation_matrices, start_animation_matrices=[], loop=True):
        '''
        drone_behavior = (function to execute, seconds after which behavior chance is 100%)
        '''
        self.name = name
        self.loop = loop

        '''
        s = delay in seconds (since last movement)
        [
            (s, [x, y, z, r]),
            (s, [x, y, z, r])
        ]
        '''
        self.start_drone_behavior = start_drone_behavior
        self.drone_behavior = drone_behavior
        self.set_matrices(animation_matrices, start_animation_matrices)
        self.reset()
      
    def set_matrices(self, animation_matrices, start_animation_matrices):
        # Figure out if we first need to start with the start_animation_matrices
        self.starting = start_animation_matrices or False

        # If there are starting matrices
        if self.starting:
            self.animation_matrices = start_animation_matrices
            self.next_matrices = animation_matrices
        else:
            self.animation_matrices = animation_matrices

    def reapply(self):
        self.reset()

        if config.use_drone:
            self.start_drone_behavior()
        else:
            print(f'Doing {self.start_drone_behavior.__name__}.')

    def reset(self):
        self.stop = False
        self.last_move = self.get_now()
        # self.current_animation = index, (delay, animation_matrix)
        self.current_animation = self.get_initial_animation()
        # Last time we executed the random move
        self.last_drone_behavior = self.get_now()
        # self.ran_start_behavior = False
    
    def get_now(self):
        return time.time()

    def get_cur_delay(self):
        return self.current_animation[1][0]
    
    def get_cur_animation_matrix(self):
        return self.current_animation[1][1]

    def get_initial_animation(self):
        return 0, self.animation_matrices[0]

    def is_last_animation(self):
        return self.current_animation[0] == len(self.animation_matrices) - 1
    
    def get_behavior_chance(self):
        diff = self.get_now() - self.last_drone_behavior
        return 1/(self.drone_behavior[1]/diff)

    def do_behavior(self):
        rnd = random.random()
        chc = self.get_behavior_chance()
        
        if not self.stop and rnd < chc:
            if config.use_drone:
                self.drone_behavior[0]()
            else:
                print(f'Doing {self.drone_behavior[0].__name__}.')
            self.last_drone_behavior = self.get_now()

    def move_next(self):
        '''
        Move the internal animation state to the next animation.
        '''

        self.last_move = self.get_now()

        # Move to the next animation if we haven't reached the end of the animation sequence yet
        if not self.is_last_animation():
            index = self.current_animation[0] + 1
            self.current_animation = index, self.animation_matrices[index]

        elif self.starting:
            self.animation_matrices = self.next_matrices

            # Move out of the starting state
            self.starting = False

        # Go back to the beginning if it is a looping animation
        elif self.loop:
            self.current_animation = self.get_initial_animation()
            
        # Stop this animation if it is not a looping animation
        else:
            self.stop = True
    
    def get_move(self):
        move = [0, 0, 0, 0]

        # if not self.ran_start_behavior and config.drone_respond_ready():
        #     self.start_drone_behavior()
        #     self.ran_start_behavior = True

        # Check if we need to execute the next movement in this iteration
        if not self.stop and self.get_now() - self.last_move > self.get_cur_delay():
            move = self.get_cur_animation_matrix()
            self.move_next()
        
        return move
            


