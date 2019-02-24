import pygame
from pygame.sprite import Sprite


class Alien(Sprite):

    def __init__(self, ai_settings, screen):
        # initialize alien and set its position
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # load in the alien image
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # starts each alien at the top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # store exact position
        self.x = float(self.rect.x)

    def blitme(self):
        # draw the alien at its current position
        self.screen.blit(self.image, self.rect)

    def update(self):
        # move the alien to the right
        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = self.x

    def check_edges(self):
        # returns TRUE value if the alien is at the edge of the screen
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True
