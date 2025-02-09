import pygame
from config.assets import PROJECTILE_IMAGES, SCALE_FACTOR

class Projectile:
    def __init__(self, start_pos, target_pos, damage, speed=10, projectile_type='normal'):
        self.position = list(start_pos)
        self.start_pos = list(start_pos)
        self.target_pos = target_pos
        self.damage = damage
        self.speed = speed * SCALE_FACTOR
        self.size = 5 * SCALE_FACTOR        
        # Вибираємо зображення в залежності від типу снаряду
        self.image = PROJECTILE_IMAGES.get(projectile_type, PROJECTILE_IMAGES['normal'])  # TODO: переробити, щоб залежало від вежі
        
        # Розрахунок напрямку руху
        dx = target_pos[0] - start_pos[0]
        dy = target_pos[1] - start_pos[1]
        distance = (dx**2 + dy**2)**0.5
        self.dx = (dx/distance) * self.speed if distance > 0 else 0
        self.dy = (dy/distance) * self.speed if distance > 0 else 0
        
    def move(self, target_pos=None):
        if target_pos:  # Оновлюємо позицію цілі, якщо вона передана
            self.target_pos = target_pos
            
        # Розрахунок напрямку руху до поточної позиції цілі
        dx = self.target_pos[0] - self.position[0]
        dy = self.target_pos[1] - self.position[1]
        distance = (dx**2 + dy**2)**0.5
        
        if distance > 0:
            self.position[0] += (dx/distance) * self.speed
            self.position[1] += (dy/distance) * self.speed
            
        # Перевіряємо чи не пролетів снаряд занадто далеко
        return ((self.position[0] - self.start_pos[0])**2 + 
                (self.position[1] - self.start_pos[1])**2)**0.5 > 800
        
    def draw(self, screen):
        image_rect = self.image.get_rect(center=self.position)
        screen.blit(self.image, image_rect) 