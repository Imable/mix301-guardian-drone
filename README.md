# Social Guardian Drone

## Set-up your environment
1. Install Python 3.7
2. Install `pipenv` using `pip install pipenv`
3. Install the dependencies for this project by running `pipenv install` in the root of this project (same directory as this `README.md`)

## Running the program
1. Run the program using the command `pipenv run python main.py`

## Basic code to control the drone
```python
from djitellopy import Tello

tello = Tello()
tello.connect()
tello.takeoff()
tello.land()
```