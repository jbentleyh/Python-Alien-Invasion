import pygame
import game_functions as gf
from settings import Settings
from ship import Ship
from pygame.sprite import Group
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

pygame.init()


def run_game():
    # initialize settings and the screen
    ai_settings = Settings()

    # set window res
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))

    # name the game window
    pygame.display.set_caption("Rocket Blaster")

    # make a play button
    play_button = Button(ai_settings, screen, "Play")

    # create an instance of the game stats and scoreboard
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    # make the ship
    ship = Ship(ai_settings, screen)

    # make a group of bullets to store in and group of aliens for fleet
    bullets = Group()
    aliens = Group()

    # create the fleet of aliens
    gf.create_fleet(ai_settings, screen, ship, aliens)

    while True:
        # check for occurring events
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets)

        if stats.game_active:
            # events have been found and are being updated
            ship.update()

            # update bullets
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)

            # update aliens
            gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets)

        # draw new screen
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button)

        # if you lose all 3 lives, end the game
        if stats.ships_left == 0:
            break


run_game()

print("Game over!!")