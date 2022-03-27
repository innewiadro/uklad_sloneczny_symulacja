import pygame
import math

pygame.init()

WIDTH, HEIGHT = 800, 800
WINDOWS = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Symulacja układu słonecznego")


def main():
    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

    pygame.quit()

main()
