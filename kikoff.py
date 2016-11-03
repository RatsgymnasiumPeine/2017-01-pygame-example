import time
import entities
from assets import assetManager
from entities import entityManager
import pygame
import sys


class Game(object):
    """
        Initialisierungsmethode. Wird einmal beim Programmstart ausgefuehrt
    """
    def __init__(self):
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

        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()
        self.time_a = time.time()
        self.time_b = time.time()

        
    """
        Update Methode, aktualisiert alle Entities
    """
    def update(self, delta):
        entityManager.update(delta)
        

    """
        Render Methode, rendert alle Entities
    """
    def render(self):
        self.screen.fill((0, 0, 0))
        entityManager.render(self.screen)

    """
        Die Loop
    """
    def loop(self):
        # Errechne Zeitdifferenz
        self.time_b = self.time_a
        self.time_a = time.time()
        # Fuehre Update Aus
        self.update(self.time_a - self.time_b)
        # Fuehre Render aus
        self.render()
        # Flippe den Screen Buffer
        pygame.display.flip()
        self.clock.tick(60)
        # Regiere auf Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()




game = Game()
while True:
    game.loop()
    

