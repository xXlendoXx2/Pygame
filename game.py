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

# High score file path
high_score_file = "high_score.txt"

# Function to load the high score
def load_high_score():
    try:
        with open(high_score_file, "r") as file:
            return int(file.read())
    except (FileNotFoundError, ValueError):
        return 0  # Return 0 if the file doesn't exist or the content is invalid

# Function to save the high score
def save_high_score(score):
    with open(high_score_file, "w") as file:
        file.write(str(score))

# Load the high score when the game starts
high_score = load_high_score()

# Player settings
player_size = 30
player_x, player_y = WIDTH // 2, HEIGHT // 2
player_speed = 5
sprint_speed = 8
stamina = 300
max_stamina = 300
stamina_recovery = 0.5
stamina_depletion = 1.5
is_sprinting = False

# Bullets
bullets = []
bullet_speed = 9
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
last_score = 0

game_over = False
in_menu = True
show_tutorial = False
show_buy_screen = False

# Function to spawn a zombie
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

# Function to move zombies
def move_zombies():
    for zombie in zombies:
        dx, dy = player_x - zombie[0], player_y - zombie[1]
        dist = math.hypot(dx, dy)
        if dist != 0:
            zombie[0] += (dx / dist) * zombie_speed
            zombie[1] += (dy / dist) * zombie_speed

# Function to move bullets
def move_bullets():
    global bullets
    for bullet in bullets:
        bullet[0] += bullet[2] * bullet_speed
        bullet[1] += bullet[3] * bullet_speed
    bullets = [b for b in bullets if 0 <= b[0] <= WIDTH and 0 <= b[1] <= HEIGHT]

# Function to check collisions
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
            save_high_score(high_score)  # Save high score whenever the game ends

# Function to draw everything on the screen
def draw():
    screen.fill(WHITE)
    if in_menu:
        draw_menu()
    elif show_tutorial:
        draw_tutorial()
    elif game_over:
        draw_game_over()
    else:
        draw_game()

    pygame.display.flip()

# Draw the menu screen
def draw_menu():
    font = pygame.font.Font(None, 50)
    title_text = font.render("Zombie Shooter", True, BLACK)
    start_text = font.render("Press 'Enter' to Start", True, BLACK)
    tutorial_text = font.render("Press 'T' for Tutorial", True, BLACK)
    buy_text = font.render("Press 'B' to Buy", True, BLACK)

    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))
    screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2 - 40))
    screen.blit(tutorial_text, (WIDTH // 2 - tutorial_text.get_width() // 2, HEIGHT // 2))
    screen.blit(buy_text, (WIDTH // 2 - buy_text.get_width() // 2, HEIGHT // 2 + 40))

# Draw the tutorial screen
def draw_tutorial():
    font = pygame.font.Font(None, 36)
    tutorial_text = [
        "Tutorial:",
        "W - Move Up",
        "A - Move Left",
        "S - Move Down",
        "D - Move Right",
        "Shift - Sprint",
        "ESC - Return to Menu"
    ]
    y_offset = 100
    for line in tutorial_text:
        text = font.render(line, True, BLACK)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, y_offset))
        y_offset += 40

# Draw the game over screen
def draw_game_over():
    font = pygame.font.Font(None, 50)
    text = font.render("You Died! Press R to Restart", True, RED)
    screen.blit(text, (WIDTH // 2 - 200, HEIGHT // 2 - 50))
    high_score_text = font.render(f"High Score: {high_score}s", True, BLACK)
    screen.blit(high_score_text, (WIDTH // 2 - 100, HEIGHT // 2))
    last_score_text = font.render(f"Your Score: {last_score}s", True, BLACK)
    screen.blit(last_score_text, (WIDTH // 2 - 100, HEIGHT // 2 + 40))

# Draw the game screen
def draw_game():
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

    # Draw stamina bar
    stamina_bar_width = 30
    stamina_bar_height = 10
    stamina_percentage = stamina / max_stamina
    pygame.draw.rect(screen, BLACK, (player_x - 0, player_y - 15, stamina_bar_width, stamina_bar_height))
    pygame.draw.rect(screen, BLUE, (player_x - 0, player_y - 15, stamina_bar_width * stamina_percentage, stamina_bar_height))

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if in_menu:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Start game
                    in_menu = False
                    start_time = pygame.time.get_ticks()
                elif event.key == pygame.K_t:  # Show tutorial
                    show_tutorial = True
                elif event.key == pygame.K_b:  # Buy (Placeholder)
                    show_buy_screen = True
                elif event.key == pygame.K_ESCAPE:  # Quit game
                    running = False
        elif show_tutorial:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                show_tutorial = False
                in_menu = True
        elif game_over:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:  # Restart the game
                player_x, player_y = WIDTH // 2, HEIGHT // 2
                zombies.clear()
                bullets.clear()
                game_over = False
                start_time = pygame.time.get_ticks()
                stamina = max_stamina  # Reset stamina on restart
                last_score = 0  # Reset the last score

    if not in_menu and not show_tutorial and not game_over:
        keys = pygame.key.get_pressed()

        # Sprinting logic
        is_sprinting = keys[pygame.K_LSHIFT] and stamina > 0
        current_speed = sprint_speed if is_sprinting else player_speed

        if keys[pygame.K_w] and player_y > 0:
            player_y -= current_speed
        if keys[pygame.K_s] and player_y < HEIGHT - player_size:
            player_y += current_speed
        if keys[pygame.K_a] and player_x > 0:
            player_x -= current_speed
        if keys[pygame.K_d] and player_x < WIDTH - player_size:
            player_x += current_speed

        # Manage stamina
        if is_sprinting:
            stamina = max(0, stamina - stamina_depletion)
        else:
            stamina = min(max_stamina, stamina + stamina_recovery)

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
