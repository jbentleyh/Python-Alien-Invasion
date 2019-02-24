import pygame
from pygame.sprite import Sprite
import game_functions as gf
from settings import Settings


class Bullet(Sprite):

    def __init__(self, ai_settings, screen, ship):
        # create a bullet object at the ship's current position
        super(Bullet, self).__init__()
        self.screen = screen

        # create a bullet at (0, 0) and then set the correct position
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width,
                                ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # store the bullet position as a decimal
        self.y = float(self.rect.y)

        # set the color and speed of the bullet
        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self, ai_settings, screen, ship, bullets, aliens):
        # update the decimal position of the bullet
        self.y -= self.speed_factor
        # update the rect position
        self.rect.y = self.y


    def draw_bullets(self):
        # draw the bullet to the screen
        pygame.draw.rect(self.screen, self.color, self.rect)



