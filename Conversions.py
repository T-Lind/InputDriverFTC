import math

from FieldDisplay import FieldDisplay
from FieldDisplayRobot import Robot
import pickle


class Conversions:
    def __init__(self):
        self.front_left = []
        self.front_right = []
        self.back_left = []
        self.back_right = []
        self.timing = []

    def one_vel(self, robot: Robot):
        angle = math.atan2(robot.vel_x, robot.vel_y)
        magnitude = math.hypot(robot.vel_x, robot.vel_y)

        angular_velocity_rads = math.radians(robot.heading_v)

        fl = math.sin(angle + math.pi / 4) * magnitude
        br = math.sin(angle + math.pi / 4) * magnitude

        fr = math.sin(angle - math.pi / 4) * magnitude
        bl = math.sin(angle - math.pi / 4) * magnitude

        if robot.left_side_inverted:
            fl *= -1
            bl *= -1
        if robot.right_side_inverted:
            fr *= -1
            br *= -1

        fl += angular_velocity_rads
        bl += angular_velocity_rads
        fr += angular_velocity_rads
        br += angular_velocity_rads

        maximum = max(abs(fl), abs(bl), abs(fr), abs(br))
        fl /= maximum
        bl /= maximum
        fr /= maximum
        br /= maximum

        self.front_left.append(fl)
        self.back_left.append(bl)
        self.front_right.append(fr)
        self.back_right.append(br)

    def __call__(self, field_display: FieldDisplay):
        while not field_display.finished:
            self.one_vel(field_display.robot_kinematics)

            field_display()
