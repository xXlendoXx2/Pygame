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
BLUE = (0, 0, 255)

# Fonts
font = pygame.font.Font(None, 36)
game_over_font = pygame.font.Font(None, 72)

# Player settings
player_size = 30
player_x, player_y = WIDTH // 2, HEIGHT // 2
player_speed = 6
sprint_speed = 9
player_health = 3  # Player health

# Bullets
bullets = []
bullet_speed = 9
bullet_cooldown = 575
last_shot_time = 0

# Zombies
zombies = []
zombie_size = 40
base_zombie_speed = 4.25
spawn_rate = 400
last_spawn_time = 0

# Waves
wave = 1
zombies_spawned = 0
zombies_per_wave = 5
wave_ongoing = True

# Game states
show_tutorial = True  # New tutorial screen flag
game_over = False

def spawn_zombie():
    global zombies_spawned
    if zombies_spawned < zombies_per_wave:
        side = random.choice(["left", "right", "top", "bottom"])
        if side == "left":
            x, y = 0, random.randint(0, HEIGHT)
        elif side == "right":
            x, y = WIDTH, random.randint(0, HEIGHT)
        elif side == "top":
            x, y = random.randint(0, WIDTH), 0
        else:
            x, y = random.randint(0, WIDTH), HEIGHT
        
        zombies.append({"x": x, "y": y, "speed": base_zombie_speed})
        zombies_spawned += 1

def move_zombies():
    for zombie in zombies:
        dx, dy = player_x - zombie["x"], player_y - zombie["y"]
        dist = math.hypot(dx, dy)
        if dist != 0:
            zombie["x"] += (dx / dist) * zombie["speed"]
            zombie["y"] += (dy / dist) * zombie["speed"]

def move_bullets():
    global bullets
    for bullet in bullets:
        bullet[0] += bullet[2] * bullet_speed
        bullet[1] += bullet[3] * bullet_speed
    bullets = [b for b in bullets if 0 <= b[0] <= WIDTH and 0 <= b[1] <= HEIGHT]

def check_collisions():
    global zombies, bullets, player_health, wave_ongoing, zombies_spawned
    for bullet in bullets[:]:
        for zombie in zombies[:]:
            if abs(bullet[0] - zombie["x"]) < zombie_size // 2 and abs(bullet[1] - zombie["y"]) < zombie_size // 2:
                zombies.remove(zombie)
                bullets.remove(bullet)
                break
    
    for zombie in zombies[:]:
        if abs(zombie["x"] - player_x) < player_size and abs(zombie["y"] - player_y) < player_size:
            player_health -= 1
            zombies.remove(zombie)
            if player_health <= 0:
                return False
    
    if not zombies and zombies_spawned >= zombies_per_wave:
        wave_ongoing = False
    return True

def draw():
    screen.fill(WHITE)
    pygame.draw.rect(screen, GREEN, (player_x, player_y, player_size, player_size))
    for bullet in bullets:
        pygame.draw.circle(screen, BLUE, (int(bullet[0]), int(bullet[1])), 5)
    for zombie in zombies:
        pygame.draw.rect(screen, RED, (zombie["x"], zombie["y"], zombie_size, zombie_size))
    
    wave_text = font.render(f"Wave: {wave}", True, BLACK)
    screen.blit(wave_text, (10, 10))
    health_text = font.render(f"Health: {player_health}", True, BLACK)
    screen.blit(health_text, (10, 40))
    
    pygame.display.flip()

def game_over_screen():
    screen.fill(WHITE)
    game_over_text = game_over_font.render("GAME OVER", True, RED)
    screen.blit(game_over_text, (WIDTH // 2 - 150, HEIGHT // 3))
    wave_text = font.render(f"You reached wave {wave}", True, BLACK)
    screen.blit(wave_text, (WIDTH // 2 - 100, HEIGHT // 2))
    restart_text = font.render("Press R to Restart or Q to Quit", True, BLACK)
    screen.blit(restart_text, (WIDTH // 2 - 180, HEIGHT // 1.5))
    pygame.display.flip()

def tutorial_screen():
    screen.fill(WHITE)
    title_text = game_over_font.render("Zombie Shooter", True, BLACK)
    screen.blit(title_text, (WIDTH // 2 - 180, HEIGHT // 6))

    instructions = [
        "WASD - Move",
        "SHIFT - Sprint",
        "Auto-shoots at nearest zombie",
        "Survive as long as possible!",
        "Press SPACE to start"
    ]
    
    y_offset = HEIGHT // 3
    for instruction in instructions:
        text = font.render(instruction, True, BLACK)
        screen.blit(text, (WIDTH // 2 - 150, y_offset))
        y_offset += 40

    pygame.display.flip()

def reset_game():
    global player_x, player_y, player_health, bullets, zombies, wave, zombies_spawned, zombies_per_wave, wave_ongoing, spawn_rate, last_shot_time, show_tutorial, game_over
    player_x, player_y = WIDTH // 2, HEIGHT // 2
    player_health = 3
    bullets = []
    zombies = []
    wave = 1
    zombies_spawned = 0
    zombies_per_wave = 5
    wave_ongoing = True
    spawn_rate = 400
    last_shot_time = 0  # Reset shooting cooldown
    show_tutorial = True  # Show tutorial again
    game_over = False

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if show_tutorial:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                show_tutorial = False  # Hide tutorial and start game
        elif game_over:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game()
                elif event.key == pygame.K_q:
                    running = False
    
    if show_tutorial:
        tutorial_screen()
    elif not game_over:
        if wave_ongoing:
            keys = pygame.key.get_pressed()
            current_speed = sprint_speed if keys[pygame.K_LSHIFT] else player_speed
            
            if keys[pygame.K_w] and player_y > 0:
                player_y -= current_speed
            if keys[pygame.K_s] and player_y < HEIGHT - player_size:
                player_y += current_speed
            if keys[pygame.K_a] and player_x > 0:
                player_x -= current_speed
            if keys[pygame.K_d] and player_x < WIDTH - player_size:
                player_x += current_speed

            now = pygame.time.get_ticks()
            if now - last_shot_time > bullet_cooldown and zombies:
                nearest_zombie = min(zombies, key=lambda z: math.hypot(z["x"] - player_x, z["y"] - player_y))
                dx, dy = nearest_zombie["x"] - player_x, nearest_zombie["y"] - player_y
                dist = math.hypot(dx, dy)
                if dist != 0:
                    bullets.append([player_x, player_y, dx / dist, dy / dist])
                    last_shot_time = now

            move_bullets()
            move_zombies()
            game_over = not check_collisions()
            if pygame.time.get_ticks() - last_spawn_time > spawn_rate:
                spawn_zombie()
        else:
            wave += 1
            zombies_per_wave += 5
            wave_ongoing = True
        draw()
    else:
        game_over_screen()
    
    clock.tick(60)

pygame.quit()
