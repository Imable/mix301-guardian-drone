# Hacky way to allow for importing from parent folders
from sys import path
path.append('..')

from ithread import IThread
from memory.memory import memory

import cv2

class Viewer(IThread):
    def __init__(self, *args, **kwargs):
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.text_color = (0, 0, 255)
        super().__init__(*args, **kwargs)

    def do(self):
        frame, observation = self.queue.get()

        cv2.putText(frame, f'Mood: {memory.get_mood}', (5, 20), self.font, 1, self.text_color)

        if observation:
            pt, radius = observation.area
            cv2.putText(frame, observation.kind, (int(pt[0]), int(pt[1])), self.font, 1, self.text_color)
            cv2.circle(frame, (int(pt[0]), int(pt[1])), int(radius), (0, 0, 255))
            cv2.circle(frame, (int(pt[0]), int(pt[1])), 3, (255, 0, 255))

        cv2.imshow("Drone tracking", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            self.exit = True