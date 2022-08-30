import pygame


def in_to_pixels(WINDOW_WIDTH, val):
    return val * (WINDOW_WIDTH / 141)


def pixels_to_in(WINDOW_WIDTH, val):
    return val / (WINDOW_WIDTH / 141)


class Robot:
    def __init__(self, x=0, y=0, vel_x=0, vel_y=0, acc_x=0, acc_y=0, heading=0, size=18, max_v=60, max_a=30,
                 loaded=False):
        self.x = x
        self.y = y

        self.vel_x = vel_x
        self.vel_y = vel_y

        self.acc_x = acc_x
        self.acc_y = acc_y

        self.heading = heading
        self.size = size

        self.max_v = max_v
        self.max_a = max_a

        self.loaded = loaded

        # Keep track of points scored
        self.score = 0

    def motion_check(self):
        if self.vel_x > self.max_v:
            self.vel_x = self.max_v
            print("Reached max x vel")

        if self.vel_y > self.max_v:
            self.vel_y = self.max_v
            print("Reached max y vel")

        if self.acc_x > self.max_a:
            self.acc_x = self.max_a
            print("Reached max x acc")

        if self.acc_y > self.max_a:
            self.acc_y = self.max_a
            print("Reached max y acc")


class GraphicalRobot:
    def __init__(self, ROBOT_SIZE, WINDOW_WIDTH):
        self.robot_size_pixels = ROBOT_SIZE / 0.222
        self.robot_image = pygame.image.load('robot_image.png')
        self.robot_image = pygame.transform.scale(self.robot_image, (
            in_to_pixels(ROBOT_SIZE, WINDOW_WIDTH), in_to_pixels(ROBOT_SIZE, WINDOW_WIDTH)))
        self.robot_image_pivot = (self.robot_image.get_width() / 2, self.robot_image.get_height() / 2)

        self.robot_pygame_surface = pygame.Surface([self.robot_size_pixels, self.robot_size_pixels])
        self.robot_pygame_surface.set_colorkey((0, 0, 0))
        self.robot_pygame_surface.fill((255, 255, 0))
