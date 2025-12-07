import pygame
import sys

pygame.init()

# Window setup
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mario Game")

clock = pygame.time.Clock()

# Player properties
player_x = 100
player_y = 500
player_width = 40
player_height = 60
player_speed = 5
player_y_velocity = 0
gravity = 0.5
is_jumping = False

# Load Mario animation frames
mario_frames = [
    pygame.transform.scale(pygame.image.load("mario1.png"), (player_width, player_height)),
    pygame.transform.scale(pygame.image.load("mario2.png"), (player_width, player_height)),
    pygame.transform.scale(pygame.image.load("mario3.png"), (player_width, player_height))
]
current_frame = 0
frame_delay = 0

# Load sounds
jump_sound = pygame.mixer.Sound("jump.mp3")
coin_sound = pygame.mixer.Sound("coin.mp3")
game_over_sound = pygame.mixer.Sound("gameover.mp3")

# Load heart image
heart_img = pygame.transform.scale(pygame.image.load("heart.png"), (30, 30))

# Camera
camera_x = 0

# Ground
ground_rect = pygame.Rect(0, 560, 3000, 40)

# Moving platforms: [x, y, width, height, speed, direction, min_x, max_x]
platforms = [
    [200, 450, 120, 20, 0, 0, 200, 200],
    [500, 350, 120, 20, 2, 1, 500, 700],
    [900, 300, 120, 20, 0, 0, 900, 900],
    [1300, 400, 120, 20, 3, 1, 1300, 1500],
    [1700, 350, 120, 20, 0, 0, 1700, 1700]
]

# Enemies: [x, y, speed, direction]
enemies = [
    [600, 520, 2, 1],
    [1100, 520, 2, -1],
    [1600, 520, 3, 1]
]

enemy_width = 40
enemy_height = 40

# Coins
coins = [
    pygame.Rect(250, 400, 20, 20),
    pygame.Rect(550, 300, 20, 20),
    pygame.Rect(950, 250, 20, 20),
    pygame.Rect(1350, 350, 20, 20),
    pygame.Rect(1750, 300, 20, 20)
]

score = 0
font = pygame.font.SysFont("Arial", 30)

# Lives system
lives = 3
game_over = False

# Win flag
flag_rect = pygame.Rect(2800, 420, 30, 140)
won = False

# ================= GAME LOOP ==================
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # ---------- GAME OVER SCREEN ----------
    if game_over:
        screen.fill((0, 0, 0))
        over_text = font.render("GAME OVER!", True, (255, 0, 0))
        restart_text = font.render("Press R to Restart", True, (255, 255, 255))
        screen.blit(over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 20))
        screen.blit(restart_text, (WIDTH // 2 - 130, HEIGHT // 2 + 20))
        pygame.display.update()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            # Reset full game
            player_x = 100
            player_y = 500
            score = 0
            lives = 3
            camera_x = 0
            coins = [
                pygame.Rect(250, 400, 20, 20),
                pygame.Rect(550, 300, 20, 20),
                pygame.Rect(950, 250, 20, 20),
                pygame.Rect(1350, 350, 20, 20),
                pygame.Rect(1750, 300, 20, 20)
            ]
            game_over = False
        continue

    keys = pygame.key.get_pressed()
    moving = False

    # Movement
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
        moving = True
    if keys[pygame.K_RIGHT]:
        player_x += player_speed
        moving = True

    # Jump
    if keys[pygame.K_SPACE] and not is_jumping:
        player_y_velocity = -10
        is_jumping = True
        jump_sound.play()

    # Gravity
    player_y_velocity += gravity
    player_y += player_y_velocity

    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)

    # Ground collision
    if player_rect.colliderect(ground_rect):
        player_y = ground_rect.top - player_height
        player_y_velocity = 0
        is_jumping = False

    # ---------- Moving Platforms ----------
    for p in platforms:
        p[0] += p[4] * p[5]
        if p[0] < p[6] or p[0] > p[7]:
            p[5] *= -1

        platform_rect = pygame.Rect(p[0], p[1], p[2], p[3])

        if player_rect.colliderect(platform_rect) and player_y_velocity > 0:
            player_y = p[1] - player_height
            player_y_velocity = 0
            is_jumping = False
            player_x += p[4] * p[5]

    # ---------- Animation ----------
    if moving:
        frame_delay += 1
        if frame_delay >= 5:
            current_frame = (current_frame + 1) % 3
            frame_delay = 0
    else:
        current_frame = 0

    # ---------- Enemies ----------
    for enemy in enemies:
        enemy[0] += enemy[2] * enemy[3]
        if enemy[0] < 550:
            enemy[3] = 1
        if enemy[0] > 1800:
            enemy[3] = -1

        enemy_rect = pygame.Rect(enemy[0], enemy[1], enemy_width, enemy_height)

        if player_rect.colliderect(enemy_rect):
            lives -= 1
            game_over_sound.play()
            pygame.time.delay(700)

            player_x = 100
            player_y = 500
            player_y_velocity = 0
            camera_x = 0  # FIX: reset camera!

            if lives <= 0:
                game_over = True

    # ---------- Coins ----------
    for coin in coins[:]:
        if player_rect.colliderect(coin):
            coins.remove(coin)
            score += 1
            coin_sound.play()

    # ---------- Win ----------
    if player_rect.colliderect(flag_rect):
        won = True

    if won:
        screen.fill((255, 255, 255))
        win_text = font.render("YOU WIN!", True, (0, 0, 0))
        screen.blit(win_text, (WIDTH // 2 - 80, HEIGHT // 2))
        pygame.display.update()
        pygame.time.delay(3000)
        pygame.quit()
        sys.exit()

    # ---------- Camera scrolling ----------
    if player_x - camera_x > WIDTH // 2:
        camera_x = player_x - WIDTH // 2

    # ---------- DRAWING ----------
    screen.fill((135, 206, 235))  # sky

    pygame.draw.circle(screen, (255, 255, 0), (100 - camera_x // 10, 100), 40)

    screen.blit(mario_frames[current_frame], (player_x - camera_x, player_y))

    pygame.draw.rect(screen, (0, 255, 0),
                     (ground_rect.x - camera_x, ground_rect.y, ground_rect.width, ground_rect.height))

    for p in platforms:
        pygame.draw.rect(screen, (139, 69, 19),
                         (p[0] - camera_x, p[1], p[2], p[3]))

    for enemy in enemies:
        pygame.draw.rect(screen, (255, 255, 0),
                         (enemy[0] - camera_x, enemy[1], enemy_width, enemy_height))

    for coin in coins:
        pygame.draw.circle(screen, (255, 215, 0),
                           (coin.x - camera_x + 10, coin.y + 10), 10)

    pygame.draw.rect(screen, (255, 0, 0),
                     (flag_rect.x - camera_x, flag_rect.y, flag_rect.width, flag_rect.height))
    pygame.draw.circle(screen, (255, 255, 255),
                       (flag_rect.x - camera_x + 15, flag_rect.y), 15)

    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (20, 20))

    for i in range(lives):
        screen.blit(heart_img, (20 + i * 35, 60))

    pygame.display.update()
    clock.tick(60)
