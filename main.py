import pygame as pg, sys, random as r, math, color as c

vec2, vec3 = pg.math.Vector2, pg.math.Vector3

RES = WIDTH, HEIGHT = 1000, 800
NUM_STARS = 1500
CENTER = vec2(WIDTH // 2, HEIGHT // 2)
COLORS = [c.temperature, c.rainbow, c.pastels]

z_distance = 40 # distance from which stars begin to move
alpha = 120 # transparency value
scaling = 1
velocity = 0 # velocity value
ang_velocity = 0.2 # angular velocity value
color_choice = 0
#Z_DISTANCE = 140 # distance from which stars begin to move
#ALPHA = 30 # transparency value

class Star:
    def __init__(self, app):
        self.screen = app.screen
        self.pos3d = self.reset()
        self.vel = r.uniform(0.05, 0.25) # speed
        #self.vel = random.uniform(0.45, 0.95) # speed
        self.color = COLORS[color_choice]() # color
        self.size = 1 # size
        self.screen_pos = vec2(0, 0) # position relative to screen

    def reset(self, scale_pos = 35) -> vec3:
        angle = r.uniform(0, 2*math.pi)
        radius = r.randrange(HEIGHT // scale_pos, HEIGHT) * scale_pos
        #radius = random.randrange(HEIGHT // 4, HEIGHT // 2) * scale_pos
        x = radius * math.sin(angle)
        y = radius * math.cos(angle)
        #self.color = COLORS[color_choice]
        return vec3(x, y, z_distance) # send new coordinates

    def update(self):
        self.pos3d.z -= self.vel # move along z-axis
        self.pos3d = self.reset() if self.pos3d.z < 1 else self.pos3d # reset if off screen

        self.screen_pos = vec2(self.pos3d.x, self.pos3d.y) / self.pos3d.z + CENTER
        self.size = (z_distance - self.pos3d.z) / (scaling * self.pos3d.z) # change size based on z-axis position
        self.pos3d.xy = self.pos3d.xy.rotate(ang_velocity) # rotate xy
        #mouse_pos = CENTER - vec2(pg.mouse.get_pos())
        #self.screen_pos += mouse_pos

    def draw(self):
        #pg.draw.rect(self.screen, self.color, (*self.screen_pos, self.size, self.size))
        pg.draw.circle(self.screen, self.color, self.screen_pos, self.size)

class Starfield:
    def __init__(self, app):
        self.stars = [Star(app) for i in range(NUM_STARS)]

    def run(self):
        [star.update() for star in self.stars]
        self.stars.sort(key=lambda star: star.pos3d.z, reverse = True) # painter's algo
        [star.draw() for star in self.stars]

class App:
    def __init__(self):
        self.screen = pg.display.set_mode(RES)
        self.alpha_surface = pg.Surface(RES)
        self.alpha_surface.set_alpha(alpha)
        pg.display.set_caption('Wormhole')
        self.clock = pg.time.Clock()
        self.starfield = Starfield(self)
    
    def run(self):
        while True:
            global alpha, z_distance, ang_velocity, scaling, color_choice
            self.screen.blit(self.alpha_surface, (0,0))
            self.starfield.run()

            pg.display.flip()
            [sys.exit() for e in pg.event.get() if e.type == pg.QUIT] # exit
            
            pressed = pg.key.get_pressed() # keyboard input
            if pressed[pg.K_f]: # f -> more transparent
                alpha = (alpha - 1) if (alpha > 0) else 0
                self.alpha_surface.set_alpha(alpha)
            if pressed[pg.K_g]: # g -> less transparent
                alpha = (alpha + 1) if (alpha < 255) else 255
                self.alpha_surface.set_alpha(alpha)
            if pressed[pg.K_z]: # z -> more z_axis
                z_distance += 1
            if pressed[pg.K_x]: # x -> less z_axis 
                z_distance -= 1
            if pressed[pg.K_a]: # a -> rotate left speed
                ang_velocity += 0.01
            if pressed[pg.K_d]: # d -> rotate right speed
                ang_velocity -= 0.01
            if pressed[pg.K_c]: # c -> size gets larger
                scaling = (scaling - 0.01) if (scaling > 0.01) else scaling
            if pressed[pg.K_v]: # v -> size gets smaller
                scaling = (scaling + 0.01) if (scaling < z_distance) else z_distance
            #if pressed[pg.K_b]: # b -> change color schemes
            #    color_choice = (color_choice + 1) if (color_choice < 3) else 0
            if pressed[pg.K_SPACE]: # space = reset to default
                z_distance = 40
                alpha = 120
                self.alpha_surface.set_alpha(alpha)
                scaling = 1
                ang_velocity = 0.2
                color_choice = 0

            self.clock.tick(60) # 60 fps

if __name__ == '__main__':
    app = App()
    app.run()