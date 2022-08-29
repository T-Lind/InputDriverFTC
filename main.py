import pygame

WINDOW_WIDTH = 637
WINDOW_HEIGHT = 632

ROBOT_SIZE = 18  # IN

ROBOT_INIT_X = 100
ROBOT_INIT_Y = 100
ROBOT_INIT_HEADING = 0

pygame.init()
pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Robot Input Driver for FTC")

display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

image = pygame.image.load(r'rover-ruckus-field.png')


if __name__ == '__main__':
    ROBOT_SIZE *= 0.222




    # Main loop
    running = True

    while running:
        display_surface.blit(image, (0, 0))



        # Event activator
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False




        pygame.display.update()

