import pygame
from config import WHITE, SCALE_FACTOR, WATER_BLUE, FIRE_RED, EARTH_GREEN
from config.assets import TOWER_IMAGES  # Додаємо імпорт зображень

# Характеристики веж
TOWER_PROPERTIES = {
    'water': {
        'color': WATER_BLUE, 
        'damage': 10, 
        'range': 150, 
        'cost': 100,
        'name': 'Водяна'
    },
    'fire': {
        'color': FIRE_RED, 
        'damage': 15, 
        'range': 100, 
        'cost': 150,
        'name': 'Вогняна'
    },
    'earth': {
        'color': EARTH_GREEN, 
        'damage': 8, 
        'range': 200, 
        'cost': 120,
        'name': 'Земляна'
    }
}

class Tower:
    def __init__(self, position, tower_type):
        self.position = position
        self.type = tower_type
        self.level = 1
        self.size = 30 * SCALE_FACTOR
        self.last_shot = 0
        self.shoot_delay = 1.0
        self.kills = 0
        
        # Копіюємо властивості для кожної вежі окремо
        self.properties = {
            'color': TOWER_PROPERTIES[tower_type]['color'],
            'damage': TOWER_PROPERTIES[tower_type]['damage'],
            'range': TOWER_PROPERTIES[tower_type]['range'],
            'cost': TOWER_PROPERTIES[tower_type]['cost'],
            'name': TOWER_PROPERTIES[tower_type]['name']
        }
        
        # Базова вартість вежі
        self.base_cost = self.properties['cost']
        # Вартість покращення (50% від базової вартості)
        self.upgrade_cost = int(self.base_cost * 0.5)
        
    def can_shoot(self, current_time):
        return current_time - self.last_shot >= self.shoot_delay
        
    def get_closest_enemy(self, enemies):
        closest_enemy = None
        min_distance = float('inf')
        
        for enemy in enemies:
            dx = enemy.position[0] - self.position[0]
            dy = enemy.position[1] - self.position[1]
            distance = (dx**2 + dy**2)**0.5
            
            if distance <= self.properties['range'] * SCALE_FACTOR:
                if distance < min_distance:
                    min_distance = distance
                    closest_enemy = enemy
                    
        return closest_enemy
        
    def draw(self, screen, selected=False):
        # Малюємо зображення вежі замість кола
        image = TOWER_IMAGES[self.type][self.level]
        image_rect = image.get_rect(center=self.position)
        screen.blit(image, image_rect)
        
        # Малюємо радіус дії якщо вежа вибрана
        if selected:
            pygame.draw.circle(screen, WHITE, 
                             (int(self.position[0]), int(self.position[1])), 
                             int(self.properties['range']), 
                             2)
    
    def upgrade(self):
        if self.level < 3:
            self.level += 1
            # Збільшуємо характеристики
            self.properties['damage'] *= 1.5
            self.properties['range'] *= 1.2
            # Збільшуємо вартість наступного покращення на 100%
            self.upgrade_cost *= 2
            return True
        return False 

    def get_total_cost(self):
        """Розраховує повну вартість вежі з урахуванням покращень"""
        base = self.base_cost
        if self.level == 2:
            base += self.base_cost * 0.5  # Перше покращення
        elif self.level == 3:
            base += self.base_cost * 0.5  # Перше покращення
            base += self.base_cost        # Друге покращення
        return base 