import pygame

# Ініціалізуємо звуковий мікшер
pygame.mixer.init()

def load_sound(path):
    return pygame.mixer.Sound(path)

# Завантажуємо всі звуки
SOUNDS = {
    # Звуки веж
    'tower_buy': load_sound('assets/sounds/tower_buy.wav'),
    'tower_sell': load_sound('assets/sounds/tower_buy.wav'),
    'tower_hit': load_sound('assets/sounds/tower_buy.wav'),
    
    # Звуки замку
    'castle_hit': load_sound('assets/sounds/tower_buy.wav'),
    
    # Звуки монет
    'coin_drop': load_sound('assets/sounds/tower_buy.wav'),
    'coin_pickup': load_sound('assets/sounds/tower_buy.wav'),
    
    # Звуки морквинок
    'carrot_pickup': load_sound('assets/sounds/tower_buy.wav'),
    'carrot_destroy': load_sound('assets/sounds/tower_buy.wav'),
    
    # Звуки рівнів
    'level_complete': load_sound('assets/sounds/tower_buy.wav'),
    'game_over': load_sound('assets/sounds/tower_buy.wav'),
    
    # Інші звуки
    'tower_place': load_sound('assets/sounds/tower_buy.wav'),
    'menu_click': load_sound('assets/sounds/tower_buy.wav'),
}

# Налаштовуємо гучність для кожного звуку
VOLUME = {
    'tower_buy': 0.7,
    'tower_sell': 0.7,
    'tower_hit': 0.5,
    'castle_hit': 0.8,
    'coin_drop': 0.6,
    'coin_pickup': 0.6,
    'carrot_pickup': 0.6,
    'carrot_destroy': 0.6,
    'level_complete': 1.0,
    'game_over': 1.0,
    'tower_place': 0.7,
    'menu_click': 0.7,
}

# Встановлюємо гучність для кожного звуку
for sound_name, volume in VOLUME.items():
    SOUNDS[sound_name].set_volume(volume)

# Додаємо змінну для контролю звуку
sound_enabled = True

def play_sound(sound_name):
    """Відтворює звук за його назвою"""
    if sound_enabled and sound_name in SOUNDS:
        SOUNDS[sound_name].play()

def toggle_sound():
    """Перемикає стан звуку"""
    global sound_enabled
    sound_enabled = not sound_enabled
    return sound_enabled

def get_sound_state():
    """Повертає поточний стан звуку"""
    return sound_enabled

# Фонова музика
MUSIC = {
    'menu': 'assets/sounds/music/menu_music.mp3',
    'game': 'assets/sounds/music/game_music.mp3',
}

def play_music(music_name):
    if music_name in MUSIC:
        pygame.mixer.music.set_volume(0.05)  # Значення від 0.0 до 1.0 
        pygame.mixer.music.load(MUSIC[music_name])
        pygame.mixer.music.play(-1)  # -1 означає безкінечне повторення

def stop_music():
    pygame.mixer.music.stop() 