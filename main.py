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
DARK_ORANGE = (255, 140, 0)
MODERATE_BLUE = (40, 60, 80)
VERY_SOFT_CYAN = (68, 85, 90)
DARK_BROWN = (54, 34, 4)
VANILLA = (243, 229, 177)

FONT = pygame.font.SysFont("comicsan", 14)


class Planet:
    # AU 1 Astronomical Unit in [m]
    # G Gravitational constant [N * M**2 / kg * s**2]
    # SCALE
    # TIMESTEP one day

    AU = 149.6e6 * 1000
    SCALE = 16 / AU
    G = 6.67428 * 10**-11

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

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                updated_points.append((x, y))

            pygame.draw.lines(win, self.color, False, updated_points, 2)

        if not self.sun:
            distance_text = FONT.render(f"{round(self.distance_to_sun/1000, 1)}km", True, WHITE)
            win.blit(distance_text, (x - distance_text.get_width()/2, (y - distance_text.get_height()/2) - 30))

        pygame.draw.circle(win, self.color, (x, y), self.radius)

    def attraction_of_objects(self, other):
        # distance between 2 object

        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x**2 + distance_y**2)

        if other.sun:
            self.distance_to_sun = distance

        # force F = G * m1 * m2 / r**2
        force = self.G * self.mass * other.mass / distance ** 2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y

    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue
            fx, fy = self.attraction_of_objects(planet)
            total_fx += fx
            total_fy += fy

        # F = m * a == > a = F / m

        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))


def main():
    run = True

    clock = pygame.time.Clock()

    sun = Planet(0, 0, 6, YELLOW, 1.98892 * 10**30)  # the last is the mass of the sun
    sun.sun = True

    earth = Planet(-1 * Planet.AU, 0, 2, BLUE, 5.97219 * 10 ** 24)
    earth.y_vel = 29.783 * 1000

    moon = Planet(earth.x - 0.016 * Planet.AU, 0, 4, RED, 7.347 * 10 ** 10)
    moon.y_vel = 1.022 * 1000

    mars = Planet(-1.524 * Planet.AU, 0, 2, RED, 6.4171 * 10 ** 23)
    mars.y_vel = 24.077 * 1000

    mercury = Planet(0.387 * Planet.AU, 0, 2, DARK_GREY, 3.3011 * 10 ** 23)
    mercury.y_vel = -47.4 * 1000

    wenus = Planet(0.723 * Planet.AU, 0, 2, DARK_YELLOW, 4.867 * 10 ** 24)
    wenus.y_vel = -35.02 * 1000

    jupiter = Planet(-5.20336301 * Planet.AU, 0, 6, DARK_ORANGE, 1.8819 * 10 ** 27)
    jupiter.y_vel = 13.06 * 1000

    saturn = Planet(-9.582 * Planet.AU, 0, 5, VANILLA, 5.6834 * 10 ** 26)
    saturn.y_vel = 9.68 * 1000

    uran = Planet(-19.201 * Planet.AU, 0, 5, VERY_SOFT_CYAN, 8.6813 * 10 ** 25)
    uran.y_vel = 6.80 * 1000

    neptun = Planet(-30.047 * Planet.AU, 0, 5, MODERATE_BLUE, 1.02413 * 10 ** 26)
    neptun.y_vel = 5.43 * 1000

    planets = [sun, mercury, earth,  mars, wenus, jupiter, saturn, uran, neptun]

    while run:
        clock.tick(60)
        WINDOWS.fill((0, 0, 0))

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False

        for planet in planets:
            planet.update_position(planets)
            planet.draw(WINDOWS)

        pygame.display.update()

    pygame.quit()


main()
