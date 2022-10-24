import math
import sys
import time

from InputDriverFTC.FieldDisplay import FieldDisplay
import pygame
from BezierCurve import recursive_lerp, Point


# Size of robot is in inches, the rest is in meters
robot = FieldDisplay(ROBOT_INIT_X=0, ROBOT_INIT_Y=0, ROBOT_INIT_HEADING=180, ROBOT_SIZE=0.406)
points = [Point(0.5, 0.5), Point(1, 3), Point(3, 2), Point(2, 0.5), Point(0.5, 3)]


def get_heading(time):
    return 360*math.sin(time/math.pi)

if __name__ == "__main__":
    timing = 0
    while robot.running:
        current_point = recursive_lerp(points, timing/30)
        robot.set_motion(x=current_point.x, y=current_point.y, heading=get_heading(timing))
        timing += 0.01

        robot()

