import time

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
                 ):

        self.WINDOW_HEIGHT = WINDOW_HEIGHT
        self.WINDOW_WIDTH = WINDOW_WIDTH

        pygame.init()
        pygame.display.set_caption("Robot Input Driver for FTC")

        self.win = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))

        self.image = pygame.image.load(r'rover-ruckus-field.png')

        self.ROBOT_SIZE = ROBOT_SIZE / 0.222
        self.robot_image = pygame.image.load('robot_image.png')
        self.robot_image = pygame.transform.scale(self.robot_image, (self.ROBOT_SIZE, self.ROBOT_SIZE))
        self.robot_pivot = (self.robot_image.get_width() / 2, self.robot_image.get_height() / 2)

        self.robot = pygame.Surface([self.ROBOT_SIZE, self.ROBOT_SIZE])
        self.robot.set_colorkey((0, 0, 0))
        self.robot.fill((255, 255, 0))

        self.running = True

        # Kinematic data

        self.robot_x = ROBOT_INIT_X
        self.robot_y = ROBOT_INIT_Y
        self.robot_heading = ROBOT_INIT_HEADING

        self.robot_vel_x = 1
        self.robot_vel_y = 0

        self.robot_acc_x = 0
        self.robot_acc_y = 0

        self.last_time = time.time()
        self.current_time = time.time()

    def __call__(self):
        self.current_time = time.time()
        time_step = self.current_time-self.last_time

        self.robot_x += self.robot_vel_x*time_step
        self.robot_y += self.robot_vel_y*time_step

        self.robot_vel_x += self.robot_acc_x*time_step
        self.robot_vel_y += self.robot_acc_y*time_step

        self.win.blit(self.image, (0, 0))

        # Event activator
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        pos = (self.robot_x, self.robot_y)
        blitRotate(self.win, self.robot_image, pos, self.robot_pivot, self.robot_heading)

        pygame.draw.line(self.win, (0, 255, 0), (pos[0] - 10, pos[1]), (pos[0] + 10, pos[1]), 2)
        pygame.draw.line(self.win, (0, 255, 0), (pos[0], pos[1] - 10), (pos[0], pos[1] + 10), 2)

        pygame.display.flip()

        pygame.display.update()

        self.last_time = self.current_time

    def in_to_pixels(self, val):
        return val*(self.WINDOW_WIDTH/141)

    def set_motion(self, vel_x=None, vel_y=None, acc_x=None, acc_y=None, heading=None):
        if vel_x is not None:
            self.robot_vel_x = self.in_to_pixels(vel_x)

        if vel_y is not None:
            self.robot_vel_y = self.in_to_pixels(vel_y)

        if acc_x is not None:
            self.robot_acc_x = self.in_to_pixels(acc_x)

        if acc_y is not None:
            self.robot_acc_x = self.in_to_pixels(acc_y)

        if heading is not None:
            self.robot_heading = heading

        # Check if it has collided

        if self.robot_x+self.ROBOT_SIZE/2 >= self.WINDOW_WIDTH:
            self.robot_vel_x = 0
            self.robot_acc_x = 0
            print("Collision!")

        if self.robot_y+self.ROBOT_SIZE/2 >= self.WINDOW_HEIGHT:
            self.robot_vel_y = 0
            self.robot_acc_y = 0
            print("Collision!")

        if self.robot_x < self.ROBOT_SIZE/2:
            self.robot_vel_x = 0
            self.robot_acc_x = 0
            print("Collision!")

        if self.robot_y < self.ROBOT_SIZE/2:
            self.robot_vel_y = 0
            self.robot_acc_y = 0
            print("Collision!")

