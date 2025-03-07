import pygame
import math
import random

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Zombie Shooter")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Player settings
player_size = 40
player_x, player_y = WIDTH // 2, HEIGHT // 2
player_speed = 3

# Bullets
bullets = []
bullet_speed = 7.5
bullet_cooldown = 625  # milliseconds
last_shot_time = 0

# Zombies
zombies = []
zombie_size = 40
zombie_speed = 2.5
spawn_rate = 400  # milliseconds
last_spawn_time = 0

# Timer
start_time = pygame.time.get_ticks()
high_score = 0
last_score = 0

game_over = False

def spawn_zombie():
    side = random.choice(["left", "right", "top", "bottom"])
    if side == "left":
        x, y = 0, random.randint(0, HEIGHT)
    elif side == "right":
        x, y = WIDTH, random.randint(0, HEIGHT)
    elif side == "top":
        x, y = random.randint(0, WIDTH), 0
    else:
        x, y = random.randint(0, WIDTH), HEIGHT
    zombies.append([x, y])

def move_zombies():
    for zombie in zombies:
        dx, dy = player_x - zombie[0], player_y - zombie[1]
        dist = math.hypot(dx, dy)
        if dist != 0:
            zombie[0] += (dx / dist) * zombie_speed
            zombie[1] += (dy / dist) * zombie_speed

def move_bullets():
    global bullets
    for bullet in bullets:
        bullet[0] += bullet[2] * bullet_speed
        bullet[1] += bullet[3] * bullet_speed
    bullets = [b for b in bullets if 0 <= b[0] <= WIDTH and 0 <= b[1] <= HEIGHT]

def check_collisions():
    global zombies, bullets, game_over, high_score, last_score
    for bullet in bullets[:]:
        for zombie in zombies[:]:
            if abs(bullet[0] - zombie[0]) < zombie_size // 2 and abs(bullet[1] - zombie[1]) < zombie_size // 2:
                zombies.remove(zombie)
                bullets.remove(bullet)
                break
    for zombie in zombies:
        if abs(zombie[0] - player_x) < player_size and abs(zombie[1] - player_y) < player_size:
            game_over = True
            last_score = (pygame.time.get_ticks() - start_time) // 1000
            high_score = max(high_score, last_score)

def draw():
    screen.fill(WHITE)
    if game_over:
        font = pygame.font.Font(None, 50)
        text = font.render("You Died! Press R to Restart", True, RED)
        screen.blit(text, (WIDTH // 2 - 200, HEIGHT // 2 - 50))
        high_score_text = font.render(f"High Score: {high_score}s", True, BLACK)
        screen.blit(high_score_text, (WIDTH // 2 - 100, HEIGHT // 2))
        last_score_text = font.render(f"Your Score: {last_score}s", True, BLACK)
        screen.blit(last_score_text, (WIDTH // 2 - 100, HEIGHT // 2 + 40))
    else:
        pygame.draw.rect(screen, GREEN, (player_x, player_y, player_size, player_size))
        for bullet in bullets:
            pygame.draw.circle(screen, RED, (int(bullet[0]), int(bullet[1])), 5)
        for zombie in zombies:
            pygame.draw.rect(screen, RED, (zombie[0], zombie[1], zombie_size, zombie_size))
        
        # Display timer
        font = pygame.font.Font(None, 36)
        elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
        timer_text = font.render(f"Time: {elapsed_time}s", True, BLACK)
        screen.blit(timer_text, (WIDTH - 150, 10))
    pygame.display.flip()

# Game loop
running = True
clock = pygame.time.Clock()
while running:
    screen.fill(WHITE)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            player_x, player_y = WIDTH // 2, HEIGHT // 2
            zombies.clear()
            bullets.clear()
            game_over = False
            start_time = pygame.time.get_ticks()
    
    if not game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and player_y > 0:
            player_y -= player_speed
        if keys[pygame.K_s] and player_y < HEIGHT - player_size:
            player_y += player_speed
        if keys[pygame.K_a] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_d] and player_x < WIDTH - player_size:
            player_x += player_speed

        # Auto-shooting at the nearest zombie
        now = pygame.time.get_ticks()
        if now - last_shot_time > bullet_cooldown and zombies:
            nearest_zombie = min(zombies, key=lambda z: math.hypot(z[0] - player_x, z[1] - player_y))
            dx, dy = nearest_zombie[0] - player_x, nearest_zombie[1] - player_y
            dist = math.hypot(dx, dy)
            if dist != 0:
                bullets.append([player_x, player_y, dx / dist, dy / dist])
                last_shot_time = now

        move_bullets()
        move_zombies()
        check_collisions()
        
        now = pygame.time.get_ticks()
        if now - last_spawn_time > spawn_rate:
            spawn_zombie()
            last_spawn_time = now

    draw()
    clock.tick(60)

pygame.quit()
