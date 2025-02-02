class GameState:
    def __init__(self):
        self.money = 1000
        self.level = 1
        self.castle_health = 100
        self.castle_max_health = 100
        self.enemies_killed = 0
        self.enemies_spawned = 0
        self.enemies_per_level = 10
        self.game_time = 0
        self.total_enemies_killed = 0
        self.total_money_earned = 0 