'''
Space Wars is a take on the old classic game space invaders.
'''

# Imports
import random
import pygame

# Initialize game engine
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()


# Window
WIDTH = 1280
HEIGHT = 720
SIZE = (WIDTH, HEIGHT)
TITLE = "Battle of Britain"
SCREEN = pygame.display.set_mode(SIZE)
pygame.display.set_caption(TITLE)


# Timer
CLOCK = pygame.time.Clock()
REFRESH_RATE = 60

# Colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (100, 255, 100)


# Fonts
FONT_SM = pygame.font.Font(None, 24)
FONT_MD = pygame.font.Font(None, 32)
FONT_LG = pygame.font.Font(None, 64)
FONT_XL = pygame.font.Font("assets/fonts/spacerangerboldital.ttf", 96)


# Images
SHIP_IMG = pygame.image.load('assets/images/spitfire.png').convert_alpha()
LASER_IMG = pygame.image.load('assets/images/laserRed.png').convert_alpha()
ENEMY_IMG = pygame.image.load('assets/images/messerschmitt-bf-109-a1.png').convert_alpha()
BOMB_IMG = pygame.image.load('assets/images/laserGreen.png').convert_alpha()
EXPLOSION = pygame.image.load('assets/images/explosion.png').convert()
BACKGROUND_IMG = pygame.image.load('assets/images/Background/ocean.jpg').convert()
FIREBALL_IMG = pygame.image.load('assets/images/fireball-effect.png').convert_alpha()


# Sounds
EXPLOSION_SOUND = pygame.mixer.Sound('assets/sounds/explosion_sound.ogg')
SHOOT_SOUND = pygame.mixer.Sound('assets/sounds/shoot.wav')
A_10_SOUND = pygame.mixer.Sound('assets/sounds/A-10 sound.ogg')


# Gloabl Varables
PLAYER = 0
LASERS = 0
MOBS = 0
FLEET = 0
BOMBS = 0
SHIP = 0
FIREBALL = 0

# Stages
START = 0
PLAYING = 1
END = 2


# Game classes
class Ship(pygame.sprite.Sprite):
    '''
    This is the class of the ship. It will
    handle movement, decteding weather it was shhot. and updating.
    '''
    def __init__(self, ship_x, ship_y, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = ship_x
        self.rect.y = ship_y

        self.heath = 100
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

        laser = Laser(LASER_IMG)
        laser.rect.centerx = self.rect.centerx
        laser.rect.centery = self.rect.top
        LASERS.add(laser)
        # SHOOT_SOUND.play()

    def update(self):
        '''
        this will up date the ship.
            See if it has hit walls
        '''

        if self.rect.left < 0:
            self.rect.left = 0

        elif self.rect.right > WIDTH:
            self.rect.right = WIDTH

        hit_list = pygame.sprite.spritecollide(self, BOMBS, True, pygame.sprite.collide_mask)
        if hit_list:
            print('Outch')
            self.heath -= 10

        hit_list = pygame.sprite.spritecollide(self, FIREBALL, True, pygame.sprite.collide_mask)
        if hit_list:
            print('Afterkill!')
            self.heath -= 20

        if self.heath <= 0:
            print("you died.")
            self.kill()
            STAGE = END

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
        bomb = Bomb(BOMB_IMG)
        bomb.rect.centerx = self.rect.centerx
        bomb.rect.centery = self.rect.bottom
        BOMBS.add(bomb)



    def after_death(self):
        '''
        After the enemy plane is shot this is will do what it needs to do after that.
        '''
        fireball = FireBall(FIREBALL_IMG)
        fireball.rect.centerx = self.rect.centerx
        fireball.rect.centery = self.rect.bottom
        FIREBALL.add(fireball)

    def update(self):
        '''
        This will check to see if the mobs have been hit.
        '''
        hit_list = pygame.sprite.spritecollide(self, LASERS, True, pygame.sprite.collide_mask)
        if hit_list:
            self.after_death()
            self.kill()

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
        if self.rect.top > HEIGHT:
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
        if self.rect.top > HEIGHT:
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

        for _m in MOBS:
            if self.moving_right:
                _m.rect.x += self.speed
                if _m.rect.right >= WIDTH:
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
        mob_list = MOBS.sprites()

        if mob_list and rand == 0:
            bomber = random.choice(mob_list)
            bomber.drop_bomb()

    def update(self):
        '''
        updates the fleet
        '''
        self.move()
        self.choose_bomber()


# Game helper functions
def show_title_screen():
    '''
    This will show the start screen.
    '''
    title_text = FONT_XL.render("Battle of Britain!", 1, WHITE)
    title_text_width = title_text.get_width()
    title_text_height = title_text.get_height()

    SCREEN.blit(title_text, [(WIDTH/2) - (title_text_width/2), (HEIGHT/2) - (title_text_height/ 2)])


def show_stats():
    '''
    will blit player heath of screen.
    '''
    _hp = FONT_MD.render(str(SHIP.heath), 1, WHITE)

    SCREEN.blit(_hp, [0, 0])




def setup():
    '''
    this sets up the whole thing.
    '''
    global STAGE, DONE
    global PLAYER, SHIP, LASERS, MOBS, FLEET, BOMBS, FIREBALL

    # ''' Make game objects '''
    rect = SHIP_IMG.get_rect()
    rect_x = rect.centerx
    rect_y = rect.bottom
    SHIP = Ship(WIDTH/2-rect_x, HEIGHT-rect_y, SHIP_IMG)

    # ''' Make sprite groups '''
    PLAYER = pygame.sprite.GroupSingle()
    PLAYER.add(SHIP)

    LASERS = pygame.sprite.Group()
    BOMBS = pygame.sprite.Group()
    FIREBALL = pygame.sprite.Group()

    mob1 = Mob(100, 100, ENEMY_IMG)
    mob2 = Mob(300, 100, ENEMY_IMG)
    mob3 = Mob(500, 100, ENEMY_IMG)

    MOBS = pygame.sprite.Group()
    MOBS.add(mob1, mob2, mob3)

    FLEET = Fleet(MOBS)

    # ''' set stage '''
    STAGE = START
    DONE = False



# Game loop
setup()

while not DONE:
    # Input handling (React to key presses, mouse clicks, etc.)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            DONE = True
        elif event.type == pygame.KEYDOWN:
            if STAGE == START:
                if event.key == pygame.K_SPACE:
                    STAGE = PLAYING

            elif STAGE == PLAYING:
                if event.key == pygame.K_w:
                    SHIP.shoot()

    # ''' poll key states '''
    STATE = pygame.key.get_pressed()
    A = STATE[pygame.K_a]
    S = STATE[pygame.K_s]
    D = STATE[pygame.K_d]

    if STAGE == PLAYING:
        if A:
            SHIP.move_left()
        elif D:
            SHIP.move_right()

        if S:
            SHIP.shoot()
            A_10_SOUND.play()

    # Game logic (Check for collisions, update points, etc.)
    if STAGE == PLAYING:
        PLAYER.update()
        LASERS.update()
        BOMBS.update()
        FLEET.update()
        MOBS.update()
        FIREBALL.update()


    # Drawing code (Describe the picture. It isn't actually drawn yet.)
    if STAGE == START:
        show_title_screen()
    elif STAGE == PLAYING:
        SCREEN.fill(BLACK)
        SCREEN.blit(BACKGROUND_IMG, (0, 0))
        LASERS.draw(SCREEN)
        BOMBS.draw(SCREEN)
        PLAYER.draw(SCREEN)
        MOBS.draw(SCREEN)
        FIREBALL.draw(SCREEN)
        show_stats()

    # Update screen (Actually draw the picture in the window.)
    pygame.display.flip()


    # Limit refresh rate of game loop
    CLOCK.tick(REFRESH_RATE)


# Close window and quit
pygame.quit()