'''
Space Wars is a take on the old classic game space invaders.
'''
# pylint: disable=import-error

# Imports
import pygame
import settings
import game_objects
import game_loop


# Initialize game engine
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()
settings.init()


def setup():
    '''
    this sets up the whole thing.
    '''
    # ''' add ship to player sprite groupe '''
    settings.PLAYER.add(settings.SHIP)

    mob_x_scale = 200
    mob_y_scale = 100

    for _x in range(100, settings.WIDTH-100, mob_x_scale):
        for _y in range(100, 300, mob_y_scale):
            settings.MOBS.add(game_objects.Mob(_x, _y, settings.ENEMY_IMG))

# Game loop
setup()
game_loop.game_loop()

# Close window and quit
pygame.quit()
