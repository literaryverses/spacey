import pygame as pg, sys

RES = WIDTH, HEIGHT = 1000, 800
NUM_STARS = 100

class Star:
    def __init__(self, app):
        pass

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
    
    def run(self):
        while True:
            self.screen.fill('black')

            pg.display.flip()
            [sys.exit() for e in pg.event.get() if e.type == pg.QUIT]
            self.clock.tick(60) # 60 fps

if __name__ == '__main__':
    app = App()
    app.run()