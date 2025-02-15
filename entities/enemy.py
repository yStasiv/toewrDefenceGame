import pygame
from config import GREEN, RED, SCALE_FACTOR
from config.assets import ENEMY_IMAGES

class Enemy:
    # Типи ворогів та їх характеристики
    ENEMY_TYPES = {
    'enemy_lvl_1': {  'health': 50,   'speed': 2,   'size': 30,  'reward': 10,   'weakness': 'fire',     },
    'enemy_lvl_2': {  'health': 100,  'speed': 1.5, 'size': 35,  'reward': 15,   'weakness': 'ice',      },
    'enemy_lvl_3': {  'health': 75,  'speed': 2.5, 'size': 32,  'reward': 10,   'weakness': 'electric', },
    'enemy_lvl_4': {  'health': 50,  'speed': 6,   'size': 40,  'reward': 25,   'weakness': 'fire',     },
    'enemy_lvl_5': {  'health': 100,  'speed': 4,   'size': 38,  'reward': 10,   'weakness': 'poison',   },
    'enemy_lvl_6': {  'health': 250,  'speed': 2.8, 'size': 45,  'reward': 25,   'weakness': 'ice',      },
    'enemy_lvl_7': {  'health': 200,  'speed': 3.2,   'size': 40,  'reward': 15,   'weakness': 'light',    },
    'boss_lvl_1':  {  'health': 500, 'speed': 1,   'size': 60,  'reward': 100,  'weakness': 'earth',    },
    'boss_lvl_2':  {  'health': 1000, 'speed': 1.5, 'size': 70,  'reward': 100,  'weakness': 'water',    },
    'boss_lvl_3':  {  'health': 1500, 'speed': 2,   'size': 80,  'reward': 100,  'weakness': 'dark',     },
}

    def __init__(self, path_points, enemy_type='enemy_lvl_1'):
        self.path_points = path_points
        self.current_point = 0
        self.position = list(path_points[0])
        
        # Отримуємо характеристики відповідно до типу ворога
        enemy_props = self.ENEMY_TYPES[enemy_type]
        self.type = enemy_type
        self.speed = enemy_props['speed'] * SCALE_FACTOR
        self.size = enemy_props['size'] * SCALE_FACTOR
        self.health = enemy_props['health']
        self.max_health = enemy_props['health']
        self.reward = enemy_props['reward']
        
    def move(self):
        if self.current_point >= len(self.path_points) - 1:
            return True  # Ворог дійшов до кінця
            
        target = self.path_points[self.current_point + 1]
        
        # Розрахунок напрямку руху
        dx = target[0] - self.position[0]
        dy = target[1] - self.position[1]
        distance = (dx**2 + dy**2)**0.5
        
        if distance < self.speed:
            self.current_point += 1
        else:
            # Нормалізація вектора руху
            self.position[0] += (dx/distance) * self.speed
            self.position[1] += (dy/distance) * self.speed
        
        return False
        
    def take_damage(self, damage):
        self.health -= damage
        return self.health <= 0
        
    def draw(self, screen):
        # Малюємо зображення ворога
        image = ENEMY_IMAGES[self.type]
        image_rect = image.get_rect(center=self.position)
        screen.blit(image, image_rect)
        
        # Малюємо полоску здоров'я
        health_width = 40 * SCALE_FACTOR
        health_height = 5 * SCALE_FACTOR
        health_x = self.position[0] - health_width/2
        health_y = self.position[1] - self.size - health_height - 5
        
        pygame.draw.rect(screen, RED, 
                        (health_x, health_y, health_width, health_height))
        current_health_width = (self.health/self.max_health) * health_width
        pygame.draw.rect(screen, GREEN, 
                        (health_x, health_y, current_health_width, health_height)) 