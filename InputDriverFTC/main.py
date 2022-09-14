import math
import sys
import time

from FieldDisplay import FieldDisplay

# Size of robot is in inches, the rest is in meters
robot = FieldDisplay(ROBOT_INIT_X=3.35, ROBOT_INIT_Y=0.88, ROBOT_INIT_HEADING=180, ROBOT_SIZE=0.406)


def get_x(t):
    if t < 2:
        return 0.64*math.cos(math.pi/2*t)-0.64
    return -0.64*2
def get_y(t):
    if t < 1.6:
        return 0
    if t < 3.4:
        return -0.21*math.sin(0.7*math.pi*t-0.9)+0.105
    return 0.044

def get_heading(t):
    if t < 3.4:
        return 180
    elif t < 4.4:
        return 50*math.cos(math.pi*t-4.4)+130
    return 80


if __name__ == "__main__":
    timing = 0
    while robot.running:
        # robot.set_motion(x=0,y=0)
        robot.set_motion(x=get_x(timing), y=get_y(timing), heading=get_heading(timing))
        time.sleep(0.01)
        timing += 0.01

        robot()
