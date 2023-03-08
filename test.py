import pygame as pg
from scengine.loader import ResourceLoader

pg.init()

window = pg.display.set_mode((720, 480))
display = pg.surface.Surface((window.get_size()[0] / 4, window.get_size()[1] / 4))

sprites = ResourceLoader("./test_game/resources").load_sprites()

sprite: pg.surface.Surface = sprites["stone"]

sprite_array = pg.surfarray.array3d(sprite)

print(sprite_array)

sprite = pg.surfarray.make_surface(sprite_array)

run = True
while run:

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

    display.fill((0, 0, 0))
    display.blit(sprite, (0, 0))
    display.blit(sprites["stone"], (20, 0))

    window.blit(pg.transform.scale(display, window.get_size()), (0, 0))

    pg.display.flip()
