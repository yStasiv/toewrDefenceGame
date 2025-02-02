import pygame
from config import SCALE_FACTOR

# Завантаження та масштабування зображень
def load_scaled_image(path, size):
    img = pygame.image.load(path)
    return pygame.transform.scale(img, (
        int(size[0] * SCALE_FACTOR), 
        int(size[1] * SCALE_FACTOR)
    ))

# Налаштування зображень веж
TOWER_IMAGES = {
    'water': {
        1: load_scaled_image('resources/images/towers/water_1.png', (40, 40)),
        2: load_scaled_image('resources/images/towers/water_1.png', (40, 40)),
        3: load_scaled_image('resources/images/towers/water_1.png', (40, 40))
    },
    'fire': {
        1: load_scaled_image('resources/images/towers/fire_1.png', (40, 40)),
        2: load_scaled_image('resources/images/towers/fire_1.png', (40, 40)),
        3: load_scaled_image('resources/images/towers/fire_1.png', (40, 40))
    },
    'earth': {
        1: load_scaled_image('resources/images/towers/earth_1.png', (40, 40)),
        2: load_scaled_image('resources/images/towers/earth_1.png', (40, 40)),
        3: load_scaled_image('resources/images/towers/earth_1.png', (40, 40))
    }
}

# Налаштування зображень ворогів
ENEMY_IMAGES = {
    'normal': load_scaled_image('resources/images/enemies/normal.png', (30, 30)),
    'fast': load_scaled_image('resources/images/enemies/normal.png', (25, 25)),
    'tank': load_scaled_image('resources/images/enemies/normal.png', (40, 40)),
    'boss': load_scaled_image('resources/images/enemies/normal.png', (50, 50)),
    'swarm': load_scaled_image('resources/images/enemies/normal.png', (20, 20))
}

# Налаштування зображень улюбленців
PET_IMAGES = {
    'fast': load_scaled_image('resources/images/pets/petty.png', (30, 30)),
    'strong': load_scaled_image('resources/images/pets/petty.png', (40, 40)),
    'guard': load_scaled_image('resources/images/pets/petty.png', (35, 35))
}

# Зображення замку для різних рівнів здоров'я
CASTLE_IMAGES = {
    100: load_scaled_image('resources/images/castle/castle.png', (120, 120)),
    80: load_scaled_image('resources/images/castle/castle.png', (120, 120)),
    50: load_scaled_image('resources/images/castle/castle.png', (120, 120)),
    25: load_scaled_image('resources/images/castle/castle.png', (120, 120)),
    10: load_scaled_image('resources/images/castle/castle.png', (120, 120))
}

# Зображення монет та морквинок
COIN_IMAGE = load_scaled_image('resources/images/coin.png', (20, 20))
CARROT_IMAGE = load_scaled_image('resources/images/carrot.png', (25, 25))

# Зображення для інтерфейсу
UI_IMAGES = {
    # Кнопки
    'menu_button': load_scaled_image('resources/images/ui/menu_button.png', (150, 40)),
    'pause_button': load_scaled_image('resources/images/ui/pause_button.png', (150, 40)),
    'upgrade_button': load_scaled_image('resources/images/ui/upgrade_button.png', (90, 30)),
    'sell_button': load_scaled_image('resources/images/ui/sell_button.png', (90, 30)),
    
    # Іконки для лічильників
    'money_icon': load_scaled_image('resources/images/ui/money_icon.png', (25, 25)),
    'time_icon': load_scaled_image('resources/images/ui/time_icon.png', (25, 25)),
    'health_icon': load_scaled_image('resources/images/ui/health_icon.png', (25, 25)),
    'enemy_icon': load_scaled_image('resources/images/ui/enemy_icon.png', (25, 25)),
    'level_icon': load_scaled_image('resources/images/ui/level_icon.png', (25, 25)),
    
    # Фон для кнопок веж
    'tower_button_bg': load_scaled_image('resources/images/ui/tower_button_bg.png', (80, 10)),
    
    # Фон для кнопок улюбленців
    'pet_button_bg': load_scaled_image('resources/images/ui/pet_button_bg.png', (80, 10)),
    
    # Фон для вибраної кнопки
    'selected_button_bg': load_scaled_image('resources/images/ui/selected_button_bg.png', (90, 10)),
    
    # Додаємо іконки для звуку
    'sound_on': load_scaled_image('resources/images/ui/upgrade_button.png', (50, 50)),
    'sound_off': load_scaled_image('resources/images/ui/sell_button.png', (50, 50))
} 