from FieldDisplay import FieldDisplay

robot = FieldDisplay(ROBOT_INIT_X=10, ROBOT_INIT_Y=10, ROBOT_INIT_HEADING=-90)

while robot.running:
    robot.set_motion(acc_y=10, vel_x=10, heading=robot.robot_kinematics.heading + 5)

    robot()
