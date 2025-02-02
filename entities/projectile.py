import pygame
from config import BLACK, SCALE_FACTOR

class Projectile:
    def __init__(self, start_pos, target_pos, damage, speed=10):
        self.position = list(start_pos)
        self.start_pos = list(start_pos)
        self.target_pos = target_pos
        self.damage = damage
        self.speed = speed * SCALE_FACTOR
        self.size = 5 * SCALE_FACTOR
        
    def move(self):
        dx = self.target_pos[0] - self.position[0]
        dy = self.target_pos[1] - self.position[1]
        distance = (dx**2 + dy**2)**0.5
        
        if distance < self.speed:
            return True
        
        self.position[0] += (dx/distance) * self.speed
        self.position[1] += (dy/distance) * self.speed
        return False
        
    def draw(self, screen):
        pygame.draw.circle(screen, BLACK, 
                         (int(self.position[0]), int(self.position[1])), 
                         int(self.size)) 