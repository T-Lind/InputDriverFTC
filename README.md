# InputDriverFTC

A pathing library to help you visualize Coyote Beta's x/y piecewise position functions over time.

### Example of How to Use:

```python
import math
import time

from InputDriverFTC.FieldDisplay import FieldDisplay

# Everything is in meters
robot = FieldDisplay(ROBOT_INIT_X=3.35, ROBOT_INIT_Y=0.88, ROBOT_INIT_HEADING=180, ROBOT_SIZE=0.406)


def get_x(t):
   return -t*0.5
def get_y(t):
    return 0.25*math.sin(t)

def get_heading(t):
    if t < 3.4:
        return 180
    elif t < 4.4:
        return 50*math.cos(math.pi*t-4.4)+130
    return 80


if __name__ == "__main__":
    timing = 0
    while robot.running:
        robot.set_motion(x=get_x(timing), y=get_y(timing), heading=get_heading(timing))
        time.sleep(0.01)
        timing += 0.01

        robot()

```
