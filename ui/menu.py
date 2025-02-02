import pygame
from config import WHITE, BLACK, BLUE, LIGHT_BLUE, SCALE_FACTOR, SCREEN_WIDTH, SCREEN_HEIGHT
from config.sounds import toggle_sound, get_sound_state
from config.assets import UI_IMAGES  # Додайте відповідну іконку звуку в assets

class Menu:
    def __init__(self):
        self.font = pygame.font.Font(None, int(74 * SCALE_FACTOR))
        self.small_font = pygame.font.Font(None, int(48 * SCALE_FACTOR))
        self.buttons = [
            {'text': 'Почати гру', 'action': 'start'},
            {'text': 'Налаштування', 'action': 'settings'},
            {'text': 'Вихід', 'action': 'quit'}
        ]
        self.button_height = 80 * SCALE_FACTOR
        self.button_width = 400 * SCALE_FACTOR
        self.padding = 20 * SCALE_FACTOR
        
        # Завантажуємо рекорд
        try:
            with open('record.txt', 'r') as f:
                self.record_level = int(f.read())
        except:
            self.record_level = 1
        
        # Додаємо кнопку звуку
        self.sound_button = pygame.Rect(
            SCREEN_WIDTH - 60 * SCALE_FACTOR,
            10,
            50 * SCALE_FACTOR,
            50 * SCALE_FACTOR
        )
        
        # Завантажуємо зображення для кнопки звуку
        self.sound_enabled = get_sound_state()
        
    def draw(self, screen):
        screen.fill(WHITE)
        
        # Малюємо заголовок
        title = self.font.render('Tower Defense', True, BLACK)
        title_rect = title.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT * 0.2))
        screen.blit(title, title_rect)
        
        # Малюємо рекорд
        record_text = self.small_font.render(f'Рекорд: {self.record_level} рівень', True, BLUE)
        record_rect = record_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT * 0.3))
        screen.blit(record_text, record_rect)

        # Малюємо кнопки
        mouse_pos = pygame.mouse.get_pos()
        
        for i, button in enumerate(self.buttons):
            button_y = SCREEN_HEIGHT * 0.4 + (self.button_height + self.padding) * i
            button_rect = pygame.Rect(
                (SCREEN_WIDTH - self.button_width) / 2,
                button_y,
                self.button_width,
                self.button_height
            )
            
            # Перевіряємо, чи миша наведена на кнопку
            if button_rect.collidepoint(mouse_pos):
                color = LIGHT_BLUE
            else:
                color = BLUE
                
            pygame.draw.rect(screen, color, button_rect, border_radius=int(15 * SCALE_FACTOR))
            
            # Текст кнопки
            text = self.font.render(button['text'], True, WHITE)
            text_rect = text.get_rect(center=button_rect.center)
            screen.blit(text, text_rect)
            
        # Малюємо кнопку звуку
        if self.sound_enabled:
            screen.blit(UI_IMAGES['sound_on'], self.sound_button)
        else:
            screen.blit(UI_IMAGES['sound_off'], self.sound_button)
        
    def handle_click(self, pos):
        for i, button in enumerate(self.buttons):
            button_y = SCREEN_HEIGHT * 0.4 + (self.button_height + self.padding) * i
            button_rect = pygame.Rect(
                (SCREEN_WIDTH - self.button_width) / 2,
                button_y,
                self.button_width,
                self.button_height
            )
            
            if button_rect.collidepoint(pos):
                return button['action']
        
        # Перевіряємо клік по кнопці звуку
        if self.sound_button.collidepoint(pos):
            self.sound_enabled = toggle_sound()
            return 'sound_toggle'
        
        return None 