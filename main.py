import pygame as pg, sys

RES = WIDTH, HEIGHT = 800, 400

class App:
    def __init__(self):
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
    
    def run(self):
        while True:
            self.screen.fill('black')

            [sys.exit() for e in pg.event.get() if e.type == pg.QUIT]
            pg.display.flip()
            self.clock.tick(60) # 60 fps

if __name__ == '__main__':
    app = App()
    app.run()