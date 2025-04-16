import sys

import pygame


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Minimal Pygame Window 🚂")
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill((0, 0, 255))  # Fill screen with black
        pygame.display.flip()  # Swap the display buffers
        clock.tick(60)  # Cap at 60 FPS


if __name__ == "__main__":
    main()
