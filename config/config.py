from djitellopy import Tello
import json
import os
import sys

class Config:
    def __init__(self):
        # self.drone = self.connect_to_drone()
        self.props = self.read_properties()
    
    def connect_to_drone(self):
        drone = Tello()
        drone.connect()
        return drone

    def read_properties(self):
        with open('./config/properties.json') as json_file:
            props = json.load(json_file)

        return props

config = Config()