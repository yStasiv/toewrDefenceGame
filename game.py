import pygame
import sys
from pygame import time, event
from pygame.locals import *
from config import *
from entities.enemy import Enemy
from entities.tower import Tower, TOWER_PROPERTIES
from entities.projectile import Projectile
from entities.coin import Coin
from ui.menu import Menu
import random
from entities.pet import Pet
from entities.carrot import Carrot
from config.assets import CASTLE_IMAGES, CASTLE_IMAGES, UI_IMAGES, CARROT_IMAGE, TOWER_IMAGES, PET_IMAGES
from config.sounds import play_sound, play_music, stop_music  # Додаємо імпорт

class Game:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.menu = Menu()
        self.current_screen = 'menu'
        
        # Додаємо змінні для керування ворогами
        self.enemies_per_level = 10  # Фіксована кількість ворогів на рівень
        self.enemies_spawned = 0     # Скільки ворогів вже з'явилось
        self.enemies_processed = 0    # Скільки ворогів або знищено, або дійшло до замку
        self.level = 1
        self.selected_type_highlight = pygame.Surface((100 * SCALE_FACTOR, 50 * SCALE_FACTOR))
        self.selected_type_highlight.set_alpha(128)  # Напівпрозорість
        self.selected_type_highlight.fill(WHITE)
        
        # Точки шляху для ворогів
        self.path_points = [
            (0, SCREEN_HEIGHT * 0.8),
            (SCREEN_WIDTH * 0.3, SCREEN_HEIGHT * 0.8),
            (SCREEN_WIDTH * 0.3, SCREEN_HEIGHT * 0.4),
            (SCREEN_WIDTH * 0.7, SCREEN_HEIGHT * 0.4),
            (SCREEN_WIDTH * 0.7, SCREEN_HEIGHT * 0.2),
            (SCREEN_WIDTH - 50, SCREEN_HEIGHT * 0.2)  # Кінець шляху
        ]
        
        # Точки для веж
        self.tower_spots = [
            (SCREEN_WIDTH * 0.2, SCREEN_HEIGHT * 0.7),
            (SCREEN_WIDTH * 0.4, SCREEN_HEIGHT * 0.7),
            (SCREEN_WIDTH * 0.2, SCREEN_HEIGHT * 0.3),
            (SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.3),
            (SCREEN_WIDTH * 0.8, SCREEN_HEIGHT * 0.3),
            (SCREEN_WIDTH * 0.8, SCREEN_HEIGHT * 0.1)
        ]
        
        # Ігрові об'єкти
        self.towers = []
        self.enemies = [Enemy(self.path_points)]
        self.projectiles = []
        self.coins = []
        
        # Інтерфейс
        self.top_ui_height = 40 * SCALE_FACTOR
        self.ui_height = SCREEN_HEIGHT * 0.15
        self.ui_y = SCREEN_HEIGHT - self.ui_height
        self.ui_font_small = pygame.font.Font(None, int(18 * SCALE_FACTOR))
        self.ui_font = pygame.font.Font(None, int(36 * SCALE_FACTOR))
        # self.ui_font_large = pygame.font.Font(None, int(48 * SCALE_FACTOR))  # Поки не потрібно
        
        # Гроші та вибрані об'єкти
        self.money = 300
        self.selected_tower = None
        self.selected_type = None
        self.game_time = 0
        self.paused = False
        
        # Кнопки інтерфейсу
        button_width = 150 * SCALE_FACTOR
        button_height = 40 * SCALE_FACTOR
        self.menu_button = pygame.Rect(10, self.ui_y + 10, button_width, button_height)
        self.pause_button = pygame.Rect(button_width + 20, self.ui_y + 10, button_width, button_height)
        self.upgrade_button = pygame.Rect(
            SCREEN_WIDTH * 0.45,  # Трохи правіше від інформації
            self.ui_y + 60,
            120 * SCALE_FACTOR,  # Збільшуємо ширину кнопок
            40 * SCALE_FACTOR
        )
        
        # Кнопки вибору типу вежі
        self.tower_buttons = []
        for i, t_type in enumerate(['water', 'fire', 'earth']):
            button_x = SCREEN_WIDTH - (3 - i) * 100 * SCALE_FACTOR
            self.tower_buttons.append({
                'rect': pygame.Rect(button_x, self.ui_y + 10, 80 * SCALE_FACTOR, 40 * SCALE_FACTOR),
                'type': t_type
            })
        
        # Додаємо змінну для рекорду
        try:
            with open('record.txt', 'r') as f:
                self.record_level = int(f.read())
        except:
            self.record_level = 1
        
        # Додаємо параметри замку
        self.castle_position = (SCREEN_WIDTH - 50, SCREEN_HEIGHT * 0.12)  # Кінець шляху
        self.castle_size = 60 * SCALE_FACTOR
        self.castle_max_health = 100
        self.castle_health = self.castle_max_health
        self.game_over = False
        self.last_spawn_time = 0  # Додаємо час останньої появи ворога
        
        # Додаємо параметри для затримки перед рівнем
        self.level_start_delay = 3.0  # 3 секунди затримки
        self.level_start_time = 0
        self.level_starting = True
        
        # Додаємо кнопку продажу
        self.sell_button = pygame.Rect(
            SCREEN_WIDTH * 0.45,
            self.ui_y + 110,  # Нижче кнопки покращення
            120 * SCALE_FACTOR,
            40 * SCALE_FACTOR
        )
        
        # Додаємо статистику гри
        self.total_enemies_killed = 0
        self.total_money_earned = 0  # Тільки від вбитих ворогів
        self.money_from_enemies = 0  # Нова змінна для відстеження грошей від ворогів
        self.current_screen = 'menu'  # Можливі значення: 'menu', 'game', 'game_over'
        
        # Змінюємо систему улюбленців
        self.pets = {}  # Словник куплених улюбленців
        self.active_pet = None  # Активний улюбленець
        self.last_pet_switch_level = 0  # Рівень останнього перемикання
        
        # Кнопки для улюbленців
        self.pet_buttons = []
        for i, p_type in enumerate(['rabbit', 'dog', 'dragon']):
            button_x = SCREEN_WIDTH - (3 - i) * 100 * SCALE_FACTOR
            self.pet_buttons.append({
                'rect': pygame.Rect(button_x, self.ui_y + 60, 80 * SCALE_FACTOR, 40 * SCALE_FACTOR),
                'type': p_type
            })
        
        self.carrots = []  # Додаємо список для морквинок
        
        # Додаємо завантаження збережених морквинок
        self.total_carrots_collected = 0
        try:
            with open('carrots.txt', 'r') as f:
                self.total_carrots_collected = int(f.read())
        except:
            self.total_carrots_collected = 0
        
        # Додаємо параметри для випливаючого меню улюbленців
        self.pet_menu_expanded = False
        self.pet_menu_position = 0  # 0 - закрите, 1 - відкрите
        self.pet_menu_width = 300 * SCALE_FACTOR
        
        # Кнопка-стрілка
        arrow_size = 30 * SCALE_FACTOR
        self.arrow_button = pygame.Rect(
            SCREEN_WIDTH - arrow_size - 30,
            SCREEN_HEIGHT - arrow_size - 40,
            arrow_size,
            arrow_size
        )
        
        # Додаємо параметр для контролю музики
        self.music_playing = True
        # Запускаємо музику меню
        play_music('menu')

    def draw_path(self):
        if len(self.path_points) > 1:
            pygame.draw.lines(screen, BLACK, False, self.path_points, int(5 * SCALE_FACTOR))

    def draw_tower_spots(self):
        for spot in self.tower_spots:
            pygame.draw.circle(screen, GREEN, (int(spot[0]), int(spot[1])), 
                             int(20 * SCALE_FACTOR))

    def draw_top_ui(self):
        pygame.draw.rect(screen, GRAY, (0, 0, SCREEN_WIDTH, self.top_ui_height))
        
        # Здоров'я замку
        screen.blit(UI_IMAGES['health_icon'], (10, 5))
        castle_text = self.ui_font.render(f'{int(self.castle_health)}/{self.castle_max_health}', True, BLACK)
        screen.blit(castle_text, (40, 5))
        
        # Час
        screen.blit(UI_IMAGES['time_icon'], (200 * SCALE_FACTOR, 5))
        time_text = self.ui_font.render(f'{int(self.game_time)}с', True, BLACK)
        screen.blit(time_text, (230 * SCALE_FACTOR, 5))
        
        # Гроші
        screen.blit(UI_IMAGES['money_icon'], (400 * SCALE_FACTOR, 5))
        money_text = self.ui_font.render(str(self.money), True, BLACK)
        screen.blit(money_text, (430 * SCALE_FACTOR, 5))
        
        # Морквинки
        screen.blit(CARROT_IMAGE, (500 * SCALE_FACTOR, 5))
        total_carrot_text = self.ui_font.render(str(self.total_carrots_collected), True, BLACK)
        screen.blit(total_carrot_text, (530 * SCALE_FACTOR, 5))
        
        # Рівень
        screen.blit(UI_IMAGES['level_icon'], (800 * SCALE_FACTOR, 5))
        level_text = self.ui_font.render(str(self.level), True, BLACK)
        screen.blit(level_text, (830 * SCALE_FACTOR, 5))
        
        # Залишилось ворогів
        screen.blit(UI_IMAGES['enemy_icon'], (900 * SCALE_FACTOR, 5))
        remaining_enemies = self.enemies_per_level - self.enemies_spawned
        enemies_text = self.ui_font.render(str(remaining_enemies), True, BLACK)
        screen.blit(enemies_text, (930 * SCALE_FACTOR, 5))

    def draw_ui(self):
        # Малюємо інтерфейс внизу екрану
        pygame.draw.rect(screen, GRAY, (0, self.ui_y, SCREEN_WIDTH, self.ui_height))
        
        # Малюємо кнопку меню
        screen.blit(UI_IMAGES['menu_button'], self.menu_button)
        menu_text = self.ui_font.render('', True, WHITE)
        menu_rect = menu_text.get_rect(center=self.menu_button.center)
        screen.blit(menu_text, menu_rect)
        
        # Малюємо кнопку паузи
        screen.blit(UI_IMAGES['pause_button'], self.pause_button)
        pause_text = self.ui_font.render('', True, BLACK)
        pause_rect = pause_text.get_rect(center=self.pause_button.center)
        screen.blit(pause_text, pause_rect)
        
        # Малюємо кнопки вибору типу вежі
        for button in self.tower_buttons:
            # Якщо вибрана, малюємо підсвічування
            if self.selected_type == button['type']:
                screen.blit(TOWER_IMAGES[button['type']]['bg'], button['rect'])
            
            # Малюємо зображення вежі
            screen.blit(TOWER_IMAGES[button['type']][0], button['rect'])
            
            # Додамо для навчання(щоб було зрозуміло що це за вежа)
            # type_text = self.ui_font.render(button['type'].title(), True, WHITE)
            # text_rect = type_text.get_rect(center=button['rect'].center)
            # screen.blit(type_text, text_rect)
            
            # Додаємо вартість
            cost = TOWER_PROPERTIES[button['type']]['cost']
            cost_text = self.ui_font_small.render(f'{cost}', True, WHITE)
            cost_rect = cost_text.get_rect(center=button['rect'].center)
            cost_rect.x += 20  # Посуваємо текст вліво на 20 пікселів

            screen.blit(cost_text, cost_rect)
        
        # Малюємо інформацію про вибрану вежу та кнопки
        if self.selected_tower:
            tower = self.selected_tower
            
            # Створюємо фон для інформації про вежу
            info_bg = pygame.Rect(10, self.ui_y + 60, SCREEN_WIDTH * 0.4, 80 * SCALE_FACTOR)
            pygame.draw.rect(screen, (200, 200, 200), info_bg)  # Світло-сірий фон
            
            # Розділяємо інформацію на два рядки
            name_text = self.ui_font.render(
                f"{TOWER_PROPERTIES[tower.type]['name']}", 
                True, BLACK
            )
            screen.blit(name_text, (info_bg.x + 10, info_bg.y + 10))
            
            stats_text = self.ui_font.render(
                f"Рівень: {tower.level}  |  Вбито: {tower.kills}", 
                True, BLACK
            )
            screen.blit(stats_text, (info_bg.x + 10, info_bg.y + 40))
            
            # Кнопки справа від інформації
            if tower.level < 3:
                # Кнопка покращення
                screen.blit(UI_IMAGES['upgrade_button'], self.upgrade_button)
                upgrade_text = self.ui_font.render(f'Покращити ({tower.upgrade_cost})', True, WHITE)
                text_rect = upgrade_text.get_rect(center=self.upgrade_button.center)
                screen.blit(upgrade_text, text_rect)
            
            # Кнопка продажу
            sell_price = int(tower.get_total_cost() * 0.8)
            screen.blit(UI_IMAGES['sell_button'], self.sell_button)
            sell_text = self.ui_font.render(f'Продати ({sell_price})', True, WHITE)
            text_rect = sell_text.get_rect(center=self.sell_button.center)
            screen.blit(sell_text, text_rect)
        
        # Малюємо горизонтальне випливаюче меню улюbленців
        menu_width = self.pet_menu_width * self.pet_menu_position
        menu_rect = pygame.Rect(
            SCREEN_WIDTH - menu_width,  # Починаємо з правого краю
            SCREEN_HEIGHT - 200 * SCALE_FACTOR,
            menu_width,
            200 * SCALE_FACTOR
        )
        pygame.draw.rect(screen, (200, 200, 200), menu_rect)
        
        # Малюємо кнопки улюbленців горизонтально
        if self.pet_menu_position > 0:
            for i, button in enumerate(self.pet_buttons):
                # Оновлюємо позицію кнопок для горизонтального розміщення справа
                button['rect'].x = menu_rect.right - ((3 - i) * 100 * SCALE_FACTOR)
                button['rect'].y = menu_rect.y + 20
                
                if button['type'] in self.pets:
                    screen.blit(UI_IMAGES['selected_button_bg'], 
                               (button['rect'].x - 5, button['rect'].y - 5))
                
                screen.blit(UI_IMAGES['pet_button_bg'], button['rect'])
                screen.blit(PET_IMAGES[button['type']], button['rect'])
                
                # Додаємо ціну улюbленця
                pet_name = str(Pet.PET_TYPES[button['type']]['cost'])
                type_text = self.ui_font.render(pet_name, True, WHITE)
                text_rect = type_text.get_rect(
                    midtop=(button['rect'].centerx, button['rect'].bottom + 5)
                )
                screen.blit(type_text, text_rect)
        
        # Малюємо кнопку-стрілку
        arrow_image = UI_IMAGES['open_pet_store'] if not self.pet_menu_expanded else UI_IMAGES['close_pet_store']
        screen.blit(arrow_image, self.arrow_button)

    def handle_tower_placement(self, pos):
        for spot in self.tower_spots:
            distance = ((pos[0] - spot[0])**2 + (pos[1] - spot[1])**2)**0.5
            if distance < 20 * SCALE_FACTOR:
                spot_occupied = any(((t.position[0] - spot[0])**2 + 
                                   (t.position[1] - spot[1])**2)**0.5 < 1 
                                  for t in self.towers)
                
                if not spot_occupied and self.selected_type:
                    tower_cost = TOWER_PROPERTIES[self.selected_type]['cost']
                    if self.money >= tower_cost:
                        self.towers.append(Tower(spot, self.selected_type))
                        self.money -= tower_cost
                        play_sound('tower_buy')  # Додаємо звук при покупці вежі
                return True
        return False

    def update_projectiles(self):
        for proj in self.projectiles[:]:
            # Шукаємо ворога, в якого цілився снаряд
            target_pos = None
            for enemy in self.enemies:
                if enemy.position == proj.target_pos:  # Змінено з target на target_pos
                    target_pos = enemy.position
                    break
                
            if proj.move(target_pos):  # Передаємо нову позицію цілі
                self.projectiles.remove(proj)

    def update_towers(self, current_time):
        for tower in self.towers:
            if tower.can_shoot(current_time):
                enemy = tower.get_closest_enemy(self.enemies)
                if enemy:
                    tower.last_shot = current_time
                    self.projectiles.append(
                        Projectile(tower.position, enemy.position, 
                                 tower.properties['damage'])
                    )
        
        # Оновлюємо активного улюбленця
        if self.active_pet:
            if self.active_pet.type == 'dragon':
                # Логіка дракона
                self.active_pet.position = [self.castle_position[0] - 50, self.castle_position[1]]
                if self.active_pet.can_shoot(current_time):
                    # Спочатку намагаємось знищити морквинки
                    for carrot in self.carrots[:]:
                        self.projectiles.append(
                            Projectile(self.active_pet.position, carrot.position, self.active_pet.damage)
                        )
                        self.carrots.remove(carrot)
                        self.active_pet.last_shot_time = current_time
                        play_sound('carrot_destroy')
                        break
                    else:
                        # Якщо морквинок немає, стріляємо по ворогах
                        if self.enemies:
                            target = self.enemies[0]  # Стріляємо в першого ворога
                            self.projectiles.append(
                                Projectile(self.active_pet.position, target.position, self.active_pet.damage)
                            )
                            self.active_pet.last_shot_time = current_time

    def check_projectile_collisions(self):
        """Перевіряє зіткнення снарядів з ворогами"""
        for proj in self.projectiles[:]:
            for enemy in self.enemies[:]:
                dx = enemy.position[0] - proj.position[0]
                dy = enemy.position[1] - proj.position[1]
                distance = (dx**2 + dy**2)**0.5
                
                if distance < enemy.size + proj.size:
                    if enemy.take_damage(proj.damage):
                        # Додаємо +1 до лічильників
                        self.enemies_killed += 1
                        self.enemies_processed += 1
                        
                        # Додаємо нагороду до статистики
                        self.money_from_enemies += enemy.reward
                        
                        # Додаємо +1 до лічильника вбивств вежі
                        for tower in self.towers:
                            if (tower.position[0] == proj.start_pos[0] and 
                                tower.position[1] == proj.start_pos[1]):
                                tower.kills += 1
                                break
                        
                        self.enemies.remove(enemy)
                        self.coins.append(Coin(enemy.position, enemy.reward))
                        play_sound('coin_drop')  # Додаємо звук випадання монетки
                        
                        # Шанс 15% що випаде морквина
                        if random.random() < 0.15:
                            self.carrots.append(Carrot(enemy.position))
                    if proj in self.projectiles:
                        self.projectiles.remove(proj)

    def spawn_enemy(self):
        """Створює нового ворога з урахуванням поточного рівня"""
        # Перевіряємо чи потрібно створювати нових ворогів
        if self.enemies_spawned >= self.enemies_per_level:
            return

        # Додаємо затримку між появою ворогів
        current_time = pygame.time.get_ticks() / 1000.0
        if not hasattr(self, 'last_spawn_time'):
            self.last_spawn_time = 0
        
        if current_time - self.last_spawn_time < 2.0:  # 2 секунди між появою ворогів
            return
        
        # Максимум 3 ворога одночасно
        # Максимальна кількість одночасних ворогів збільшується з рівнем
        max_simultaneous = 3 + (self.level - 1) // 2  # Кожні 2 рівні +1 до максимуму
        max_simultaneous = min(max_simultaneous, 10)   # Але не більше 10
        
        # Перевіряємо чи не досягнуто ліміт
        if len(self.enemies) >= max_simultaneous:
            return
        
        # Вибір типу ворога залежно від рівня
        r = random.random()
        
        if self.level < 3:
            # Рівні 1-2: тільки звичайні вороги
            enemy_type = 'normal'
        elif self.level < 5:
            # Рівні 3-4: звичайні та швидкі
            enemy_type = 'fast' if r > 0.7 else 'normal'
        elif self.level < 7:
            # Рівні 5-6: звичайні, швидкі та танки
            if r > 0.8:
                enemy_type = 'tank'
            elif r > 0.5:
                enemy_type = 'fast'
            else:
                enemy_type = 'normal'
        elif self.level < 10:
            # Рівні 7-9: всі типи крім босса
            if r > 0.8:
                enemy_type = 'tank'
            elif r > 0.6:
                enemy_type = 'fast'
            elif r > 0.4:
                enemy_type = 'swarm'
            else:
                enemy_type = 'normal'
        else:
            # Рівень 10+: всі типи ворогів
            if r > 0.9:
                enemy_type = 'boss'
            elif r > 0.7:
                enemy_type = 'tank'
            elif r > 0.5:
                enemy_type = 'fast'
            elif r > 0.3:
                enemy_type = 'swarm'
            else:
                enemy_type = 'normal'
        
        self.enemies.append(Enemy(self.path_points, enemy_type))
        self.enemies_spawned += 1
        self.last_spawn_time = current_time

    def check_level_complete(self):
        """Перевіряє чи всі вороги рівня оброблені (вбиті або дійшли до замку)"""
        if (self.enemies_processed >= self.enemies_per_level and 
            len(self.enemies) == 0):
            play_sound('level_complete')  # Додаємо звук при завершенні рівня
            self.level += 1
            
            # Очищуємо всі снаряди при завершенні рівня
            self.projectiles.clear()
            
            # Оновлюємо рекорд якщо потрібно
            if self.level > self.record_level:
                self.record_level = self.level
                # Зберігаємо новий рекорд
                with open('record.txt', 'w') as f:
                    f.write(str(self.record_level))
            
            # Скидаємо лічильники для нового рівня
            self.enemies_spawned = 0
            self.enemies_processed = 0
            self.enemies_killed = 0
            
            # Очищуємо незібрані морквинки
            self.carrots.clear()
            
            # Збільшуємо кількість ворогів на 15%
            self.enemies_per_level = int(self.enemies_per_level * 1.15)
            
            # Встановлюємо затримку перед початком нового рівня
            self.level_starting = True
            self.level_start_time = pygame.time.get_ticks() / 1000.0

    def draw_castle(self):
        # Визначаємо який стан замку показувати
        health_percent = (self.castle_health / self.castle_max_health) * 100
        
        if health_percent > 70:
            castle_image = CASTLE_IMAGES[100]
        elif health_percent > 50:
            castle_image = CASTLE_IMAGES[75]
        elif health_percent > 30:
            castle_image = CASTLE_IMAGES[50]
        elif health_percent > 20:
            castle_image = CASTLE_IMAGES[30]
        elif health_percent > 10:
            castle_image = CASTLE_IMAGES[20]
        else:
            castle_image = CASTLE_IMAGES[10]
        
        # Малюємо зображення замку
        image_rect = castle_image.get_rect(center=self.castle_position)
        screen.blit(castle_image, image_rect)
        
        # Малюємо полоску здоров'я
        health_width = 80 * SCALE_FACTOR
        health_height = 10 * SCALE_FACTOR
        health_x = self.castle_position[0] - health_width/2
        health_y = image_rect.top - health_height - 5
        
        pygame.draw.rect(screen, RED, 
                        (health_x, health_y, health_width, health_height))
        current_health_width = (self.castle_health/self.castle_max_health) * health_width
        pygame.draw.rect(screen, GREEN, 
                        (health_x, health_y, current_health_width, health_height))

    def handle_enemy_reached_castle(self, enemy):
        # Віднімаємо здоров'я замку залежно від поточного здоров'я ворога
        damage = enemy.health / 10  # 10% від поточного здоров'я ворога
        play_sound('castle_hit')  # Додаємо звук при влучанні в замок
        self.castle_health -= damage
        
        # Збільшуємо лічильник оброблених ворогів
        self.enemies_processed += 1
        
        if self.castle_health <= 0:
            self.castle_health = 0
            play_sound('game_over')  # Додаємо звук при програші
            self.game_over = True

    def draw_game_over_screen(self):
        screen.fill(WHITE)
        
        # Малюємо заголовок
        title_font = pygame.font.Font(None, int(100 * SCALE_FACTOR))
        title_text = title_font.render('Гра Завершена!', True, RED)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT * 0.2))
        screen.blit(title_text, title_rect)
        
        # Малюємо статистику
        stats_font = pygame.font.Font(None, int(50 * SCALE_FACTOR))
        
        # Рівень
        level_text = stats_font.render(f'Досягнутий рівень: {self.level}', True, BLACK)
        level_rect = level_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT * 0.4))
        screen.blit(level_text, level_rect)
        
        # Вбиті вороги
        kills_text = stats_font.render(f'Знищено ворогів: {self.total_enemies_killed}', True, BLACK)
        kills_rect = kills_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT * 0.5))
        screen.blit(kills_text, kills_rect)
        
        # Зароблені гроші
        money_text = stats_font.render(f'Зароблено золота: {self.total_money_earned}', True, BLACK)
        money_rect = money_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT * 0.6))
        screen.blit(money_text, money_rect)
        
        # Кнопка повернення в меню
        button_width = 400 * SCALE_FACTOR
        button_height = 80 * SCALE_FACTOR
        menu_button = pygame.Rect(
            (SCREEN_WIDTH - button_width) / 2,
            SCREEN_HEIGHT * 0.8,
            button_width,
            button_height
        )
        
        pygame.draw.rect(screen, BLUE, menu_button, border_radius=int(15 * SCALE_FACTOR))
        button_text = stats_font.render('До головного меню', True, WHITE)
        text_rect = button_text.get_rect(center=menu_button.center)
        screen.blit(button_text, text_rect)
        
        return menu_button  # Повертаємо rect кнопки для обробки кліків

    def update(self):
        # Оновлюємо позицію меню
        target_position = 1.0 if self.pet_menu_expanded else 0.0
        if self.pet_menu_position < target_position:
            self.pet_menu_position = min(self.pet_menu_position + 0.1, target_position)
        elif self.pet_menu_position > target_position:
            self.pet_menu_position = max(self.pet_menu_position - 0.1, target_position)

    def run(self):
        while True:
            current_time = time.get_ticks() / 1000.0
            dt = self.clock.tick(60) / 1000.0
            
            for e in event.get():
                if e.type == QUIT:
                    pygame.quit()
                    sys.exit()
                
                if e.type == MOUSEBUTTONDOWN:
                    if self.current_screen == 'game':
                        # Спочатку перевіряємо клік по монетках (завжди активно)
                        for coin in self.coins[:]:
                            dx = e.pos[0] - coin.position[0]
                            dy = e.pos[1] - coin.position[1]
                            if (dx**2 + dy**2)**0.5 < coin.size:
                                self.money += coin.value
                                self.coins.remove(coin)
                                play_sound('coin_pickup')
                                continue
                        
                        # Перевіряємо кліки по кнопках меню та паузи (завжди активні)
                        if self.menu_button.collidepoint(e.pos):
                            self.current_screen = 'menu'
                            stop_music()  # Зупиняємо музику гри
                            play_music('menu')  # Запускаємо музику меню
                            self.__init__()
                            continue
                        
                        if self.pause_button.collidepoint(e.pos):
                            self.paused = not self.paused
                            continue
                        
                        # Перевіряємо кліки по кнопках покращення/продажу, якщо вежа вибрана
                        if self.selected_tower:
                            if self.upgrade_button.collidepoint(e.pos):
                                if (self.selected_tower.level < 3 and 
                                    self.money >= self.selected_tower.upgrade_cost):
                                    upgrade_cost = self.selected_tower.upgrade_cost
                                    if self.selected_tower.upgrade():
                                        self.money -= upgrade_cost
                                        continue
                            
                            if self.sell_button.collidepoint(e.pos):
                                sell_price = int(self.selected_tower.get_total_cost() * 0.8)
                                self.money += sell_price
                                self.towers.remove(self.selected_tower)
                                self.selected_tower = None
                                play_sound('tower_sell')
                                continue
                        
                        # Далі обробляємо кліки по меню улюбленців та вежах
                        if self.arrow_button.collidepoint(e.pos):
                            self.pet_menu_expanded = not self.pet_menu_expanded
                            play_sound('menu_click')  # TODO: Додати звук
                            # Скидаємо вибір типу вежі при відкритті/закритті меню
                            self.selected_type = None
                            self.selected_tower = None
                        elif self.pet_menu_expanded and self.pet_menu_position > 0.9:  # Перевіряємо що меню повністю відкрите
                            # Обробляємо кліки по кнопках улюbленців
                            for button in self.pet_buttons:
                                if button['rect'].collidepoint(e.pos):
                                    pet_type = button['type']
                                    if pet_type in self.pets:
                                        if self.level > self.last_pet_switch_level:
                                            self.active_pet = self.pets[pet_type]
                                            self.last_pet_switch_level = self.level
                                    else:
                                        pet_cost = Pet.PET_TYPES[pet_type]['cost']
                                        if self.money >= pet_cost and self.level > self.last_pet_switch_level:
                                            new_pet = Pet((SCREEN_WIDTH/2, SCREEN_HEIGHT/2), pet_type)
                                            self.pets[pet_type] = new_pet
                                            self.active_pet = new_pet
                                            self.money -= pet_cost
                                            self.last_pet_switch_level = self.level
                                    break
                        elif not self.pet_menu_expanded and self.pet_menu_position < 0.1:
                            # Обробка кліків по вежах та інших елементах
                            for button in self.tower_buttons:
                                if button['rect'].collidepoint(e.pos):
                                    self.selected_type = button['type']
                                    self.selected_tower = None
                                    break
                            
                            # Перевіряємо клік по вежах
                            for tower in self.towers:
                                distance = ((e.pos[0] - tower.position[0])**2 + 
                                          (e.pos[1] - tower.position[1])**2)**0.5
                                if distance < tower.size:
                                    self.selected_tower = tower
                                    self.selected_type = None
                                    break
                            
                            # Спроба встановити нову вежу
                            if self.selected_type:
                                self.handle_tower_placement(e.pos)
                    elif self.current_screen == 'menu':
                        action = self.menu.handle_click(e.pos)
                        if action == 'start':
                            self.current_screen = 'game'
                            stop_music()  # Зупиняємо музику меню
                            play_music('game')  # Запускаємо музику гри
                            self.game_time = 0
                            self.enemies = [Enemy(self.path_points)]
                            self.enemies_spawned = 0
                            self.enemies_killed = 0
                            self.paused = False
                        elif action == 'settings':
                            pass
                        elif action == 'quit':
                            pygame.quit()
                            sys.exit()
                    elif self.current_screen == 'game_over':
                        menu_button = self.draw_game_over_screen()
                        if menu_button.collidepoint(e.pos):
                            self.current_screen = 'menu'
                            self.__init__()

            if self.current_screen == 'game' and not self.paused:
                # Перевіряємо чи триває затримка перед рівнем
                if self.level_starting:
                    if current_time - self.level_start_time >= self.level_start_delay:
                        self.level_starting = False
                else:
                    self.spawn_enemy()
                    self.update_towers(current_time)
                    self.update_projectiles()
                    self.check_projectile_collisions()
                    
                    for enemy in self.enemies[:]:
                        if enemy.move():
                            self.handle_enemy_reached_castle(enemy)
                            self.enemies.remove(enemy)
                    
                    self.check_level_complete()
                    self.game_time += dt
                
                if self.game_over:
                    self.current_screen = 'game_over'
                    self.total_enemies_killed = self.enemies_killed
                    self.total_money_earned = self.money_from_enemies  # Використовуємо тільки гроші від ворогів
                
                # Оновлюємо активного улюbленця
                if self.active_pet:
                    if self.active_pet.type == 'guard':
                        # Логіка охоронця
                        self.active_pet.position = [self.castle_position[0] - 50, self.castle_position[1]]
                        if self.active_pet.can_shoot(current_time):
                            # Спочатку намагаємось знищити морквинки
                            for carrot in self.carrots[:]:
                                self.projectiles.append(
                                    Projectile(self.active_pet.position, carrot.position, self.active_pet.damage)
                                )
                                self.carrots.remove(carrot)
                                self.active_pet.last_shot_time = current_time
                                play_sound('carrot_destroy')  # Додаємо звук знищення морквинки
                                break
                            else:
                                # Якщо морквинок немає, стріляємо по ворогах
                                if self.enemies:
                                    target = self.enemies[0]  # Стріляємо в першого ворога
                                    self.projectiles.append(
                                        Projectile(self.active_pet.position, target.position, self.active_pet.damage)
                                    )
                                    self.active_pet.last_shot_time = current_time
                    else:
                        # Логіка збирачів
                        if self.active_pet.can_collect_carrots:
                            for carrot in self.carrots[:]:
                                dx = self.active_pet.position[0] - carrot.position[0]
                                dy = self.active_pet.position[1] - carrot.position[1]
                                if (dx**2 + dy**2)**0.5 < self.active_pet.size + carrot.size:
                                    self.active_pet.carrots_collected += 1
                                    self.total_carrots_collected += 1  # Збільшуємо загальний лічильник
                                    self.carrots.remove(carrot)
                                    # Зберігаємо новий результат
                                    with open('carrots.txt', 'w') as f:
                                        f.write(str(self.total_carrots_collected))
                        
                        if self.active_pet.can_collect_coins:
                            collected_coin = self.active_pet.move_to_coin(self.coins)
                            if collected_coin:
                                self.money += collected_coin.value
                                self.coins.remove(collected_coin)

            # Малювання
            if self.current_screen == 'menu':
                self.menu.draw(screen)
            elif self.current_screen == 'game':
                screen.fill(WHITE)
                self.draw_top_ui()
                self.draw_path()
                self.draw_tower_spots()
                self.draw_castle()
                
                for tower in self.towers:
                    tower.draw(screen, tower == self.selected_tower)
                
                for proj in self.projectiles:
                    proj.draw(screen)
                
                for coin in self.coins:
                    coin.draw(screen)
                
                for enemy in self.enemies:
                    enemy.draw(screen)
                
                self.draw_ui()
                
                # Показуємо повідомлення про початок рівня
                if self.level_starting:
                    remaining_time = int(self.level_start_delay - (current_time - self.level_start_time))
                    level_text = self.ui_font.render(f'Рівень {self.level} починається через {remaining_time}...', True, RED)
                    level_rect = level_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
                    screen.blit(level_text, level_rect)
                
                if self.paused:
                    pause_text = self.ui_font.render('ПАУЗА', True, RED)
                    pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
                    screen.blit(pause_text, pause_rect)
                
                if self.active_pet:
                    self.active_pet.draw(screen)
                
                for carrot in self.carrots:
                    carrot.draw(screen)
            elif self.current_screen == 'game_over':
                self.draw_game_over_screen()

            self.update()  # Додайте цей виклик для оновлення анімації

            pygame.display.flip() 