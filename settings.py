class Settings():
    # This class stores all necessary settings for the game to work as intended

    def __init__(self):
        # initialize the game settings
        self.screen_width = 830
        self.screen_height = 720
        self.bg_color = (255, 255, 255)

        # Ship settings
        self.ship_speed_factor = 1.5
        self.ship_limit = 3

        # bullet settings
        self.bullet_speed_factor = 1
        self.bullet_width = 3
        self.bullet_height = 20
        self.bullet_color = 60, 60, 60

        # Alien settings
        self.alien_speed_factor = 1
        self.alien_drop_speed = 10
        # fleet direction 1 means RIGHT, -1 means LEFT
        self.fleet_direction = 1

        # how fast the game speeds up
        self.speedup_scale = 1.1
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        # initialize settings that will change throughout the game
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1

        # fleet initial direction
        self.fleet_direction = 1

        # scoring
        self.alien_points = 50

    def increase_speed(self):
        # increase all speeds
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        # adds score multiplier!
        self.alien_points = int(self.alien_points * self.score_scale)