# # Hacky way to allow for importing from parent folders
from sys import path
path.append('..')

from ithread import IThread

from config.config import config
from helper.matrix import mat_nul

from .controller import Controller

class Process(IThread):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.controller = Controller()
    
    def do(self):
        # Ignore the frame
        (_, observation) = self.queue.get()

        if observation:
            errors = self.get_errors(observation)
            update = self.controller.update(errors)
            # Added update
            self.notify_consumers(update)
        else:
            self.notify_consumers(
                mat_nul()
            )
    
    def get_errors(self, observation):
        return [
            (observation.area[0][0] - config.props["img"]["frame_center_x"]) * 0.5, # X - Left right
            config.props["umbrella"]["radius"] - observation.area[1],               # Y - Backward forward distance from person, matching the size of the umbrella with the actual size
            config.props["img"]["frame_center_y"] - observation.area[0][1] - config.props["umbrella"]["height_offset"],         # Z - Up down into the air
            (observation.area[0][0] - config.props["img"]["frame_center_x"]) * 0.5  #  X - Rotate around Y axis, towards the umbrella
        ]