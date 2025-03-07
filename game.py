import pygame

# Initialiserer Pygame
pygame.init()

# Skjermoppsett
BREDDE, HØYDE = 800, 600
skjerm = pygame.display.set_mode((BREDDE, HØYDE))

# Farger
HVIT = (255, 255, 255)
BLÅ = (0, 0, 255)

# Spillerens posisjon
spiller_x, spiller_y = 400, 275
spiller_fart = .2

# Spill-løkken
spillet_kjører = True
while spillet_kjører:
    skjerm.fill(HVIT)
    # Håndterer hendelser
    for hendelse in pygame.event.get():
        if hendelse.type == pygame.QUIT:
            spillet_kjører = False

    # Bevegelse med piltaster
    taster = pygame.key.get_pressed()
    if taster[pygame.K_LEFT]:
        spiller_x -= spiller_fart

    taster = pygame.key.get_pressed()
    if taster[pygame.K_RIGHT]:
        spiller_x += spiller_fart

    taster = pygame.key.get_pressed()
    if taster[pygame.K_DOWN]:
        spiller_y += spiller_fart

    taster = pygame.key.get_pressed()
    if taster[pygame.K_UP]:
        spiller_y -= spiller_fart
        
    # Tegne spilleren
    pygame.draw.rect(skjerm, BLÅ, (spiller_x, spiller_y, 50, 50))
    pygame.display.flip()

pygame.quit()
