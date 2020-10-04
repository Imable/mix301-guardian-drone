# Hacky way to allow for importing from parent folders
from sys import path
path.append('..')

from ithread import IThread
from queue import Queue
import cv2

class Observer(IThread):

    def __init__(self, model, *args, **kwargs):
        self.model = cv2.CascadeClassifier(cv2.data.haarcascades + model)
        super().__init__(*args, **kwargs)

    def run(self):
        while True:
            while not self.queue.empty():
                frame = self.queue.get()
                rects = self.model.detectMultiScale(frame, 1.1, 5)