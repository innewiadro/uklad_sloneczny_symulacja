import pygame
import math

pygame.init()

WIDTH, HEIGHT = 1000, 1000
WINDOWS = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Symulacja układu słonecznego")

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (255, 0, 0)
DARK_YELLOW = (204, 204, 0)
DARK_GREY = (81, 81, 81)

class Planet:
    # AU 1 Astronomical Unit in [m]
    # G Gravitational constant [N * M**2 / kg * s**2]
    # SCALE
    # TIMESTEP one day

    AU = 149.6e6 * 1000
    G = 6.67428e-11
    SCALE = 250 / AU
    TIMESTEP = 3600 * 24

    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        self.sun = False
        self.distance_to_sun = 0

        self.orbit = []
        # predkość początkowa
        self.x_vel = 0
        self.y_vel = 0

    def draw(self, win):
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2

        pygame.draw.circle(win, self.color, (x, y), self.radius)


def main():
    run = True
    clock = pygame.time.Clock()

    sun = Planet(0, 0, 30, YELLOW, 1.98892 * 10**30)  # the last is the mass of the sun
    sun.sun = True

    earth = Planet(-1 * Planet.AU, 0, 16, BLUE, 5.9742 * 10 ** 24)

    mars = Planet(-1.524 * Planet.AU, 0, 12, RED, 6.39 * 10 ** 23)

    mercury = Planet(0.387 * Planet.AU, 0, 8, DARK_GREY, 3.30 * 10 ** 23)

    wenus = Planet(0.723 * Planet.AU, 0, 14, DARK_YELLOW, 4.8685 * 10 ** 24)

    planets = [sun, earth, mars, mercury, wenus]

    while run:
        clock.tick(60)
        #WINDOWS.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for planet in planets:
            planet.draw(WINDOWS)


        pygame.display.update()
    pygame.quit()


main()
