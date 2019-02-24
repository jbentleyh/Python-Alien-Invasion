class GameStats():
    # track all the statistics for the game
    def __init__(self, ai_settings):
        # initialize stats
        self.ai_settings = ai_settings
        self.reset_stats()

        # start the game in an inactive state
        self.game_active = False

        # track the highest score
        self.high_score = 0

    def reset_stats(self):
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1

    def loseLife(self):
        self.ships_left -= 1
