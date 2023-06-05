import pygame as pg, sys, random as r, math, color as c, asyncio as a

vec2, vec3 = pg.math.Vector2, pg.math.Vector3

RES = WIDTH, HEIGHT = 1000, 800
NUM_STARS = 1500
CENTER = vec2(WIDTH // 2, HEIGHT // 2)
COLORS = [c.temperature, c.rainbow, c.pastels, c.monochrome]
VELOCITY = lambda s: 0.486665 * math.log(1.62499*s + 0.121003) + 1.02781


z_distance = 40 # distance from which stars begin to move
alpha = 120 # transparency value
size_scale = 0.2 # scaling for size
radius_scale = 35 # scaling for radius
radius_x = radius_y = 0 # movement of radius
spd = 0.05 # velocity value
ang_spd = 0.2 # angular velocity value
color_choice = shape = 0

class Star:
    def __init__(self, app):
        self.screen = app.screen
        self.pos3d = self.reset()
        self.vel = r.uniform(spd, VELOCITY(spd))
        self.color = COLORS[color_choice]() # color
        self.size = 1 # size
        self.screen_pos = vec2(0, 0) # position relative to screen

    def reset(self, scale_pos = 35) -> vec3:
        angle = r.uniform(0, 2*math.pi)
        radius = r.randrange(HEIGHT // radius_scale, HEIGHT // (4 - 0.065 * radius_scale)) * scale_pos
        x = radius * math.sin(angle)
        y = radius * math.cos(angle)
        self.color = COLORS[color_choice]()
        return vec3(x, y, z_distance) # send new coordinates

    def update(self):
        self.pos3d.z -= self.vel # move along z-axis
        self.pos3d = self.reset() if self.pos3d.z < 1 else self.pos3d # reset if off screen

        self.screen_pos = vec2(self.pos3d.x, self.pos3d.y) / self.pos3d.z + CENTER
        self.screen_pos += vec2(radius_x, radius_y)
        self.size = (z_distance - self.pos3d.z) / (size_scale * self.pos3d.z) # change size based on z-axis position
        self.pos3d.xy = self.pos3d.xy.rotate(ang_spd) # rotate xy
        mouse_pos = CENTER - vec2(pg.mouse.get_pos()) # move screen based on mouse position
        self.screen_pos += mouse_pos

    def draw(self):
        if shape == 0:
            pg.draw.rect(self.screen, self.color, (*self.screen_pos, self.size, self.size))
        elif shape == 1:
            pg.draw.circle(self.screen, self.color, self.screen_pos, self.size)

    def set_spd(self):
        self.vel = r.uniform(spd, VELOCITY(spd))

class Starfield:
    def __init__(self, app):
        self.stars = [Star(app) for _ in range(NUM_STARS)]

    def run(self):
        [star.update() for star in self.stars]
        self.stars.sort(key=lambda star: star.pos3d.z, reverse = True) # painter's algo
        [star.draw() for star in self.stars]
    
    def change_spd(self):
        [star.set_spd() for star in self.stars]

class App:
    def __init__(self):
        self.screen = pg.display.set_mode(RES)
        self.alpha_surface = pg.Surface(RES)
        self.alpha_surface.set_alpha(alpha)
        pg.display.set_caption('Wormhole')
        self.clock = pg.time.Clock()
        self.starfield = Starfield(self)
    
    async def run(self):
        while True:
            global alpha, z_distance, spd, ang_spd, size_scale, radius_scale, color_choice, shape, radius_x, radius_y
            self.screen.blit(self.alpha_surface, (0,0))
            self.clock.tick(60) # 60 fps
            self.starfield.run()

            #[sys.exit() for e in pg.event.get() if e.type == pg.QUIT] # exit
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit(); sys.exit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_r: # r -> change color
                        color_choice = (color_choice + 1) if (color_choice < 3) else 0
                    if event.key == pg.K_t: # t -> change shape
                        shape = (shape + 1) if (shape < 1) else 0
                    if event.key == pg.K_SPACE: # space -> starfield setting
                        z_distance = 40
                        alpha = 120
                        size_scale = shape = 1
                        radius_scale = 35
                        spd = 0.05
                        ang_spd = 0.2
                        radius_x = radius_y = color_choice = 0
                        self.starfield = Starfield(self)
                        self.alpha_surface.set_alpha(alpha)
                    if event.key == pg.K_RETURN: # return -> wormhole setting
                        z_distance = 140
                        alpha = 30
                        size_scale = 0.2
                        radius_scale = 4
                        spd = 0.45
                        ang_spd = color_choice = 0
                        shape = 1
                        radius_x = radius_y = 0
                        self.starfield = Starfield(self)
                        self.alpha_surface.set_alpha(alpha)
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
                z_distance = (z_distance - 1) if (z_distance > 1) else 1
            if pressed[pg.K_a]: # a -> rotate left speedup
                ang_spd += 0.01
            if pressed[pg.K_d]: # d -> rotate right speedup
                ang_spd -= 0.01
            if pressed[pg.K_w]: # w -> accelerate
                spd = (spd + 0.001) if (spd < 3) else 3
                self.starfield.change_spd()
            if pressed[pg.K_s]: # s -> decelerate
                spd = (spd - 0.001) if (spd > -0.02) else -0.02
                self.starfield.change_spd()
            if pressed[pg.K_c]: # c -> size gets larger
                size_scale = (size_scale - 0.01) if (size_scale > 0.01) else size_scale
            if pressed[pg.K_v]: # v -> size gets smaller
                size_scale = (size_scale + 0.01) if (size_scale < z_distance) else z_distance
            if pressed[pg.K_e]: # e -> radius moves right
                radius_x = (radius_x + 1) if (radius_x < WIDTH//2) else WIDTH//2
            if pressed[pg.K_q]: # q -> radius moves left
                radius_x = (radius_x - 1) if (radius_x > -WIDTH//2) else -WIDTH//2
            if pressed[pg.K_y]: # y -> radius moves right
                radius_y = (radius_y - 1) if (radius_y > -HEIGHT//2) else -HEIGHT//2
            if pressed[pg.K_h]: # h -> radius moves left
                radius_y = (radius_y + 1) if (radius_y < HEIGHT//2) else HEIGHT//2
            '''if pressed[pg.K_b]: # b -> radius gets larger
                print(radius_scale)
                radius_scale = (radius_scale - 1) if (radius_scale > 2) else 2
                print(radius_scale)
            if pressed[pg.K_h]: # h -> radius gets larger
                print(radius_scale)
                radius_scale = (radius_scale + 1) if (radius_scale < HEIGHT-1) else HEIGHT-1
                print(radius_scale)'''

            pg.display.flip()
            await a.sleep(0)

if __name__ == '__main__':
    app = App()
    a.run(app.run())