from FieldDisplay import FieldDisplay

robot = FieldDisplay(ROBOT_INIT_X=10, ROBOT_INIT_Y=10, ROBOT_INIT_HEADING=-90, GUI=True, TELEMETRY=True)

robot.set_objective("Intake", "intake", 70.5, 70.5)
robot.set_objective("Deposit", "deposit", 100, 70.5)

while robot.running:
    robot.go_to_position(70.5, 70.5, margin_of_error=2)

    robot()
