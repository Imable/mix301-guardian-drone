import time
from numpy import clip

# Modified code from PyImageSearch
# https://www.pyimagesearch.com/2019/04/01/pan-tilt-face-tracking-with-a-raspberry-pi-and-opencv/
class PID:
    def __init__(self, kP=1, kI=0, kD=0):
        # initialize gains
        self.kP = kP
        self.kI = kI
        self.kD = kD

        self.cP = 0
        self.cI = 0
        self.cD = 0

        self.current_time = time.time()
        self.previous_time = self.current_time

        self.previous_error = 0

    def initialize(self):
        # initialize the current and previous time
        self.current_time = time.time()
        self.previous_time = self.current_time

        # initialize the previous error
        self.previous_error = 0

        # initialize the term result variables
        self.cP = 0
        self.cI = 0
        self.cD = 0

    def update(self, error, sleep=0.2):
        # pause for a bit
        # time.sleep(sleep)

        # grab the current time and calculate delta time
        self.current_time = time.time()
        delta_time = self.current_time - self.previous_time

        # calculate the delta error
        delta_error = error - self.previous_error

        # calculate the proportional term
        self.cP = error

        # calculate the integral term
        self.cI += error * delta_time

        # calculate the derivative term (and prevent divide by zero)
        self.cD = (delta_error / delta_time) if delta_time > 0 else 0

        # save previous time and error for the next update
        self.previous_time = self.current_time
        self.previous_error = error

        # sum the terms and return
        return sum([
            self.kP * self.cP,
            self.kI * self.cI,
            self.kD * self.cD])

class Controller:
    def __init__(self):
        self.pids = [
            PID(kP=0.05, kI=0.0001, kD=0.01),   # X
            PID(kP=0.3, kI=0.0001, kD=0.1),     # Y
            PID(kP=0.7, kI=0.0001, kD=0.1),     # Z
            PID(kP=0.4, kI=0.0001, kD=0.1)      # R ( = rotation - yaw)
        ]

        for pid in self.pids:
            pid.initialize()
    
    def update(self, errors):
        '''
        Returns list of updates to be send to the drone in order of X, Y, Z, R.
        '''
        updates = []

        for pid, error in zip(self.pids, errors):
            update = pid.update(error, sleep=0)
            update = int(clip(update, -30, 30))
            updates.append(update)

        return updates