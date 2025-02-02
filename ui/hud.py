import pygame
from config import BLACK, GRAY, SCALE_FACTOR, SCREEN_WIDTH, screen

class HUD:
    def __init__(self):
        self.font = pygame.font.Font(None, int(36 * SCALE_FACTOR))
        self.top_ui_height = 40 * SCALE_FACTOR
        
    def draw_top_ui(self, game_state):
        pygame.draw.rect(screen, GRAY, (0, 0, SCREEN_WIDTH, self.top_ui_height))
        
        # Здоров'я замку
        castle_text = self.font.render(
            f'Замок: {int(game_state.castle_health)}/{game_state.castle_max_health}', 
            True, BLACK
        )
        screen.blit(castle_text, (10, 5))
        
        # Час
        time_text = self.font.render(f'Час: {int(game_state.game_time)}с', True, BLACK)
        screen.blit(time_text, (200 * SCALE_FACTOR, 5))
        
        # Гроші
        money_text = self.font.render(f'Гроші: {game_state.money}', True, BLACK)
        screen.blit(money_text, (400 * SCALE_FACTOR, 5))
        
        # Рівень
        level_text = self.font.render(f'Рівень: {game_state.level}', True, BLACK)
        screen.blit(level_text, (600 * SCALE_FACTOR, 5))
        
        # Залишилось ворогів
        remaining = game_state.enemies_per_level - game_state.enemies_spawned
        enemies_text = self.font.render(f'Залишилось: {remaining}', True, BLACK)
        screen.blit(enemies_text, (800 * SCALE_FACTOR, 5)) 