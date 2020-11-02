from sys import path
path.append('..')

from config.config import config
from .mood import Mood
import random

def happy_behavior():
    config.drone.flip_forward()

def happy_start():
    config.drone.set_speed(100)
    config.drone.flip_back()

def sad_behavior():
    sad_start()

def sad_start():
    config.drone.set_speed(10)
    if random.random() < 0.5:
        config.drone.flip_left()
        config.drone_emergency_stop()
        time.sleep(7)
        config.drone_takeoff()

def no_mood_behavior():
    pass

def no_mood_start():
    pass

def confused_behavior():
    pass

def confused_start():
    pass

# NOTE: Confused mood needs to be the last mood in the list. That will not be selected by random selection
raw_moods = [
    Mood(
        'happy',
        (happy_behavior, 240),
        happy_start,
        [
            (1, [0, 0, 20, 0]),
            (1, [0, 0, -20, 0])
        ]
    ),
    Mood(
        'sad',
        (sad_behavior, 240),
        sad_start,
        [
            (1, [-20, 0, 0, 0]),
            (1, [20, 0, 0, 0])
        ],
        [
            (1, [0, 0, -20, 0])
        ],
        True
    ),
    Mood(
        'no_mood',
        (no_mood_behavior, 1000),
        no_mood_start,
        [
            (2, [0, 0, 0, 0])
        ]
    ),
    Mood(
        'confused',
        (confused_behavior, 1000),
        confused_start,
        [
            (1, [0, -30, 0, 60]),
            (1, [0, 20, 0, -20])
        ]
    )
]

moods = { mood.name: mood for mood in raw_moods }