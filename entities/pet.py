import pygame
from config import YELLOW, BLUE, RED, SCALE_FACTOR, BLACK
from config.assets import PET_IMAGES

class Pet:
    PET_TYPES = {
        'rabbit': {
            'speed': 10,
            'size': 15,
            'color': YELLOW,
            'cost': 500,
            'name': 'Швидкий збирач',
            'can_collect_carrots': False,
            'can_collect_coins': True,
            'can_attack': False
        },
        'dog': {
            'speed': 4,
            'size': 25,
            'color': BLUE,
            'cost': 300,
            'name': 'Надійний збирач',
            'can_collect_carrots': True,
            'can_collect_coins': True,
            'can_attack': False
        },
        'dragon': {
            'speed': 0,  # Не рухається
            'size': 20,
            'color': RED,
            'cost': 1000,
            'name': 'Охоронець',
            'can_collect_carrots': False,
            'can_collect_coins': False,
            'can_attack': True,
            'damage': 30,
            'attack_delay': 1.0,  # Секунд між пострілами
            'range': 10,  # TODO: не робе поки шо
            'shoot_delay': 1.0
        }
    }

    def __init__(self, position, pet_type='fast'):
        self.position = list(position)
        self.target = None
        self.carrots_collected = 0
        self.last_shot_time = 0
        
        # Отримуємо характеристики відповідно до типу
        pet_props = self.PET_TYPES[pet_type]
        self.type = pet_type
        self.speed = pet_props['speed'] * SCALE_FACTOR
        self.size = pet_props['size'] * SCALE_FACTOR
        self.color = pet_props['color']
        self.can_collect_carrots = pet_props['can_collect_carrots']
        self.can_collect_coins = pet_props['can_collect_coins']
        self.can_attack = pet_props['can_attack']
        
        if self.can_attack:
            self.damage = pet_props['damage']
            self.attack_delay = pet_props['attack_delay']
        
    def move_to_coin(self, coins):
        if not self.can_collect_coins or not coins:
            return None
            
        # Якщо немає цілі, знаходимо найближчу монету
        if not self.target:
            closest_coin = None
            min_distance = float('inf')
            
            for coin in coins:
                dx = coin.position[0] - self.position[0]
                dy = coin.position[1] - self.position[1]
                distance = (dx**2 + dy**2)**0.5
                
                if distance < min_distance:
                    min_distance = distance
                    closest_coin = coin
            
            self.target = closest_coin
        
        # Рухаємось до цілі
        if self.target:
            dx = self.target.position[0] - self.position[0]
            dy = self.target.position[1] - self.position[1]
            distance = (dx**2 + dy**2)**0.5
            
            if distance < self.speed:
                collected_coin = self.target
                self.target = None
                return collected_coin
            else:
                self.position[0] += (dx/distance) * self.speed
                self.position[1] += (dy/distance) * self.speed
        
        return None
        
    def can_shoot(self, current_time):
        return current_time - self.last_shot_time >= self.attack_delay
        
    def draw(self, screen):
        image = PET_IMAGES[self.type]
        image_rect = image.get_rect(center=self.position)
        screen.blit(image, image_rect) 