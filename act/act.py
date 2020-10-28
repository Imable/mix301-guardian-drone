# # Hacky way to allow for importing from parent folders
from sys import path
path.append('..')

from ithread import IThread

from config.config import config
from memory.memory import memory

from helper.matrix import mat_add, mat_movement

import time

class Act(IThread):
    
    def graceful_exit(self):
        if config.use_drone:
            config.drone.land()
   
    def run(self):
        while not self.exit:
            
            # inject moves from behavior here
            # count, avg_action = 0, memory.behave() # [0, 0, 0, 0]

            behavior_move, recognition_move = memory.behave(), self.queue.get() #memory.behave(), [0,0,0,0],
           
            move = mat_add(behavior_move, recognition_move)
          
            # Send movements to drone if we are using the drone
            print(move)

            # If we use the drone, the drone is ready to respond and the move is not just [0,0,0,0], send the move to the drone
            if config.use_drone and config.drone_respond_ready() and mat_movement(move):
                config.drone.send_rc_control(
                    move[0],
                    move[1],
                    move[2],
                    move[3]
                )
            
            time.sleep(0.1)

        self.graceful_exit()
        
    # def add_action(self, avg_action, cur_action):
    #     new_action = []

    #     for avg, cur in zip(avg_action, cur_action):
    #         new_action.append(avg + cur)

    #     return new_action      