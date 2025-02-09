import pygame
from config import YELLOW, BLACK, SCALE_FACTOR
from config.assets import UI_IMAGES, COIN_IMAGES

class Coin:
    def __init__(self, position, value):
        self.position = list(position)
        self.value = value
        self.size = 15 * SCALE_FACTOR
        # Вибираємо зображення в залежності від номіналу
        if 10 >= value:
            self.image = COIN_IMAGES['10']
        elif 15 >=value:
            self.image = COIN_IMAGES['15']
        elif 25 >= value:
            self.image = COIN_IMAGES['25']
        else:
            self.image = COIN_IMAGES['100']
        self.collected = False
        
    def draw(self, screen):
        image_rect = self.image.get_rect(center=self.position)
        screen.blit(self.image, image_rect)
        
        # value_text = pygame.font.Font(None, int(20 * SCALE_FACTOR)).render(str(self.value), True, BLACK)
        # value_rect = value_text.get_rect(center=self.position)
        # screen.blit(value_text, value_rect) 
