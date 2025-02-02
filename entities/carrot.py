import pygame
import random
from config import ORANGE, SCALE_FACTOR

class Carrot:
    def __init__(self, position):
        self.position = list(position)
        self.size = 15 * SCALE_FACTOR
        self.collected = False
        
    def draw(self, screen):
        # Малюємо морквину (спрощено як помаранчевий трикутник)
        points = [
            (self.position[0], self.position[1] - self.size),
            (self.position[0] - self.size/2, self.position[1] + self.size/2),
            (self.position[0] + self.size/2, self.position[1] + self.size/2)
        ]
        pygame.draw.polygon(screen, ORANGE, points) 