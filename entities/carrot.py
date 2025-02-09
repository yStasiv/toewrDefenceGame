import pygame
from config.assets import CARROT_IMAGE,  SCALE_FACTOR

class Carrot:
    def __init__(self, position):
        self.position = list(position)
        self.size = 15 * SCALE_FACTOR
        self.collected = False
        self.image = CARROT_IMAGE
        
    def draw(self, screen):
        image_rect = self.image.get_rect(center=self.position)
        screen.blit(self.image, image_rect) 