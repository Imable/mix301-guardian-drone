# Hacky way to allow for importing from parent folders
from sys import path
path.append('..')

from ithread import IThread
from config.config import config

import cv2
import imutils
import time

class Stream(IThread):

    def graceful_exit(self):
        config.drone.streamoff()

    def run(self):
        # cap = cv2.VideoCapture(0)

        while not self.exit:
            # Capture frame-by-frame
            # ret, frame = cap.read()

            frame = config.frame.frame

            # Our operations on the frame come here
            frame = imutils.resize(frame, width=config.props['img']['width'])

            # Send the frame to the consumers
            self.notify_consumers(frame)

            # time.sleep(0.5)
        
        self.graceful_exit()

        # cap.release()
        # cv2.destroyAllWindows()