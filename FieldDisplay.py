import math
import time
from FieldDisplayRobot import Robot, GraphicalRobot, in_to_pixels, pixels_to_in
from Objective import Objective
import pygame

def blitRotate(surf, image, pos, originPos, angle):
    image_rect = image.get_rect(topleft=(pos[0] - originPos[0], pos[1] - originPos[1]))
    offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center
    rotated_offset = offset_center_to_pivot.rotate(-angle)
    rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)
    rotated_image = pygame.transform.rotate(image, angle)
    rotated_image_rect = rotated_image.get_rect(center=rotated_image_center)
    surf.blit(rotated_image, rotated_image_rect)


class FieldDisplay:
    N_INPUTS = 6

    def __init__(self,
                 WINDOW_WIDTH=632,
                 WINDOW_HEIGHT=632,
                 ROBOT_SIZE=18,
                 ROBOT_INIT_X=0,
                 ROBOT_INIT_Y=0,
                 ROBOT_INIT_HEADING=0,
                 MAX_VEL=60,
                 MAX_ACC=25,
                 GUI=True,
                 TELEMETRY=False
                 ):
        """
        A class to display an autonomous plotter for FTC. Input data is optional!
        :param WINDOW_WIDTH: The width of the input window in pixels
        :param WINDOW_HEIGHT: The height of the input window in pixels
        :param ROBOT_SIZE: The size (square) of the robot in inches
        :param ROBOT_INIT_X: The starting x position (0, 0) is top left!!!
        :param ROBOT_INIT_Y:The starting y position (0, 0) is top left!!!
        :param ROBOT_INIT_HEADING: The starting heading (to the right on the screen)
        :param MAX_VEL: The maximum velocity the robot can go. Default is 60 in/s
        :param MAX_ACC: The maximum velocity the robot can go. Default is 25 in/s
        """

        self.WINDOW_HEIGHT = WINDOW_HEIGHT
        self.WINDOW_WIDTH = WINDOW_WIDTH

        self.GUI = GUI
        self.telemetry = TELEMETRY

        # Create the robot which controls all the kinematics
        self.robot_kinematics = Robot(x=ROBOT_INIT_X, y=ROBOT_INIT_Y, heading=ROBOT_INIT_HEADING, size=ROBOT_SIZE,
                                      max_v=MAX_VEL, max_a=MAX_ACC)

        if self.GUI:
            pygame.init()
            pygame.display.set_caption("Robot Input Driver for FTC")

            self.win = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
            self.image = pygame.image.load(r'rover-ruckus-field.png')

            # Create the graphics for the robot
            self.graphical_robot = GraphicalRobot(ROBOT_SIZE, WINDOW_WIDTH)


        # Loop state
        self.running = True

        # Objective list
        self.objectives = []

        self.last_time = time.time()
        self.current_time = time.time()
        self.run_time = time.time()
        self.elapsed_time = 0

        self.last_time_printed = -1

        self.finished = False

    def __call__(self, finished=False):
        """
        Method to run the field display. Takes no arguments and updates the robot position and graphics
        :param finished set the field to finish
        """
        self.current_time = time.time()
        time_step = self.current_time - self.last_time

        self.robot_kinematics.motion_check()

        self.robot_kinematics.x += self.robot_kinematics.vel_x * time_step
        self.robot_kinematics.y += self.robot_kinematics.vel_y * time_step

        self.robot_kinematics.vel_x += self.robot_kinematics.acc_x * time_step
        self.robot_kinematics.vel_y += self.robot_kinematics.acc_y * time_step

        self.robot_kinematics.heading += self.robot_kinematics.heading_v * time_step
        self.robot_kinematics.heading_v += self.robot_kinematics.heading_acc * time_step

        time_elapsed = int((time.time()-self.run_time))
        self.elapsed_time = time_elapsed
        if self.telemetry and time_elapsed % 3 == 0 and time_elapsed != self.last_time_printed:
            self.last_time_printed = time_elapsed
            print(f'''\
                =================
                Telemetry Output:
                X: {self.robot_kinematics.x}, Y: {self.robot_kinematics.y}
                X velocity: {self.robot_kinematics.vel_x}, Y velocity: {self.robot_kinematics.vel_y}
                X acceleration: {self.robot_kinematics.acc_x}, Y acceleration: {self.robot_kinematics.acc_y}
            ''')

        if self.GUI:
            # Event activator
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Draw the background
            self.win.blit(self.image, (0, 0))

            pos = (in_to_pixels(self.robot_kinematics.x, self.WINDOW_WIDTH),
                   in_to_pixels(self.robot_kinematics.y, self.WINDOW_WIDTH))
            blitRotate(self.win, self.graphical_robot.robot_image, pos, self.graphical_robot.robot_image_pivot,
                       self.robot_kinematics.heading)

            pygame.draw.line(self.win, (0, 255, 0), (pos[0] - 10, pos[1]), (pos[0] + 10, pos[1]), 2)
            pygame.draw.line(self.win, (0, 255, 0), (pos[0], pos[1] - 10), (pos[0], pos[1] + 10), 2)

            self.draw_objectives()

            pygame.display.flip()

            pygame.display.update()

        self.last_time = self.current_time

    def set_motion(self, vel_x=None, vel_y=None, acc_x=None, acc_y=None, heading=None):
        """
        Set motion data to the robot object
        :param vel_x: The velocity for the robot to go at in the x direction (in/s)
        :param vel_y: The velocity for the robot to go at in the y direction (in/s)
        :param acc_x: The velocity for the robot to go at in the x direction (in/s^2)
        :param acc_y: The velocity for the robot to go at in the y direction (in/s^2)
        :param heading: The heading for the robot to be at
        :return:
        """
        if vel_x is not None:
            self.robot_kinematics.vel_x = vel_x

        if vel_y is not None:
            self.robot_kinematics.vel_y = vel_y

        if acc_x is not None:
            self.robot_kinematics.acc_x = acc_x

        if acc_y is not None:
            self.robot_kinematics.acc_y = acc_y

        if heading is not None:
            self.robot_kinematics.heading = heading

        # Check if it has collided

        robot_buffer_size = self.robot_kinematics.size / 2

        if in_to_pixels(self.robot_kinematics.x + robot_buffer_size, self.WINDOW_WIDTH) >= self.WINDOW_WIDTH:
            self.robot_kinematics.x = pixels_to_in(self.WINDOW_WIDTH, self.WINDOW_WIDTH) - robot_buffer_size

        if in_to_pixels(self.robot_kinematics.y + robot_buffer_size, self.WINDOW_WIDTH) >= self.WINDOW_HEIGHT:
            self.robot_kinematics.y = pixels_to_in(self.WINDOW_HEIGHT, self.WINDOW_WIDTH) - robot_buffer_size

        if self.robot_kinematics.x < robot_buffer_size:
            self.robot_kinematics.x = robot_buffer_size

        if self.robot_kinematics.y < robot_buffer_size:
            self.robot_kinematics.y = robot_buffer_size


    def take_action(self, num):
        if num == 0:
            self.robot_kinematics.acc_x += 0.01
        elif num == 1:
            self.robot_kinematics.acc_x -= 0.01
        elif num == 2:
            self.robot_kinematics.acc_y += 0.01
        elif num == 3:
            self.robot_kinematics.acc_y -= 0.01
        elif num == 4:
            self.robot_kinematics.heading_acc += 0.01
        elif num == 5:
            self.robot_kinematics.heading_acc -= 0.01

        objective = self.objectives[-1]
        return 1/math.hypot(objective.x-self.robot_kinematics.x, objective.y-self.robot_kinematics.y)

    def set_objective(self, name="Objective", objective_type="deposit", x=100, y=100):
        self.objectives.append(Objective(name, objective_type, x, y))

    def draw_objectives(self):
        for objective in self.objectives:
            pos = (in_to_pixels(objective.x, self.WINDOW_WIDTH), in_to_pixels(objective.y, self.WINDOW_WIDTH))
            if objective.objective_type == "deposit":
                pygame.draw.circle(self.win, (0, 255, 0), pos, 7, 0)
            elif objective.objective_type == "intake":
                pygame.draw.circle(self.win, (255, 0, 255), pos, 7, 0)
            else:
                raise SyntaxError("Incorrect type specified in FieldDisplay.draw_objectives(). Supported objective types are 'deposit', 'intake'")

    def go_to_position(self, x, y, end_velocity=0, margin_of_error=0.2):
        while abs(self.robot_kinematics.x-x) > margin_of_error and abs(self.robot_kinematics.y-y) > margin_of_error\
                or math.hypot(self.robot_kinematics.vel_x, self.robot_kinematics.vel_y) > end_velocity:
            self()



            negative_sign = -(self.robot_kinematics.x-x)/abs(self.robot_kinematics.x-x)
            if abs(self.robot_kinematics.x-x) > margin_of_error:
                self.robot_kinematics.vel_x += 10*negative_sign
            if abs(self.robot_kinematics.y - y) > margin_of_error:
                self.robot_kinematics.vel_y += 10*negative_sign
