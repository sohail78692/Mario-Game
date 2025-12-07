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

# Load Mario sprite
mario_img = pygame.image.load("mario.png")
mario_img = pygame.transform.scale(mario_img, (player_width, player_height))

# Load  Sound Effects
jump_sound = pygame.mixer.Sound("jump.mp3")
coin_sound = pygame.mixer.Sound("coin.mp3")
game_over_sound = pygame.mixer.Sound("gameover.mp3")

# Camera offset
camera_x = 0

# Ground & platforms
ground_rect = pygame.Rect(0, 560, 3000, 40)
platforms = [
    pygame.Rect(200, 450, 120, 20),
    pygame.Rect(500, 350, 120, 20),
    pygame.Rect(900, 300, 120, 20),
    pygame.Rect(1300, 400, 120, 20),
    pygame.Rect(1700, 350, 120, 20)
]

# Enemy setup
enemy_width = 40
enemy_height = 40
enemy_x = 600
enemy_y = 520
enemy_speed = 2
enemy_direction = 1
enemy_rect = pygame.Rect(enemy_x, enemy_y, enemy_width, enemy_height)

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

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    # Movement controls
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed

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

    # Platform collision
    for platform in platforms:
        if player_rect.colliderect(platform) and player_y_velocity > 0:
            player_y = platform.top - player_height
            player_y_velocity = 0
            is_jumping = False

    # Enemy movement
    enemy_x += enemy_speed * enemy_direction
    if enemy_x < 550 or enemy_x > 750:
        enemy_direction *= -1
    enemy_rect.x = enemy_x
    enemy_rect.y = enemy_y

    # Collision with enemy
    if player_rect.colliderect(enemy_rect):
        game_over_sound.play()
        pygame.time.delay(1000)
        print("Game Over!")
        pygame.quit()
        sys.exit()

    # Coin collection
    for coin in coins[:]:
        if player_rect.colliderect(coin):
            coins.remove(coin)
            score += 1
            coin_sound.play()

    # Camera scroll
    if player_x - camera_x > WIDTH // 2:
        camera_x = player_x - WIDTH // 2

    # Drawing
    screen.fill((135, 206, 235))

    # Background art
    pygame.draw.circle(screen, (255, 255, 0), (100 - camera_x // 10, 100), 40)

    pygame.draw.circle(screen, (255, 255, 255), (300 - camera_x // 5, 120), 30)
    pygame.draw.circle(screen, (255, 255, 255), (330 - camera_x // 5, 130), 25)
    pygame.draw.circle(screen, (255, 255, 255), (360 - camera_x // 5, 120), 30)

    pygame.draw.circle(screen, (255, 255, 255), (700 - camera_x // 5, 160), 35)
    pygame.draw.circle(screen, (255, 255, 255), (740 - camera_x // 5, 150), 25)
    pygame.draw.circle(screen, (255, 255, 255), (780 - camera_x // 5, 160), 30)

    pygame.draw.ellipse(screen, (34, 139, 34), (100 - camera_x // 2, 450, 300, 200))
    pygame.draw.ellipse(screen, (34, 139, 34), (600 - camera_x // 2, 470, 400, 250))

    screen.blit(mario_img, (player_x - camera_x, player_y))

    pygame.draw.rect(screen, (0, 255, 0), (ground_rect.x - camera_x, ground_rect.y, ground_rect.width, ground_rect.height))
    for platform in platforms:
        pygame.draw.rect(screen, (139, 69, 19), (platform.x - camera_x, platform.y, platform.width, platform.height))

    pygame.draw.rect(screen, (255, 255, 0), (enemy_rect.x - camera_x, enemy_rect.y, enemy_rect.width, enemy_rect.height))

    for coin in coins:
        pygame.draw.circle(screen, (255, 215, 0), (coin.x - camera_x + 10, coin.y + 10), 10)

    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (20, 20))

    pygame.display.update()
    clock.tick(60)
