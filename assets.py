import pygame

"""
Assetmanager verwaltet alle Bilder, Sounds etc.
"""
class AssetManager(object):
    """
    Konstruktor der Klasse AssetManager
    """
    def __init__(self):
        # Assets Map fuer fertig geladene Assets
        self._assets = {}
        # Lazy Map fuer just in time zu ladende Assets
        self._lazy = {}

    """
    Laedt ein Asset
    """
    def load(self, name, path, lazy):
        if lazy:
            # Wenn lazy loading
            print "Lazy loading \"" + name + "\" with file", path
            self._lazy[name] = path
        else:
            # Sofortiges laden des Assets
            try:
                print "Loading \"" + name + "\" with file", path
                self._assets[name] = pygame.image.load(path)
            except pygame.error as e:
                print e

    def get(self, name):
        if name in self._assets:
            # Asset wurde schon geladen, gebe es zurueck
            return self._assets[name]
        else:
            # Asset noch nicht geladen
            if name in self._lazy:
                # Asset befindet sich aber in der Lazy liste
                # Lade es sofort und gebe es zurueck
                self.load(name, self._lazy[name], False)
                return self.get(name)
            else:
                # Weder in Asset Liste noch in Lazy Liste
                print "AssetManager: Tried to load assets: ", name

# Variable assetManager die programmweit benutzt werden kann und auf die gleiche Instanz zeigt (Singleton)
assetManager = AssetManager()