# Hacky way to allow for importing from parent folders
from sys import path
path.append('..')

from ithread import IThread
import cv2

from DTO.observation import Observation
from memory.memory import memory

class UmbrellaObserver(IThread):

    def __init__(self, *args, **kwargs):
        self.kind  = 'umbrella'
        self.color_lower = (23, 100, 100) 
        self.color_upper = (35, 255, 255)
        super().__init__(*args, **kwargs)
    
    def do(self):
        frame = self.queue.get()
        area, frame = self.track(frame)
        if area:
            memory.found()
            self.notify_consumers(
                (
                    frame,
                    Observation(
                        self.kind,
                        area
                    )
                )
            )
        else:
            memory.lost()
            self.notify_consumers(
                (
                    frame,
                    None
                )
            )        
    
    def track(self, frame):
        """Simple HSV color space tracking"""
        # resize the frame, blur it, and convert it to the HSV
        # color space
        blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

        # construct a mask for the color then perform
        # a series of dilations and erosions to remove any small
        # blobs left in the mask
        mask = cv2.inRange(hsv, self.color_lower, self.color_upper)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        # find contours in the mask and initialize the current
        # (x, y) center of the ball
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0]
        center = None

        # only proceed if at least one contour was found
        if len(cnts) > 0:
            # find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle and
            # centroid
            # Once the center of the object is determined, its distance from the center of the frame is calculated. 

            max_radius = 0
            obs = (0,0)

            for c in cnts: #iterate through every contour
                #c = max(cnts, key=cv2.contourArea)
                (x, y), radius = cv2.minEnclosingCircle(c)
                if radius > 10:
                    M = cv2.moments(c)
                    center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

                    if radius > max_radius:
                        obs = (x,y)
                        max_radius = radius
            
            if max_radius > 10:
                return ((obs[0], obs[1]), max_radius), hsv #feed the optimized xoffset and yoffset to telloCV.py
            else: 
                return None, hsv
        else:
            return None, hsv

