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
        config.stop_streaming()

    def run(self):
        while not self.exit:
            # Capture frame-by-frame
            frame = config.frame()

            # Our operations on the frame come here
            frame = imutils.resize(frame, width=config.props['img']['width'])

            # Send the frame to the consumers
            self.notify_consumers(frame)
        
        self.graceful_exit()