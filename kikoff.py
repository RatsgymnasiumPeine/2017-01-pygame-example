import time
import entities
from assets import assetManager
from entities import entityManager
import pygame
import sys


"""
Initialisierungsfunktion. Wird einmal beim Programmstart ausgefuehrt"""
def init():
    toLoad = [
        ("mainchar-r", "images/mainchar-r.png"),
        ("mainchar-l", "images/mainchar-l.png"),
        ("mainchar-n", "images/mainchar-n.png"),
        ("mainchar-j", "images/mainchar-j.png"),
        ("ball", "images/ball.png")
    ]
    for asset in toLoad:
        # Lade alle Assets in der Liste mit Lazy Loading
        assetManager.load(asset[0], asset[1], True)

    # Fuege einen Hauptcharacter zum Spielfeld hinzu
    entityManager.addEntity(entities.MainCharacter())

"""
Update Funktion, aktualisiert alle Entities
"""
def update(delta):
    entityManager.update(delta)

"""
Render Funktion, rendert alle Entities
"""
def render(screen):
    screen.fill((0, 0, 0))
    entityManager.render(screen)


# Pygame Initialisierung
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
time_a = time.time()
time_b = time.time()
# Fuehre Init aus
init()
while True:
    # Errechne Zeitdifferenz
    time_b = time_a
    time_a = time.time()
    # Fuehre Update Aus
    update(time_a - time_b)
    # Fuehre Render aus
    render(screen)
    # Flippe den Screen Buffer
    pygame.display.flip()
    clock.tick(60)
    # Regiere auf Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

