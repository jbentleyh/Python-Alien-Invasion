import pygame
from pygame.sprite import Sprite

class Ship(Sprite):

    # initialize ship and its starting location on screen
    def __init__(self, ai_settings, screen):

        super(Ship, self).__init__()

        self.screen = screen
        self.ai_settings = ai_settings

        # load image of ship and its rect
        self.image = pygame.image.load('images/rocket.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # start each ship at the bottom of the screen
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # store the decimal value of the ship's center
        self.center = float(self.rect.centerx)

        # movement flag
        self.moving_right = False
        self.moving_left = False

    def update(self):
        # update the ship's position base on the flag
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor

        # update the ship from the self.center point
        self.rect.centerx = self.center

    def blitme(self):
        # draw the ship at the current coordinates
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        self.center = self.screen_rect.centerx
