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

class Game:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.menu = Menu()
        self.current_screen = 'menu'
        
        # Додаємо змінні для керування ворогами
        self.enemies_per_level = 10
        self.enemies_spawned = 0
        self.enemies_killed = 0
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
            (SCREEN_WIDTH, SCREEN_HEIGHT * 0.2)
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
        self.ui_font = pygame.font.Font(None, int(36 * SCALE_FACTOR))
        
        # Гроші та вибрані об'єкти
        self.money = 1000
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
            SCREEN_WIDTH - 100 * SCALE_FACTOR,
            self.ui_y + 60 * SCALE_FACTOR,
            90 * SCALE_FACTOR,
            30 * SCALE_FACTOR
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

    def draw_path(self):
        if len(self.path_points) > 1:
            pygame.draw.lines(screen, BLACK, False, self.path_points, int(5 * SCALE_FACTOR))

    def draw_tower_spots(self):
        for spot in self.tower_spots:
            pygame.draw.circle(screen, GREEN, (int(spot[0]), int(spot[1])), 
                             int(20 * SCALE_FACTOR))

    def draw_top_ui(self):
        pygame.draw.rect(screen, GRAY, (0, 0, SCREEN_WIDTH, self.top_ui_height))
        
        time_text = self.ui_font.render(f'Час: {int(self.game_time)}с', True, BLACK)
        screen.blit(time_text, (10, 5))
        
        money_text = self.ui_font.render(f'Гроші: {self.money}', True, BLACK)
        screen.blit(money_text, (200 * SCALE_FACTOR, 5))
        
        level_text = self.ui_font.render(f'Рівень: {self.level}', True, BLACK)
        screen.blit(level_text, (400 * SCALE_FACTOR, 5))
        
        enemies_text = self.ui_font.render(
            f'Вороги: {self.enemies_killed}/{self.enemies_per_level}', 
            True, BLACK
        )
        screen.blit(enemies_text, (600 * SCALE_FACTOR, 5))

    def draw_ui(self):
        # Малюємо інтерфейс внизу екрану
        pygame.draw.rect(screen, GRAY, (0, self.ui_y, SCREEN_WIDTH, self.ui_height))
        
        # Малюємо кнопку меню
        pygame.draw.rect(screen, BLUE, self.menu_button, border_radius=int(5 * SCALE_FACTOR))
        menu_text = self.ui_font.render('Меню', True, WHITE)
        menu_rect = menu_text.get_rect(center=self.menu_button.center)
        screen.blit(menu_text, menu_rect)
        
        # Малюємо кнопку паузи
        pygame.draw.rect(screen, YELLOW, self.pause_button, border_radius=int(5 * SCALE_FACTOR))
        pause_text = self.ui_font.render('Пауза', True, BLACK)
        pause_rect = pause_text.get_rect(center=self.pause_button.center)
        screen.blit(pause_text, pause_rect)
        
        # Малюємо кнопки вибору типу вежі
        for button in self.tower_buttons:
            color = TOWER_PROPERTIES[button['type']]['color']
            
            # Підсвічування вибраного типу
            if self.selected_type == button['type']:
                # Малюємо підсвічування
                screen.blit(self.selected_type_highlight, 
                          (button['rect'].x - 10, button['rect'].y - 10))
                # Малюємо рамку
                pygame.draw.rect(screen, WHITE, button['rect'].inflate(20, 20), 3)
            
            # Малюємо кнопку
            pygame.draw.rect(screen, color, button['rect'])
            
            # Додаємо текст типу вежі
            type_text = self.ui_font.render(button['type'].title(), True, WHITE)
            text_rect = type_text.get_rect(center=button['rect'].center)
            screen.blit(type_text, text_rect)
            
            # Додаємо вартість
            cost = TOWER_PROPERTIES[button['type']]['cost']
            cost_text = self.ui_font.render(f'{cost}', True, WHITE)
            cost_rect = cost_text.get_rect(center=(button['rect'].centerx, 
                                                 button['rect'].bottom + 20))
            screen.blit(cost_text, cost_rect)
        
        # Малюємо інформацію про вибрану вежу та кнопку покращення
        if self.selected_tower:
            tower = self.selected_tower
            info_text = f"{TOWER_PROPERTIES[tower.type]['name']}, Рівень: {tower.level}, Вбито: {tower.kills}"
            if tower.level < 3:
                info_text += f", Ціна покращення: {tower.upgrade_cost}"
            tower_info = self.ui_font.render(info_text, True, BLACK)
            screen.blit(tower_info, (10, self.ui_y + 60))
            
            if tower.level < 3:
                pygame.draw.rect(screen, BLUE, self.upgrade_button)
                upgrade_text = self.ui_font.render('Покращити', True, WHITE)
                text_rect = upgrade_text.get_rect(center=self.upgrade_button.center)
                screen.blit(upgrade_text, text_rect)

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
                return True
        return False

    def update_projectiles(self):
        for proj in self.projectiles[:]:
            if proj.move():
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

    def check_projectile_collisions(self):
        """Перевіряє зіткнення снарядів з ворогами"""
        for proj in self.projectiles[:]:
            for enemy in self.enemies[:]:
                dx = enemy.position[0] - proj.position[0]
                dy = enemy.position[1] - proj.position[1]
                distance = (dx**2 + dy**2)**0.5
                
                if distance < enemy.size + proj.size:
                    if enemy.take_damage(proj.damage):
                        # Додаємо +1 до лічильника вбивств вежі, яка зробила постріл
                        for tower in self.towers:
                            if (tower.position[0] == proj.start_pos[0] and 
                                tower.position[1] == proj.start_pos[1]):
                                tower.kills += 1
                                break
                        
                        self.enemies.remove(enemy)
                        self.enemies_killed += 1
                        # Створюємо монетку з нагородою відповідно до типу ворога
                        self.coins.append(Coin(enemy.position, enemy.reward))
                    if proj in self.projectiles:
                        self.projectiles.remove(proj)

    def spawn_enemy(self):
        """Створює нового ворога з урахуванням поточного рівня"""
        if (self.enemies_spawned < self.enemies_per_level and 
            len(self.enemies) < 3):  # Максимум 3 ворога одночасно
            
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

    def check_level_complete(self):
        if (self.enemies_killed >= self.enemies_per_level and 
            len(self.enemies) == 0):
            self.level += 1
            # Оновлюємо рекорд якщо потрібно
            if self.level > self.record_level:
                self.record_level = self.level
                # Зберігаємо новий рекорд
                with open('record.txt', 'w') as f:
                    f.write(str(self.record_level))
            
            self.enemies_spawned = 0
            self.enemies_killed = 0
            self.enemies_per_level += 5

    def run(self):
        while True:
            current_time = time.get_ticks() / 1000.0
            dt = self.clock.tick(60) / 1000.0
            
            for e in event.get():
                if e.type == QUIT:
                    pygame.quit()
                    sys.exit()
                
                if e.type == MOUSEBUTTONDOWN:
                    if self.current_screen == 'menu':
                        action = self.menu.handle_click(e.pos)
                        if action == 'start':
                            self.current_screen = 'game'
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
                    elif self.current_screen == 'game':
                        if self.menu_button.collidepoint(e.pos):
                            self.current_screen = 'menu'
                        elif self.pause_button.collidepoint(e.pos):
                            self.paused = not self.paused
                        else:
                            # Перевіряємо клік по монетках
                            for coin in self.coins[:]:
                                dx = e.pos[0] - coin.position[0]
                                dy = e.pos[1] - coin.position[1]
                                if (dx**2 + dy**2)**0.5 < coin.size:
                                    self.money += coin.value
                                    self.coins.remove(coin)
                                    continue
                            
                            # Перевіряємо клік по кнопці покращення
                            if (self.selected_tower and 
                                self.upgrade_button.collidepoint(e.pos)):
                                # Перевіряємо чи можна покращити вежу
                                if (self.selected_tower.level < 3 and 
                                    self.money >= self.selected_tower.upgrade_cost):
                                    # Знімаємо гроші тільки якщо покращення успішне
                                    upgrade_cost = self.selected_tower.upgrade_cost
                                    if self.selected_tower.upgrade():
                                        self.money -= upgrade_cost
                            
                            # Перевіряємо клік по кнопках вибору типу вежі
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

            if self.current_screen == 'game' and not self.paused:
                self.spawn_enemy()
                self.update_towers(current_time)
                self.update_projectiles()
                self.check_projectile_collisions()
                
                for enemy in self.enemies[:]:
                    if enemy.move():
                        self.enemies.remove(enemy)
                
                self.check_level_complete()
                self.game_time += dt

            # Малювання
            if self.current_screen == 'menu':
                self.menu.draw(screen)
            elif self.current_screen == 'game':
                screen.fill(WHITE)
                self.draw_top_ui()
                self.draw_path()
                self.draw_tower_spots()
                
                for tower in self.towers:
                    tower.draw(screen, tower == self.selected_tower)
                
                for proj in self.projectiles:
                    proj.draw(screen)
                
                for coin in self.coins:
                    coin.draw(screen)
                
                for enemy in self.enemies:
                    enemy.draw(screen)
                
                self.draw_ui()
                
                if self.paused:
                    pause_text = self.ui_font.render('ПАУЗА', True, RED)
                    pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
                    screen.blit(pause_text, pause_rect)
            
            pygame.display.flip() 