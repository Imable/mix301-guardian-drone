from djitellopy import Tello
import json
import os
import sys
import cv2
import time

class Config:
    def __init__(self):
        self.time_of_initialization = time.time()
        self.props = self.read_properties()

        self.use_drone = True
        self.drone_flying = False
        self.drone = None

        self.calculate_additional_props()

        if self.use_drone:
            self.connect_to_drone()
        else:
            self.cap = cv2.VideoCapture(0)
    
    def connect_to_drone(self):
        self.drone = Tello()
        self.drone.connect()
        self.drone.streamon()
        self.cap = self.drone.get_frame_read()
        # self.drone_takeoff()
        # self.drone.move_up(100)

    def drone_respond_ready(self):
        return time.time() - self.time_of_initialization > self.props["drone"]["respond_delay"]
    
    def frame(self):
        if self.use_drone:
            frame = self.cap.frame
        else:
            ret, frame = self.cap.read()
        
        return frame
    
    def stop_streaming(self):
        if self.use_drone:
            self.drone.streamoff()
        else:
            self.cap.release()
    
    def drone_emergency_stop(self):
        self.drone.emergency()
        self.drone_flying = False
    
    def drone_takeoff(self):
        self.drone.takeoff()
        self.drone_flying = True

    def read_properties(self):
        with open('./config/properties.json') as json_file:
            props = json.load(json_file)

        return props
    
    def calculate_additional_props(self):
        self.props["img"]["height"] = 300
        self.props["img"]["frame_center_x"] = self.props["img"]["width"] * 0.5
        self.props["img"]["frame_center_y"] = self.props["img"]["height"] * 0.5

config = Config()