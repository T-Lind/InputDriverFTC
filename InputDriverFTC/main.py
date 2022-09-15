import math
import sys
import time

from InputDriverFTC.FieldDisplay import FieldDisplay

# Size of robot is in inches, the rest is in meters
robot = FieldDisplay(ROBOT_INIT_X=3.35, ROBOT_INIT_Y=0.88, ROBOT_INIT_HEADING=180, ROBOT_SIZE=0.406)


def get_x(t):
    if t < 2:
        return 0.64 * math.cos(math.pi / 2 * t) - 0.64
    if t < 4.4:
        return -0.64 * 2
    if t < 4.9:
        return -0.085 * math.cos(2 * math.pi * t + 0.63) - 0.085 + -0.64 * 2
    if t < 25:
        return -0.64 * 2 - 0.085 * 2
    if t < 25.5:
        return (-0.64 * 2 - 0.085 * 2) - 0.1 * math.cos(2 * math.pi * t) + 0.1
    return -0.64 * 2 + 0.05


def get_y(t):
    if t < 1.6:
        return 0
    if t < 3.4:
        return -0.21 * math.sin(0.7 * math.pi * t - 0.9) + 0.105
    if t < 25.25:
        return 0.044
    if t < 26.25:
        return 0.044 - 0.3 - 0.3 * math.cos(math.pi * t - 0.79)
    return -0.556


def get_heading(t):
    if t < 3.4:
        return 0
    if t < 4.4:
        return -51 * math.cos(math.pi * t - 1.25) - 51
    return -102


if __name__ == "__main__":
    timing = 0
    while robot.running:
        # robot.set_motion(x=0,y=0)
        robot.set_motion(x=get_x(timing), y=get_y(timing), heading=get_heading(timing))
        time.sleep(0.01)
        timing += 0.01

        robot()
