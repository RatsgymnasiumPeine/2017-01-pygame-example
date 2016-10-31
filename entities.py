from assets import assetManager
import pygame
import math

"""
Entity Manager kuemmert sich um alle Entities im Spiel. Dazu zaehlt das updaten und rendern
der EntityManager ueberprueft auch, ob es sich ueberhaupt um ein Entity handelt wenn es hinzugefuegt wird.
"""
class EntityManager(object):
    """
    Initialisierung. erstellt ein leeres Array um Entites zu speichern
    """
    def __init__(self):
        self._entities = []

    """
    Fuegt ein Entity zur Liste der Entities hinzu. Prueft ob es sich wirklich um ein Entity handelt
    """
    def addEntity(self, entity):
        if(isinstance(entity, Entity)):
            print "Added Entity to Manager:", entity
            self._entities.append(entity)
        else:
            print "EntityEngine: tried to add non entity: ", entity

    """
    Loescht ein Entity aus der Liste der Entities"""
    def removeEntity(self, entity):
        print "Removed Entity from Manager:", entity
        self._entities.remove(entity)

    """
    Updatemethode iteriert ueber jedes Entity und fuehrt dessen Updatemethode aus
    delta:   Zeit seit letztem update in Sekunden
    """
    def update(self, delta):
        for entity in self._entities:
            entity.update(delta)

    """
    Render methode iteriert ueber jedes Entity und fuehrt dessen Rendermethode aus
    """
    def render(self, screen):
        for entity in self._entities:
            entity.render(screen)



# Variable fuer den EntityManager die im ganzen Programm benutzt werden kann und auf die gleiche Instanz zeigt (Singleton)
entityManager = EntityManager()

"""
Basisklasse Entity
Enthaelt allgemeine Informationen, die jedes Entity haben sollte (x,y,vx,vy)
"""
class Entity(object):
    """
    Konstruktor der Basisklasse
    """
    def __init__(self):
        # Setzt die Basiswerte auf 0
        self.x = 0
        self.y = 0
        self.vx = 0
        self.vy = 0

    """
    Updatemethode
    """
    def update(self, delta):
        # Fuehrt rudimentaere physikalische Operationen durch
        self.vy += 2000 * delta
        self.x += self.vx * delta
        self.y += self.vy * delta

    """
    Rendermethode
    sollte ueberschrieben werden
    """
    def render(self, screen):
        pass


class MainCharacter(Entity):
    """
    Konstruktor der Klasse MainCharacter
    """
    def __init__(self):
        Entity.__init__(self)
        # Ist bereit fuer einen Schuss
        self.shootready = True
        # X - Position in der Mitte des Bildschirms setzen
        self.x = 1280/2

    def render(self, screen):
        # Wenn der Betrag der y-Geschwindigkeit > 0
        if math.fabs(self.vy) > 0:
            # Zeichne Jumpbild
            screen.blit(assetManager.get("mainchar-j"), (self.x - 64, self.y - 64))

        # Wenn die x-Geschwindigkeit = 0
        elif self.vx == 0:
            # Zeichne Neutralbild
            screen.blit(assetManager.get("mainchar-n"), (self.x - 64, self.y - 64))

        # Wenn die x-Geschwindikeit > 0
        elif self.vx > 0:
            # Zeichne Linksbild
            screen.blit(assetManager.get("mainchar-r"), (self.x - 64, self.y - 64))

        # Wenn die x-Geschwindikeit < 0
        elif self.vx < 0:
            # Zeichne Rechtsbild
            screen.blit(assetManager.get("mainchar-l"), (self.x - 64, self.y - 64))


    """
    Updatemethode der Klasse MainCharacter"""
    def update(self, delta):
        # Fuehre update der Entityklasse aus
        Entity.update(self,delta)

        # Wenn y-Koordinate > 500, setze y auf 500 und die y-Geschwindikeit auf 0
        # Einfache Fallbegrenzung
        if self.y > 500:
            self.y = 500
            self.vy = 0

        # Wenn x-Koordinate > 1280, setze x auf 1280
        # Einfache Gehbegrenzung nach rechts
        if self.x > 1280:
            self.x = 1280

        # Wenn x-Koordinate < 0, setze x auf 0
        # Einfache Gehbegrenzung nach links
        if self.x < 0:
            self.x = 0

        # Hole den Zustand aller Tasten
        keypressed = pygame.key.get_pressed()

        # Wenn D gedrueckt, aber nicht A
        if   keypressed[pygame.K_d] and not keypressed[pygame.K_a]:
            self.vx = 500
        # Wenn A gedrueckt, aber nicht D
        elif keypressed[pygame.K_a] and not keypressed[pygame.K_d]:
            self.vx = -500
        # Wenn beide gedrueckt, oder keine
        else:
            self.vx = 0

        # Wenn Leertaste gedrueckt
        if keypressed[pygame.K_SPACE] and self.vy  == 0:
            self.vy = -1000

        # Wenn E gedrueckt
        if keypressed[pygame.K_e]:
            # Wenn Schuss bereit
            if self.shootready:
                # Erzeuge neues Entity Ball
                b = Ball()
                # Setze Attribute des Balls
                b.x = self.x
                b.y = self.y
                b.vx = 2 * self.vx
                if b.vx == 0:
                    b.vy = -2000
                # Fuege den Ball dem EntityManager hinzu
                entityManager.addEntity(b)
                # Schuss ist nun nicht mehr bereit
                self.shootready = False
        else:
            # Wenn E nicht mehr gedrueckt ist der naechste Schuss bereit
            self.shootready = True


"""
Klasse Ball
"""
class Ball(Entity):
    """
    Konstruktor der Klasse Ball
    """
    def __init__(self):
        # Ruft Entity Konstruktor auf
        Entity.__init__(self)
        # Setzt einen Timer auf 60
        self.timer = 60

    """
    Update Methode der Klasse Ball
    """
    def update(self, delta):
        # Ruft Entity Updatemethode auf
        Entity.update(self, delta)
        # Berechnet den Timer neu
        self.timer -= delta
        # Wenn Timer abgelaufen, entferne sich selbst aus dem EntityManager
        if self.timer < 0:
            entityManager.removeEntity(self)

        # Wenn y-Koordinate > 564, setze y auf 564 und invertiere y-Geschwindikeit (Abpralleffekt)
        if self.y > 564:
            self.y = 564
            self.vy *= -1

        # Wenn x-Koordinate < 0, setze x auf 0 und invertiere x-Geschwindikeit mit dem Faktor 0.5 (Abpralleffekt mit verringerung der Geschwindigkeit)
        if self.x < 0:
            self.x = 0
            self.vx *= -0.5

        # Wenn x-Koordinate > 1280, setze x auf 1280 und invertiere x-Geschwindikeit mit dem Faktor 0.5 (Abpralleffekt mit verringerung der Geschwindigkeit)
        if self.x > 1280:
            self.x = 1280
            self.vx *= -0.5

    """
    Rendermethode der Klasse Ball
    """
    def render(self, screen):
        # Zeichne den Ball
        screen.blit(assetManager.get("ball"), (self.x - 32, self.y - 32))
