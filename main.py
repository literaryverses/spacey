import pygame as pg, sys, random, math

vec2, vec3 = pg.math.Vector2, pg.math.Vector3

RES = WIDTH, HEIGHT = 1000, 800
NUM_STARS = 100
CENTER = math.vec2(WIDTH // 2, HEIGHT // 2)
COLORS = 'red green blue orange purple cyan'.split()
Z_DISTANCE = 40 # distance from which stars begin to move

class Star:
    def __init__(self, app):
        self.screen = app.screen
        self.pos3d = None

    def get_pos3d(self):
        angle = random.uniform(0, 2*math.pi)
        radius = random.randrange(HEIGHT)
        x = radius * math.sin(angle)
        y = radius * math.cos(angle)
        return vec3(x, y, Z_DISTANCE)

    def update(self):
        pass

    def draw(self):
        pass

class Starfield:
    def __init__(self, app):
        self.stars = [Star(app for i in range(NUM_STARS))]
 
    def run(self):
        [star.update() for star in self.stars]
        [star.draw() for star in self.stars]

class App:
    def __init__(self):
        self.screen = pg.display.set_mode(RES)
        pg.display.set_caption('Wormhole')
        self.clock = pg.time.Clock()
        self.starfield = Starfield(self)
    
    def run(self):
        while True:
            self.screen.fill('black')
            self.starfield.run()

            pg.display.flip()
            [sys.exit() for e in pg.event.get() if e.type == pg.QUIT]
            self.clock.tick(60) # 60 fps

if __name__ == '__main__':
    app = App()
    app.run()