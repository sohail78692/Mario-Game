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

# Camera offset
camera_x = 0

# Ground & platforms in world space
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

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    # Move Left/Right
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed

    # Jump
    if keys[pygame.K_SPACE] and not is_jumping:
        player_y_velocity = -10
        is_jumping = True

    # Gravity
    player_y_velocity += gravity
    player_y += player_y_velocity

    # Player rect
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)

    # Collision with ground
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
        print("Game Over!")
        pygame.quit()
        sys.exit()

    # Camera movement (scroll world)
    if player_x - camera_x > WIDTH // 2:
        camera_x = player_x - WIDTH // 2

    # Drawing
    screen.fill((135, 206, 235))  # sky

    screen.blit(mario_img, (player_x - camera_x, player_y))  # Mario

    # Ground
    pygame.draw.rect(screen, (0, 255, 0),
                     (ground_rect.x - camera_x, ground_rect.y, ground_rect.width, ground_rect.height))

    # Platforms
    for platform in platforms:
        pygame.draw.rect(screen, (139, 69, 19),
                         (platform.x - camera_x, platform.y, platform.width, platform.height))

    # Draw Enemy
    pygame.draw.rect(screen, (255, 255, 0),
                     (enemy_rect.x - camera_x, enemy_rect.y, enemy_rect.width, enemy_rect.height))

    pygame.display.update()
    clock.tick(60)
