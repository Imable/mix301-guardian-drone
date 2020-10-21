from djitellopy import Tello
import json
import os
import sys

class Config:
    def __init__(self):
        self.drone = None
        self.props = self.read_properties()
        self.calculate_additional_props()
        self.connect_to_drone()
    
    def connect_to_drone(self):
        self.drone = Tello()
        self.drone.connect()
        self.drone.streamon()
        self.frame = self.drone.get_frame_read()
        self.drone.takeoff()
        self.drone.move_up(70)

    def read_properties(self):
        with open('./config/properties.json') as json_file:
            props = json.load(json_file)

        return props
    
    def calculate_additional_props(self):
        self.props["img"]["height"] = 720 * self.props["img"]["width"] / 1280
        self.props["img"]["frame_center_x"] = self.props["img"]["width"] * 0.5
        self.props["img"]["frame_center_y"] = self.props["img"]["height"] * 0.5

config = Config()