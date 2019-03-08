'''
This will house the game loop
'''
# pylint: disable=import-error
import settings
import pygame

# Game helper functions
def show_title_screen():
    '''
    This will show the start screen.
    '''
    settings.SCREEN.fill(settings.BLACK)
    title_text = settings.FONT_XL.render("Battle of Britain!", 1, settings.WHITE)
    title_text_width = title_text.get_width()
    title_text_height = title_text.get_height()

    settings.SCREEN.blit(title_text, [(settings.WIDTH/2) - (title_text_width/2),
                                      (settings.HEIGHT/2) - (title_text_height/ 2)])

def show_end_screen():
    '''
    This will show the end screen.
    '''
    # settings.SCREEN.fill(settings.BLACK)
    title_text = settings.FONT_XL.render("GAME OVER!!!!", 1, settings.WHITE)
    title_text_width = title_text.get_width()
    title_text_height = title_text.get_height()

    for _m in settings.MOBS:
        settings.SCREEN.blit(title_text, [(settings.WIDTH/2) - (title_text_width/2),
                                          _m.rect.y -settings.HEIGHT - title_text_height])


def show_stats():
    '''
    will blit player heath of screen.
    '''
    _hp = settings.FONT_MD.render(str(settings.SHIP.heath), 1, settings.WHITE)

    settings.SCREEN.blit(_hp, [0, 0])

def draw_hp():
    '''
    Draws the hp bar.
    '''
    hp_inner_rect = [7, settings.HEIGHT - 50, (settings.SHIP.heath/
                                               settings.SHIP_MAX_HEALTH) * 100, 25]
    pygame.draw.rect(settings.SCREEN, settings.GREEN, hp_inner_rect, 0)

    hp_outter_rect = [4, settings.HEIGHT - 53, 103, 28]
    pygame.draw.rect(settings.SCREEN, settings.BLACK, hp_outter_rect, 5)



def draw_stage_playing():
    '''
    This is all the code that will draw, blit, or fill.
    During the playing portion of the game.
    '''
    settings.SCREEN.fill(settings.BLACK)
    settings.SCREEN.blit(settings.BACKGROUND_IMG, (0, 0))
    settings.LASERS.draw(settings.SCREEN)
    settings.BOMBS.draw(settings.SCREEN)
    settings.PLAYER.draw(settings.SCREEN)
    settings.MOBS.draw(settings.SCREEN)
    settings.FIREBALL.draw(settings.SCREEN)
    draw_hp()
    show_stats()


def game_logic():
    '''
    This is all the code that will update the classes.
    During the playing portion of the game.
    '''
    if settings.STAGE == settings.PLAYING:
        settings.PLAYER.update()
        settings.LASERS.update()
        settings.BOMBS.update()
        settings.FLEET.update()
        settings.MOBS.update()
        settings.FIREBALL.update()

    elif settings.STAGE == settings.END:
        settings.LASERS.update()
        settings.BOMBS.update()
        settings.FLEET.update()
        settings.FIREBALL.update()

    if settings.SHIP.heath <= 0 or settings.MOBS == 0:
        settings.STAGE = settings.END




def ship_movement(_a, _d):
    '''
    Logic for moving the ship.
    During the playing portion of the game.
    '''
    if _a:
        settings.SHIP.move_left()
    elif _d:
        settings.SHIP.move_right()
    else:
        pass


def continuous_shooting(_s):
    '''
    Holding S will fire a continuous stream of bulletts.
    '''
    if _s:
        settings.SHIP.shoot()
        settings.A_10_SOUND.play()


def game_loop():
    '''
    This is the game loop
    '''
    while not settings.DONE:
        # Input handling (React to key presses, mouse clicks, etc.)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                settings.DONE = True
            elif event.type == pygame.KEYDOWN:
                if settings.STAGE == settings.START:
                    if event.key == pygame.K_SPACE:
                        settings.STAGE = settings.PLAYING

                elif settings.STAGE == settings.PLAYING:
                    if event.key == pygame.K_w:
                        settings.SHIP.shoot()
                    elif event.key == pygame.K_w:
                        settings.STAGE = settings.END

        # ''' poll key states '''
        _state = pygame.key.get_pressed()
        _a = _state[pygame.K_a]
        _s = _state[pygame.K_s]
        _d = _state[pygame.K_d]

        if settings.STAGE == settings.PLAYING:
            ship_movement(_a, _d)
            continuous_shooting(_s)
        elif settings.STAGE == settings.END:
            settings.FLEET.update()

        # Game logic (Check for collisions, update points, etc.)
        game_logic()

        # Drawing code (Describe the picture. It isn't actually drawn yet.)
        draw_stage_playing()

        if settings.STAGE == settings.START:
            show_title_screen()

        elif settings.STAGE == settings.END:
            show_end_screen()



        # Update screen (Actually draw the picture in the window.)
        pygame.display.flip()


        # Limit refresh rate of game loop
        settings.CLOCK.tick(settings.REFRESH_RATE)
