# # Hacky way to allow for importing from parent folders
from sys import path
path.append('..')

from ithread import IThread

from config.config import config

import time

class Act(IThread):
    
    def graceful_exit(self):
        config.drone.land()
   
    def run(self):
        while not self.exit:
            count, avg_action = 0, [0, 0, 0, 0]
            while not self.queue.empty():
                avg_action = self.add_action(avg_action, self.queue.get())
                count += 1
                
                # Combine all actions
                # Send to drone

            if count > 0:
                final_move = [int(action / count) for action in avg_action]
                print(final_move)
                
                config.drone.send_rc_control(
                    final_move[0],
                    final_move[1],
                    final_move[2],
                    final_move[3]
                )

                time.sleep(1)

        self.graceful_exit()
        
    def add_action(self, avg_action, cur_action):
        new_action = []

        for avg, cur in zip(avg_action, cur_action):
            new_action.append(avg + cur)

        return new_action
        

            