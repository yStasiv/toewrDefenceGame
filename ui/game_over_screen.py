import pygame
from config import WHITE, RED, BLACK, BLUE, SCALE_FACTOR, SCREEN_WIDTH, SCREEN_HEIGHT, screen

class GameOverScreen:
    def __init__(self):
        self.title_font = pygame.font.Font(None, int(100 * SCALE_FACTOR))
        self.stats_font = pygame.font.Font(None, int(50 * SCALE_FACTOR))
        
    def draw(self, level, kills, money):
        screen.fill(WHITE)
        
        # Малюємо заголовок
        title_text = self.title_font.render('Гра Завершена!', True, RED)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT * 0.2))
        screen.blit(title_text, title_rect)
        
        # Малюємо статистику
        stats = [
            f'Досягнутий рівень: {level}',
            f'Знищено ворогів: {kills}',
            f'Зароблено золота: {money}'
        ]
        
        for i, stat in enumerate(stats):
            text = self.stats_font.render(stat, True, BLACK)
            rect = text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT * (0.4 + i * 0.1)))
            screen.blit(text, rect)
        
        # Кнопка повернення в меню
        button_width = 400 * SCALE_FACTOR
        button_height = 80 * SCALE_FACTOR
        menu_button = pygame.Rect(
            (SCREEN_WIDTH - button_width) / 2,
            SCREEN_HEIGHT * 0.8,
            button_width,
            button_height
        )
        
        pygame.draw.rect(screen, BLUE, menu_button, border_radius=int(15 * SCALE_FACTOR))
        button_text = self.stats_font.render('До головного меню', True, WHITE)
        text_rect = button_text.get_rect(center=menu_button.center)
        screen.blit(button_text, text_rect)
        
        return menu_button 