import sys
import pygame
from time import sleep
from bullet import Bullet
from alien import Alien
from settings import Settings
from pygame.sprite import Sprite
from ship import Ship
from game_stats import GameStats


def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    # find and respond to event such as movement or mouse events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RIGHT:
            # move right
            ship.moving_right = True
        if event.key == pygame.K_LEFT:
            # move left
            ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            # create new bullet and add it the bullet Group
            new_bullet = Bullet(ai_settings, screen, ship)
            bullets.add(new_bullet)
        elif event.key == pygame.K_q:
            sys.quit()


def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    # start a new game when the player clicks play, also resets stats
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)

    if button_clicked and not stats.game_active:
        # reset the game settings
        ai_settings.initialize_dynamic_settings()

        # hide mouse cursor
        pygame.mouse.set_visible(False)
        stats.reset_stats()
        stats.game_active = True

        # reset the scoring images
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # empty the aliens and bullets before starting
        aliens.empty()
        bullets.empty()

        # create the new fleet and center the ship
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


def check_keyup_events(event, ship):
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_RIGHT:
            ship.moving_right = False
        if event.key == pygame.K_LEFT:
            ship.moving_left = False


def check_fleet_edges(ai_settings, aliens):
    # check edge and act accordingly
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    # drop the fleet and change directions
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.alien_drop_speed

    # makes the direction -1 or 1 to swap the direction
    # (L = -1, R =1)
    ai_settings.fleet_direction *= -1


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    # update the bullet positions
    bullets.update(ai_settings, screen, ship, bullets, aliens)

    # delete bullets that have gone off screen
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)

    if len(aliens) == 0:
        # destroy existing bullets, spawn new fleet, and increase the game speed
        bullets.empty()
        ai_settings.increase_speed()

        # increase the level
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_settings, screen, ship, aliens)


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    # remove any alien and bullets when a collision happens
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        # makes sure all bullets collisions are counted in each loop through
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()

        check_high_scores(stats, sb)


def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets):
    # check if aliens have reached the bottom of the screen
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # treat as if the ship was hit
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
            break

def check_high_scores(stats, sb):
    # check if there's a ne high score
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
    # game acts accordingly when ship gets hit by an aliens
    if stats.ships_left > 0:
        # subtract 1 life
        stats.loseLife()

        # update the scoreboard
        sb.prep_ships()

        # empty the aliens and bullets
        aliens.empty()
        bullets.empty()

        # create a new fleet and center the ship
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # pause
        sleep(0.5)

    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    screen.fill(ai_settings.bg_color)

    # re_draw the bullets behind ship and aliens
    for bullet in bullets.sprites():
        bullet.draw_bullets()
    # update the images on the screen during each loop pass
    ship.blitme()
    aliens.draw(screen)

    # draw the current score
    sb.show_score()

    # draw the play button if the game is inactive
    if not stats.game_active:
        play_button.draw_button()

    # update the frame
    pygame.display.update()


def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets):
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # check for alien and bullet collision
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
        print("Ship hit!!")

    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)


def get_number_rows(ai_settings, ship_height, alien_height):
    # find number of rows of aliens can possibly fit
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def get_number_aliens_x(ai_settings, alien_width):
    # calc how many aliens can fit on a row
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def create_fleet(ai_settings, screen, ship, aliens):
    # calc number of aliens can fit on screen, alien width worth of space between each alien
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    # create fleet of aliens
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    # create alien and place it on the row
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)
