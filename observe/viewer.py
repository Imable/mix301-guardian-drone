# Hacky way to allow for importing from parent folders
from sys import path
path.append('..')

from ithread import IThread

import cv2

class Viewer(IThread):
    def do(self):
        frame = self.queue.get()
        cv2.imshow("Drone", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            self.exit = True