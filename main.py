import os
import sys
import pygame
import random as r
import time

size = width, height = 600, 600
clock = pygame.time.Clock()
screen = pygame.display.set_mode(size)
bullet_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()

fps = 100
v_enemy = 100
v_bullet = 500
enemy_time = pygame.USEREVENT + 1
enemy2_time = pygame.USEREVENT + 3
bullet_time = pygame.USEREVENT + 2
bullet_timing = 500
bullet_timing_enemy = 1.5
SCORE = 0
DAMAGE = 0
MONEY = 0
SCORE_LEVEL = 0
enemy_health = [2, 4]
enemy_timing = 1000
enemy2_timing = 10000


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def terminate():
    pygame.quit()
    sys.exit()


player_image = load_image('player.png')
enemy_image = load_image('enemy.png')
map_img = load_image('mysea.png')
bullet_image = load_image('bullet.png', -1)
enemy2_image = load_image('enemy2.png')


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group)
        self.image = player_image
        self.rect = self.image.get_rect()
        self.x = pos_x
        self.y = pos_y
        self.rect.x = self.x
        self.rect.y = self.y
        self.damage = 1
        self.double = False

    def move(self, n_x, n_y):
        self.x = n_x - 30
        self.y = n_y - 25
        self.rect.x = self.x
        self.rect.y = self.y
        if pygame.sprite.spritecollideany(self, enemy_group):
            return False
        return True

    def double_bullet(self):
        self.double = True

    def get_double(self):
        return not self.double

    def shooting(self):
        if self.double:
            Bullet(self.x + 15, self.y - 25, self.damage, bullet_group)
            Bullet(self.x + 45, self.y - 25, self.damage, bullet_group)
        else:
            Bullet(self.x + 30, self.y - 25, self.damage, bullet_group)

    def set_damage(self, a):
        self.damage += a

    def get_damage(self):
        return self.damage


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, health, image, money):
        super().__init__(enemy_group)
        self.image = image
        self.rect = self.image.get_rect()
        self.x = pos_x
        self.y = pos_y
        self.rect.x = self.x
        self.rect.y = self.y
        self.health = health
        self.money = money
        self.times = time.time() + bullet_timing_enemy

    def shooting(self):
        cl = time.time()
        if self.times <= cl:
            Bullet(self.rect.x + 27, self.rect.y + 55, 1, enemy_group, y=False)
            self.times += bullet_timing_enemy

    def update(self):
        self.rect = self.rect.move(0, v_enemy / fps)
        if enemy_health[1] == self.health:
            self.shooting()
        sprite = pygame.sprite.spritecollideany(self, bullet_group)
        if sprite:
            self.health -= sprite.get_damage()
            sprite.kill()
            if self.health <= 0:
                self.kill()
                global SCORE
                SCORE += self.money
        if self.rect.x > 600:
            self.kill()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, damage, group, y=True):
        super().__init__(group)
        self.image = bullet_image
        self.rect = self.image.get_rect()
        self.x = pos_x
        self.y = pos_y
        self.rect.x = self.x
        self.rect.y = self.y
        self.damage = damage
        self.player = y

    def update(self):
        a = 1 if self.player else -1
        self.rect = self.rect.move(0, -v_bullet * a / fps)
        if self.rect.x > 600:
            self.kill()

    def get_damage(self):
        return self.damage


class Game:
    def __init__(self):
        self.speed = 1
        self.damage = 1
        self.level = 1

    def draw_up(self):
        font = pygame.font.Font(None, 30)
        text = font.render(f"Score: {SCORE} Money: {MONEY} Level: {self.level}", True, (0, 0, 0))
        text1 = font.render(f"Speed: {self.speed} Damage: {self.damage}", True, (0, 0, 0))
        screen.blit(text, (10, 10))
        screen.blit(text1, (350, 10))

    def up_speed(self):
        self.speed = round(self.speed * 1.1, 2)

    def up_damage(self):
        self.damage += 1

    def get_speed(self):
        return self.speed > 50

    def up_level(self):
        self.level += 1


def start_screen():
    fon = load_image('start.jpg')
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 100)
    text = font.render(f"Игра Planes", True, (255, 255, 255))
    screen.blit(text, (100, 500))
    font = pygame.font.Font(None, 30)
    text = font.render(f"Клавиша 1 + 1 урон 1 монета", True, (255, 255, 255))
    screen.blit(text, (10, 10))
    text = font.render(f"Клавиша 2 + скорость выстрела 1 монета", True, (255, 255, 255))
    screen.blit(text, (10, 30))
    text = font.render(f"Клавиша 3 спецспособность 5 монет", True, (255, 255, 255))
    screen.blit(text, (10, 50))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(100)


def finish_screen(score):
    fon = load_image('finish.png')
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 60)
    text = font.render(f"Вы проиграли", True, (255, 255, 255))
    text1 = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(text, (100, 500))
    screen.blit(text1, (100, 450))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        pygame.display.flip()
        clock.tick(100)


def main():
    pygame.init()
    start_screen()
    p = Player(250, 500)
    g = Game()
    global DAMAGE, MONEY, bullet_timing, SCORE_LEVEL, enemy_timing, enemy2_timing
    player_group.draw(screen)
    pygame.time.set_timer(enemy_time, enemy_timing)
    pygame.time.set_timer(enemy2_time, enemy2_timing)
    pygame.time.set_timer(bullet_time, bullet_timing)
    running = True
    finish_game = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEMOTION:
                up = p.move(event.pos[0], event.pos[1])
                if not up:
                    running = False
                    finish_game = True
            if event.type == enemy_time:
                Enemy(r.randrange(550), 0, enemy_health[0], enemy_image, 1)
            if event.type == enemy2_time:
                Enemy(r.randrange(550), 0, enemy_health[1], enemy2_image, 4)
                Enemy(r.randrange(550), 0, enemy_health[1], enemy2_image, 4)
            if event.type == bullet_time:
                p.shooting()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_1:
                    if MONEY > 0:
                        g.up_damage()
                        MONEY -= 1
                        p.set_damage(1)
                if not g.get_speed():
                    if event.key == pygame.K_2:
                        if MONEY >= 1:
                            g.up_speed()
                            MONEY -= 1
                            bullet_timing = int(bullet_timing / 1.1)
                            pygame.time.set_timer(bullet_time, bullet_timing)
                if p.get_double():
                    if event.key == pygame.K_3:
                        if MONEY >= 5:
                            p.double_bullet()
                            MONEY -= 5
                if event.key == pygame.K_0:
                    MONEY = 100
        if SCORE // 10 > DAMAGE // 10:
            if DAMAGE != SCORE:
                DAMAGE = SCORE
                MONEY += 1
        if SCORE // 20 > SCORE_LEVEL // 20:
            if SCORE_LEVEL != SCORE:
                SCORE_LEVEL = SCORE
                if SCORE // 20 % 2 == 0:
                    for i in range(len(enemy_health)):
                        enemy_health[i] = enemy_health[i] * 2
                else:
                    enemy2_timing = int(enemy2_timing / 1.1)
                    enemy_timing = int(enemy_timing / 1.1)
                g.up_level()
        screen.blit(map_img, (0, 0))
        player_group.draw(screen)
        enemy_group.draw(screen)
        enemy_group.update()
        bullet_group.draw(screen)
        bullet_group.update()
        g.draw_up()
        pygame.display.flip()
        clock.tick(fps)
    if finish_game:
        finish_screen(SCORE)
    pygame.quit()


if __name__ == '__main__':
    main()
