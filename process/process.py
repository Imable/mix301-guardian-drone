# # Hacky way to allow for importing from parent folders
from sys import path
path.append('..')

from ithread import IThread

from config.config import config

from .controller import Controller

class Process(IThread):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.controller = Controller()

    # Override the put_queue function, because this thread uses a PriorityQueue
    def put_queue(self, obj, priority=3):
        self.queue.put((priority, obj))
    
    def do(self):
        _, observation = self.queue.get()

        # print(f'Observed {observation.kind} at {observation.rect}!')

        errors = self.get_errors(observation)
        update = self.controller.update(errors)
        self.notify_consumers(update)
    
    def get_errors(self, observation):
        return [
            observation.rect[0] - config.props["img"]["frame_center_x"], # X error
            config.props["img"]["frame_center_y"] - observation.rect[1], # Y error
            config.props["face"]["size"] - observation.rect[2],          # Z error
            observation.rect[0] - config.props["img"]["frame_center_x"]  # R error
        ]