import pygame

# Ініціалізація Pygame
pygame.init()

# Отримуємо розмір екрану пристрою
info = pygame.display.Info()
SCREEN_WIDTH = info.current_w
SCREEN_HEIGHT = info.current_h
SCALE_FACTOR = min(SCREEN_WIDTH/800, SCREEN_HEIGHT/600)

# Кольори
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (128, 128, 128)
BLUE = (0, 0, 255)
LIGHT_BLUE = (100, 100, 255)
YELLOW = (255, 255, 0)
BROWN = (165, 42, 42)
WATER_BLUE = (0, 191, 255)
FIRE_RED = (255, 69, 0)
EARTH_GREEN = (34, 139, 34)
PURPLE = (128, 0, 128)  # Додаємо фіолетовий колір для босса

# Створюємо вікно
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Tower Defense') 