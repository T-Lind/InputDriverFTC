from FieldDisplayRobot import Robot, GraphicalRobot, m_to_pixels, pixels_to_m
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
                 WINDOW_WIDTH=632,
                 WINDOW_HEIGHT=632,
                 ROBOT_SIZE=0.4572,
                 ROBOT_INIT_X=0,
                 ROBOT_INIT_Y=0,
                 ROBOT_INIT_HEADING=0,
                 ):

        self.WINDOW_HEIGHT = WINDOW_HEIGHT
        self.WINDOW_WIDTH = WINDOW_WIDTH

        # Create the robot which controls all the kinematics
        self.robot_kinematics = Robot(x=ROBOT_INIT_X, y=ROBOT_INIT_Y, heading=ROBOT_INIT_HEADING, size=ROBOT_SIZE)

        self.robot_init_x = ROBOT_INIT_X
        self.robot_init_y = ROBOT_INIT_Y
        self.robot_init_heading = ROBOT_INIT_HEADING

        pygame.init()
        pygame.display.set_caption("Robot Input Driver for FTC")

        self.win = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        self.image = pygame.image.load(r'power-play-field.png')

        # Create the graphics for the robot
        self.graphical_robot = GraphicalRobot(ROBOT_SIZE, WINDOW_WIDTH)

        # Loop state
        self.running = True

    def __call__(self):
        """
        Method to run the field display. Takes no arguments and updates the robot position and graphics
        """

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        # Draw the background
        self.win.blit(self.image, (0, 0))

        pos = (m_to_pixels(self.WINDOW_WIDTH, self.robot_init_x)+m_to_pixels(self.WINDOW_WIDTH, self.robot_kinematics.x),
               m_to_pixels(self.WINDOW_HEIGHT, self.robot_init_y)+m_to_pixels(self.WINDOW_HEIGHT, self.robot_kinematics.y))
        blitRotate(self.win, self.graphical_robot.robot_image, pos, self.graphical_robot.robot_image_pivot,
                   self.robot_kinematics.heading+self.robot_init_heading)

        pygame.draw.line(self.win, (0, 255, 0), (pos[0] - 10, pos[1]), (pos[0] + 10, pos[1]), 2)
        pygame.draw.line(self.win, (0, 255, 0), (pos[0], pos[1] - 10), (pos[0], pos[1] + 10), 2)

        pygame.display.flip()

        pygame.display.update()

    def set_motion(self, x=None, y=None, heading=None):
        """
        Set motion data to the robot object
        :param x: the x pos to set
        :param y: the y pos to set
        :param heading: The heading for the robot to be at
        """
        if x is not None:
            self.robot_kinematics.x = x
        if y is not None:
            self.robot_kinematics.y = y
        if heading is not None:
            self.robot_kinematics.heading = heading

        if heading is not None:
            self.robot_kinematics.heading = heading

        # Check if it has collided

        # robot_buffer_size = self.robot_kinematics.size / 2
        #
        # if m_to_pixels(self.robot_kinematics.x + robot_buffer_size, self.WINDOW_WIDTH) >= self.WINDOW_WIDTH:
        #     self.robot_kinematics.x = pixels_to_m(self.WINDOW_WIDTH, self.WINDOW_WIDTH) - robot_buffer_size
        #
        # if m_to_pixels(self.robot_kinematics.y + robot_buffer_size, self.WINDOW_WIDTH) >= self.WINDOW_HEIGHT:
        #     self.robot_kinematics.y = pixels_to_m(self.WINDOW_HEIGHT, self.WINDOW_WIDTH) - robot_buffer_size
        #
        # if self.robot_kinematics.x < robot_buffer_size:
        #     self.robot_kinematics.x = robot_buffer_size
        #
        # if self.robot_kinematics.y < robot_buffer_size:
        #     self.robot_kinematics.y = robot_buffer_size
