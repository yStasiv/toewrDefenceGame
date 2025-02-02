import pygame
from config import YELLOW, BLACK, SCALE_FACTOR

class Coin:
    def __init__(self, position, value=10):
        self.position = list(position)
        self.value = value
        self.size = 15 * SCALE_FACTOR
        self.collected = False
        
    def draw(self, screen):
        pygame.draw.circle(screen, YELLOW, 
                         (int(self.position[0]), int(self.position[1])), 
                         int(self.size))
        value_text = pygame.font.Font(None, int(20 * SCALE_FACTOR)).render(str(self.value), True, BLACK)
        value_rect = value_text.get_rect(center=self.position)
        screen.blit(value_text, value_rect) 