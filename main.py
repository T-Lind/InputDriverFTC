from FieldDisplay import FieldDisplay

robot = FieldDisplay(ROBOT_INIT_X=100, ROBOT_INIT_Y=100)

while robot.running:
    robot.set_motion(vel_y=-30, vel_x=-30)

    robot()
