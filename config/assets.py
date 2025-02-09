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
        'bg': load_scaled_image('resources/images/towers/water_tower_bg.png', (40, 80)),
        0: load_scaled_image('resources/images/towers/water_tower.png', (40, 60)),
        1: load_scaled_image('resources/images/towers/water_tower_1lvl_upgrade.png', (40, 60)),
        2: load_scaled_image('resources/images/towers/water_tower_2lvl_upgrade.png', (40, 60)),
        3: load_scaled_image('resources/images/towers/water_tower_3lvl_upgrade.png', (40, 60))
    },
    'fire': {
        'bg': load_scaled_image('resources/images/towers/fire_tower_bg.png', (40, 80)),
        0: load_scaled_image('resources/images/towers/fire_tower.png', (40, 60)),
        1: load_scaled_image('resources/images/towers/fire_tower_1lvl_upgrade.png', (40, 60)),
        2: load_scaled_image('resources/images/towers/fire_tower_2lvl_upgrade.png', (40, 60)),
        3: load_scaled_image('resources/images/towers/fire_tower_3lvl_upgrade.png', (40, 60))
    },
    'earth': {
        "bg": load_scaled_image('resources/images/towers/earth_tower_bg.png', (40, 80)),
        0: load_scaled_image('resources/images/towers/earth_tower.png', (40, 60)),
        1: load_scaled_image('resources/images/towers/earth_tower_1lvl_upgrade.png', (40, 60)),
        2: load_scaled_image('resources/images/towers/earth_tower_2lvl_upgrade.png', (40, 60)),
        3: load_scaled_image('resources/images/towers/earth_tower_3lvl_upgrade.png', (40, 60))
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
    'rabbit': load_scaled_image('resources/images/pets/rabbit_pet.png', (30, 40)),
    'dragon': load_scaled_image('resources/images/pets/dragon_pet.png', (40, 40)),
    'dog': load_scaled_image('resources/images/pets/dog_pet.png', (40, 35))
}


# Зображення замку для різних рівнів здоров'я
CASTLE_IMAGES = {
    100: load_scaled_image('resources/images/castle/castle_100persent_hp.png', (120, 120)),
    75: load_scaled_image('resources/images/castle/castle_75persent_hp.png', (120, 120)),
    50: load_scaled_image('resources/images/castle/castle_50persent_hp.png', (120, 120)),
    30: load_scaled_image('resources/images/castle/castle_30persent_hp.png', (120, 120)),
    20: load_scaled_image('resources/images/castle/castle_20persent_hp.png', (120, 120)),
    10: load_scaled_image('resources/images/castle/castle_10persent_hp.png', (120, 120)),
}


# Зображення монет та морквинок
COIN_IMAGE = load_scaled_image('resources/images/bank_coin.png', (20, 20))
CARROT_IMAGE = load_scaled_image('resources/images/carrot.png', (25, 25))

# Завантаження зображень монет різного номіналу
COIN_IMAGES = {
    '10': pygame.transform.scale(pygame.image.load('resources/images/coins/coin_10.png'), (30 * SCALE_FACTOR, 30 * SCALE_FACTOR)),
    '15': pygame.transform.scale(pygame.image.load('resources/images/coins/coin_15.png'), (30 * SCALE_FACTOR, 30 * SCALE_FACTOR)),
    '25': pygame.transform.scale(pygame.image.load('resources/images/coins/coin_25.png'), (30 * SCALE_FACTOR, 30 * SCALE_FACTOR)),
    '100': pygame.transform.scale(pygame.image.load('resources/images/coins/coin_100.png'), (30 * SCALE_FACTOR, 30 * SCALE_FACTOR))
}

# Зображення для інтерфейсу
UI_IMAGES = {
    # Кнопки
    'menu_button': load_scaled_image('resources/images/ui/menu_button.png', (150, 40)),
    'pause_button': load_scaled_image('resources/images/ui/pause_button.png', (150, 40)),
    'upgrade_button': load_scaled_image('resources/images/ui/upgrade_button.png', (90, 30)),
    'sell_button': load_scaled_image('resources/images/ui/sell_button.png', (90, 30)),
    
    # Іконки для лічильників
    'money_icon': load_scaled_image('resources/images/ui/bank_coin.png', (25, 25)),
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
    'sound_off': load_scaled_image('resources/images/ui/sell_button.png', (50, 50)),
    
    # Завантаження зображень стрілок
    'open_pet_store': load_scaled_image('resources/images/store_btns/open_pet_store.png', (50, 50)),
    'close_pet_store': load_scaled_image('resources/images/store_btns/close_pet_store.png', (50, 50)),
}

# Завантаження зображень снарядів
PROJECTILE_IMAGES = {
    'normal': load_scaled_image('resources/images/pets/dragon_bullet.png', (10, 10)),
    'fire': load_scaled_image('resources/images/towers/fire_bullet.png', (10, 10)),
    'water': load_scaled_image('resources/images/towers/water_bullet.png', (10, 10)),
    'earth': load_scaled_image('resources/images/towers/earth_bullet.png', (10, 10)),

}