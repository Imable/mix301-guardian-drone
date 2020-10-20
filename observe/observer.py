# Hacky way to allow for importing from parent folders
from sys import path
path.append('..')

from ithread import IThread
import cv2

from DTO.observation import Observation

class Observer(IThread):

    def __init__(self, kind, model, *args, **kwargs):
        self.kind  = kind
        self.model = cv2.CascadeClassifier(cv2.data.haarcascades + model)
        super().__init__(*args, **kwargs)

    def do(self):
        frame = self.queue.get()
        # Potentially filter on skin color first
        rects = self.model.detectMultiScale(frame, 1.1, 5)
        
        if len(rects) > 0:
            self.notify_consumers(
                Observation(
                    self.kind,
                    rects[0],
                    100 # TODO: Implement actual distance calculation: https://www.pyimagesearch.com/2015/01/19/find-distance-camera-objectmarker-using-python-opencv/
                )
            )
