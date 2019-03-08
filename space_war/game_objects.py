'''
This file will contain all the game objects (classes). To make main file easer to read.
'''
# pylint: disable=import-error
import random
import pygame
import settings

class Ship(pygame.sprite.Sprite):
    '''
    This is the class of the ship. It will
    handle movement, decteding weather it was shhot. and updating.
    '''
    def __init__(self, ship_x, ship_y, image,):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = ship_x
        self.rect.y = ship_y

        self.heath = settings.SHIP_MAX_HEALTH
        self.speed = 3

    def move_left(self):
        '''
        moves space ship left
        '''
        self.rect.x -= self.speed

    def move_right(self):
        '''
        moves space ship right
        '''
        self.rect.x += self.speed

    def shoot(self):
        '''
        this will start the process of a laser being shot from the ship.
        '''

        laser = Laser(settings.LASER_IMG)
        laser.rect.centerx = self.rect.centerx
        laser.rect.centery = self.rect.top
        settings.LASERS.add(laser)


    def update(self):
        '''
        this will up date the ship.
            See if it has hit walls
        '''

        if self.rect.left < 0:
            self.rect.left = 0

        elif self.rect.right > settings.WIDTH:
            self.rect.right = settings.WIDTH

        hit_list = pygame.sprite.spritecollide(self, settings.BOMBS,
                                               True, pygame.sprite.collide_mask)
        if hit_list:
            print('Outch')
            self.heath -= 10


        hit_list = pygame.sprite.spritecollide(self, settings.FIREBALL,
                                               True, pygame.sprite.collide_mask)

        if hit_list:
            self.heath -= 20

        if self.heath <= 0:
            self.kill()


class Laser(pygame.sprite.Sprite):
    '''
    This class will hold all the lasers shot. And will move and kill them.
    '''
    def __init__(self, image):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()

        self.speed = 5

    def update(self):
        '''
        Move the lasers up the screen and will delete them when appoiot
        '''
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()


class Mob(pygame.sprite.Sprite):
    '''
    This class will house all the enemies and update them.
    '''
    def __init__(self, mob_x, mob_y, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = mob_x
        self.rect.y = mob_y


    def drop_bomb(self):
        '''
        This is acctually shoot the enemy lasers
        '''
        bomb = Bomb(settings.BOMB_IMG)
        bomb.rect.centerx = self.rect.centerx
        bomb.rect.centery = self.rect.bottom
        settings.BOMBS.add(bomb)



    def after_death(self):
        '''
        After the enemy plane is shot this is will do what it needs to do after that.
        '''
        fireball = FireBall(settings.FIREBALL_IMG)
        fireball.rect.centerx = self.rect.centerx
        fireball.rect.centery = self.rect.bottom
        settings.FIREBALL.add(fireball)

    def update(self):
        '''
        This will check to see if the mobs have been hit.
        '''
        hit_list = pygame.sprite.spritecollide(self, settings.LASERS,
                                               True, pygame.sprite.collide_mask)
        if hit_list:
            self.after_death()
            self.kill()
            settings.EXPLOSION_SOUND.play()


class Bomb(pygame.sprite.Sprite):
    '''
    This class will hold all the bombs shot. And will move and kill them.
    '''
    def __init__(self, image):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()

        self.speed = 3

    def update(self):
        '''
        Move the lasers up the screen and will delete them when appoiot.
        '''
        self.rect.y += self.speed
        if self.rect.top > settings.HEIGHT:
            self.kill()


class FireBall(pygame.sprite.Sprite):
    '''
    This class will hold all the bombs shot. And will move and kill them.
    '''
    def __init__(self, image):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()

        self.speed = 6

    def update(self):
        '''
        Move the lasers up the screen and will delete them when appoiot.
        '''
        self.rect.y += self.speed
        if self.rect.top > settings.HEIGHT:
            self.kill()


class Fleet():
    '''
    This is a class of the mobs where it will process their movement.
    '''
    def __init__(self, mobes):
        self.mobs = mobes
        self.speed = 3
        self.moving_right = True
        self.drop_speed = 5
        self.bomb_rate = 60
    def move(self):
        '''
        This function will move the fleet.
        '''
        hits_edge = False

        for _m in settings.MOBS:
            if self.moving_right:
                _m.rect.x += self.speed
                if _m.rect.right >= settings.WIDTH:
                    hits_edge = True

            else:
                _m.rect.x -= self.speed
                if _m.rect.left <= 0:
                    hits_edge = True

        if hits_edge:
            self.reverse()
            self.move_down()

    def reverse(self):
        '''
        IDK WHY THIS HAS TO BE A FUNCTION
        '''
        self.moving_right = not self.moving_right

    def move_down(self):
        '''
        This runs through all the mobs, then moves them down.
        '''
        for mob in self.mobs:
            mob.rect.y += self.drop_speed

    def choose_bomber(self):
        '''
        This will randoly choose which bomber will shoot,
        And how often it will shoot.
        '''
        rand = random.randrange(self.bomb_rate)
        mob_list = settings.MOBS.sprites()

        if mob_list and rand == 0:
            bomber = random.choice(mob_list)
            bomber.drop_bomb()

    def update(self):
        '''
        updates the fleet
        '''
        if settings.STAGE == settings.PLAYING:
            self.move()
            self.choose_bomber()

        elif settings.STAGE == settings.END:
            self.move_down()

        else:
            pass
