import pygame as x
import random
import math

vec2, vec3 = x.math.Vector2, x.math.Vector3

RES = WIDTH, HEIGHT = 1600, 900
NUM_STARS = 1500
CENTER = vec2(WIDTH // 2, HEIGHT // 2)
COLORS = 'white'.split()
Z_DISTANCE = 140
ALPHA = 10


class Star:
    def __init__(self, app):
        self.screen = app.screen
        self.pos3d = self.get_pos3d()
        self.vel = random.uniform(0.05, 0.25)
        self.color = random.choice(COLORS)
        self.screen_pos = vec2(0, 0)
        self.size = 10

    
    def get_pos3d(self, scale_pos=35):
        angle = random.uniform(0, 2 * math.pi)
        radius = random.randrange(HEIGHT // scale_pos, HEIGHT) * scale_pos
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        return vec3(x, y, Z_DISTANCE)

    def update(self):
        self.pos3d.z -= self.vel
        self.pos3d = self.get_pos3d() if self.pos3d.z < 1 else self.pos3d

        self.screen_pos = vec2(self.pos3d.x, self.pos3d.y) / self.pos3d.z + CENTER
        self.size = (Z_DISTANCE - self.pos3d.z) / (0.2 * self.pos3d.z)
        # rotate xy
        self.pos3d.xy = self.pos3d.xy.rotate(0.2)
        # mouse
        #mouse_pos = CENTER - vec2(x.mouse.get_pos())
        #self.screen_pos += mouse_pos

    def draw(self):
        s = self.size
        if (-s < self.screen_pos.x < WIDTH + s) and (-s < self.screen_pos.y < HEIGHT + s):
            x.draw.rect(self.screen, self.color, (*self.screen_pos, self.size, self.size))


class Starfield:
    def __init__(self, app):
        self.stars = [Star(app) for i in range(NUM_STARS)]

    def run(self):
        [star.update() for star in self.stars]
        self.stars.sort(key=lambda star: star.pos3d.z, reverse=True)
        [star.draw() for star in self.stars]


class App:
    def __init__(self):
        self.screen = x.display.set_mode(RES)
        self.alpha_surface = x.Surface(RES)
        self.alpha_surface.set_alpha(ALPHA)
        self.clock = x.time.Clock()
        self.starfield = Starfield(self)

    def run(self):
        while True:
            # self.screen.fill('black')
            self.screen.blit(self.alpha_surface, (0, 0))
            self.starfield.run()

            x.display.flip()
            [exit() for i in x.event.get() if i.type == x.QUIT]
            self.clock.tick(60)


if __name__ == '__main__':
    app = App()
    app.run()
