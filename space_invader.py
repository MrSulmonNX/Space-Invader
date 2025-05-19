import pygame
import sys
import random

# 画面サイズ
WIDTH = 800
HEIGHT = 600

# 色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# プレイヤー
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 20))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speed_x = 0

    def update(self):
        self.speed_x = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speed_x = -5
        if keystate[pygame.K_RIGHT]:
            self.speed_x = 5
        self.rect.x += self.speed_x
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

# 弾
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((5, 10))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        # 画面外に出たら消滅
        if self.rect.bottom < 0:
            self.kill()

# インベーダー
class Invader(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 20))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_x = 2
        self.move_down = False
        self.move_timer = random.randint(30, 60)

    def update(self):
        self.rect.x += self.speed_x
        self.move_timer -= 1
        if self.move_timer == 0:
            self.move_down = True
            self.move_timer = random.randint(30, 60)

        if self.move_down:
            self.rect.y += 10
            self.speed_x *= -1
            self.move_down = False

        if self.rect.right > WIDTH or self.rect.left < 0:
            self.speed_x *= -1
            self.rect.y += 10

# Pygameの初期化
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")
clock = pygame.time.Clock()

# スプライトグループ
all_sprites = pygame.sprite.Group()
invaders = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

# インベーダーの作成
for i in range(8):
    for j in range(3):
        invader = Invader(50 + i * 70, 50 + j * 50)
        all_sprites.add(invader)
        invaders.add(invader)

# ゲームループ
running = True
while running:
    # イベント処理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    # ゲームの更新
    all_sprites.update()

    # 弾とインベーダーの衝突判定
    collisions = pygame.sprite.groupcollide(bullets, invaders, True, True)
    # プレイヤーとインベーダーの衝突判定
    if pygame.sprite.spritecollide(player, invaders, False):
        running = False # ゲームオーバー

    # 画面の描画
    screen.fill(BLACK)
    all_sprites.draw(screen)

    # 画面の更新
    pygame.display.flip()

    # フレームレートの維持
    clock.tick(60)

pygame.quit()
sys.exit()