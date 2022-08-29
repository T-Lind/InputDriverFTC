import pygame

WINDOW_WIDTH = 637
WINDOW_HEIGHT = 632

ROBOT_SIZE = 18  # IN

ROBOT_INIT_X = 100
ROBOT_INIT_Y = 100
ROBOT_INIT_HEADING = 0

pygame.init()
pygame.display.set_caption("Robot Input Driver for FTC")

win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

image = pygame.image.load(r'rover-ruckus-field.png')

vel = 10
angle = 0


if __name__ == '__main__':
    ROBOT_SIZE /= 0.222
    robot = pygame.Surface([ROBOT_SIZE, ROBOT_SIZE])
    robot.set_colorkey((0, 0, 0))
    robot.fill((255, 255, 0))

    robot_x = ROBOT_INIT_X
    robot_y = ROBOT_INIT_Y
    robot_heading = ROBOT_INIT_HEADING

    # Main loop
    running = True

    while running:
        win.blit(image, (0, 0))

        # Event activator
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Move robot with keys
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and robot_x > 0:
            robot_x -= vel

        if keys[pygame.K_RIGHT] and robot_x < WINDOW_WIDTH:
            robot_x += vel

        if keys[pygame.K_DOWN] and robot_y < WINDOW_HEIGHT:
            robot_y += vel

        if keys[pygame.K_UP] and robot_y > 0:
            robot_y -= vel

        if keys[pygame.K_a]:
            angle += 5

        if keys[pygame.K_d]:
            angle -= 5

        rotatedSail = pygame.transform.rotate(robot, angle)
        Sail_rect = robot.get_rect(topleft=(robot_x - ROBOT_SIZE / 2, robot_y - ROBOT_SIZE / 2))
        win.blit(rotatedSail, Sail_rect)
        pygame.display.flip()

        pygame.display.update()

