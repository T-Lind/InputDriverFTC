import pygame


def m_to_pixels(WINDOW_WIDTH, val):
    return val * (WINDOW_WIDTH / 3.5814)


def pixels_to_m(WINDOW_WIDTH, val):
    return val / (WINDOW_WIDTH / 3.5814)


class Robot:
    def __init__(self, x=0, y=0, heading=0, size=0.4):
        self.x = x
        self.y = y

        self.heading = heading
        self.size = size

class GraphicalRobot:
    def __init__(self, ROBOT_SIZE, WINDOW_WIDTH):
        self.robot_size_pixels = ROBOT_SIZE / 0.222
        self.robot_image = pygame.image.load('robot_image.png')
        self.robot_image = pygame.transform.scale(self.robot_image, (
            m_to_pixels(ROBOT_SIZE, WINDOW_WIDTH), m_to_pixels(ROBOT_SIZE, WINDOW_WIDTH)))
        self.robot_image_pivot = (self.robot_image.get_width() / 2, self.robot_image.get_height() / 2)

        self.robot_pygame_surface = pygame.Surface([self.robot_size_pixels, self.robot_size_pixels])
        self.robot_pygame_surface.set_colorkey((0, 0, 0))
        self.robot_pygame_surface.fill((255, 255, 0))
