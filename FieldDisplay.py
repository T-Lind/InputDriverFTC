import time
from FieldDisplayRobot import Robot, GraphicalRobot, in_to_pixels, pixels_to_in
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
    def __init__(self,
                 WINDOW_WIDTH=637,
                 WINDOW_HEIGHT=632,
                 ROBOT_SIZE=18,
                 ROBOT_INIT_X=0,
                 ROBOT_INIT_Y=0,
                 ROBOT_INIT_HEADING=0,
                 MAX_VEL=60,
                 MAX_ACC=25
                 ):

        self.WINDOW_HEIGHT = WINDOW_HEIGHT
        self.WINDOW_WIDTH = WINDOW_WIDTH

        pygame.init()
        pygame.display.set_caption("Robot Input Driver for FTC")

        self.win = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))

        self.image = pygame.image.load(r'rover-ruckus-field.png')

        self.robot_kinematics = Robot(x=ROBOT_INIT_X, y=ROBOT_INIT_Y, heading=ROBOT_INIT_HEADING, size=ROBOT_SIZE,
                                      max_v=MAX_VEL, max_a=MAX_ACC)
        self.graphical_robot = GraphicalRobot(ROBOT_SIZE, WINDOW_WIDTH)

        self.running = True

        self.last_time = time.time()
        self.current_time = time.time()

    def __call__(self):
        self.current_time = time.time()
        time_step = self.current_time - self.last_time

        self.robot_kinematics.motion_check()

        self.robot_kinematics.x += self.robot_kinematics.vel_x * time_step
        self.robot_kinematics.y += self.robot_kinematics.vel_y * time_step

        self.robot_kinematics.vel_x += self.robot_kinematics.acc_x * time_step
        self.robot_kinematics.vel_y += self.robot_kinematics.acc_y * time_step

        # Draw the background
        self.win.blit(self.image, (0, 0))

        # Event activator
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        pos = (in_to_pixels(self.robot_kinematics.x, self.WINDOW_WIDTH), in_to_pixels(self.robot_kinematics.y, self.WINDOW_WIDTH))
        blitRotate(self.win, self.graphical_robot.robot_image, pos, self.graphical_robot.robot_image_pivot,
                   self.robot_kinematics.heading)

        pygame.draw.line(self.win, (0, 255, 0), (pos[0] - 10, pos[1]), (pos[0] + 10, pos[1]), 2)
        pygame.draw.line(self.win, (0, 255, 0), (pos[0], pos[1] - 10), (pos[0], pos[1] + 10), 2)

        pygame.display.flip()

        pygame.display.update()

        self.last_time = self.current_time

    def set_motion(self, vel_x=None, vel_y=None, acc_x=None, acc_y=None, heading=None):
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
            print("Collision!")

        if in_to_pixels(self.robot_kinematics.y + robot_buffer_size, self.WINDOW_WIDTH) >= self.WINDOW_HEIGHT:
            self.robot_kinematics.y = pixels_to_in(self.WINDOW_HEIGHT, self.WINDOW_WIDTH) - robot_buffer_size
            print("Collision!")

        if self.robot_kinematics.x < robot_buffer_size:
            self.robot_kinematics.x = robot_buffer_size
            print("Collision!")

        if self.robot_kinematics.y < robot_buffer_size:
            self.robot_kinematics.y = robot_buffer_size
            print("Collision!")

    # def set_objective(self, name="Objective", objective_type="deposit", x=100, y=100):

