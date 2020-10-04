# Hacky way to allow for importing from parent folders
from sys import path
path.append('..')

from ithread import IThread
from config.config import config

import cv2
import imutils

class Stream(IThread):

    def run(self):
        cap = cv2.VideoCapture(0)

        while True:
            # Capture frame-by-frame
            ret, frame = cap.read()

            # Our operations on the frame come here
            frame = imutils.resize(frame, width=config.props['img']['width'])

            # Send the frame to the consumers
            self.notify_consumers(frame)

        cap.release()
        cv2.destroyAllWindows()