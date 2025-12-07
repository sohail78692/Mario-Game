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

# Camera offset
camera_x = 0

# Load Mario sprite
mario_img = pygame.image.load("mario.png")
mario_img = pygame.transform.scale(mario_img, (player_width, player_height))

# Ground and platforms in world coordinates
ground_rect = pygame.Rect(0, 560, 3000, 40)  # long ground (3000px)

platforms = [
    pygame.Rect(200, 450, 120, 20),
    pygame.Rect(500, 350, 120, 20),
    pygame.Rect(900, 300, 120, 20),
    pygame.Rect(1300, 400, 120, 20),
    pygame.Rect(1700, 350, 120, 20)
]

# Game Loop
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

    # Apply gravity
    player_y_velocity += gravity
    player_y += player_y_velocity

    # Player collision rectangle
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

    # ---- Camera movement logic ----
    # Keep Mario near center of screen
    if player_x - camera_x > WIDTH // 2:
        camera_x = player_x - WIDTH // 2

    # Draw everything
    screen.fill((135, 206, 235))  # sky blue background

    # Draw Mario (adjusted by camera)
    screen.blit(mario_img, (player_x - camera_x, player_y))

    # Draw ground & platforms relative to camera
    pygame.draw.rect(screen, (0, 255, 0), (ground_rect.x - camera_x, ground_rect.y, ground_rect.width, ground_rect.height))

    for platform in platforms:
        pygame.draw.rect(screen, (139, 69, 19), (platform.x - camera_x, platform.y, platform.width, platform.height))

    pygame.display.update()
    clock.tick(60)
