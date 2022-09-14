import math
import sys
import time

from FieldDisplay import FieldDisplay

# Size of robot is in inches, the rest is in meters
robot = FieldDisplay(ROBOT_INIT_X=0, ROBOT_INIT_Y=1, GUI=True, TELEMETRY=True)


def get_x(time):
    if time < 2.5:
        return math.sin(0.2 * time * math.pi)
    elif time < 4:
        return 1
    elif time < 6:
        return 0.5 * time - 1
    elif time < 9:
        return math.sin(0.2 * time * math.pi + math.pi) + math.sqrt(2)
    else:
        return sys.float_info.min


if __name__ == "__main__":
    timing = 0
    while robot.running:
        robot.set_motion(x=get_x(timing))
        time.sleep(0.01)
        timing += 0.01

        robot()
