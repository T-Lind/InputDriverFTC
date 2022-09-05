import math
import time

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

    def one_vel(self, robot: Robot, run_time):
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
        self.timing.append(int((time.time()-run_time)))

    def __call__(self, field_display: FieldDisplay):
        while not field_display.finished:
            self.one_vel(field_display.robot_kinematics, field_display.run_time)
            field_display()

        output_file_fl = 'fl.data'
        output_file_bl = 'bl.data'
        output_file_fr = 'fr.data'
        output_file_br = 'br.data'
        fw_fl = open(output_file_fl, 'wb')
        fw_bl = open(output_file_bl, 'wb')
        fw_fr = open(output_file_fr, 'wb')
        fw_br = open(output_file_br, 'wb')

        pickle.dump(self.front_left, fw_fl)
        pickle.dump(self.back_left, fw_bl)
        pickle.dump(self.front_right, fw_fr)
        pickle.dump(self.back_right, fw_br)

        fw_fl.close()
        fw_bl.close()
        fw_fr.close()
        fw_br.close()
