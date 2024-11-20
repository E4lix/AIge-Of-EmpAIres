import pygame
import numpy as np

# Chargement de Tileset
class Tileset:
    def __init__(self, file, size=(64, 64), margin=0, spacing=0):
        self.file = file
        self.size = size
        self.margin = margin
        self.spacing = spacing
        self.image = pygame.image.load(file)
        self.rect = self.image.get_rect()
        self.tiles = []
        self.load()

    def load(self):
        self.tiles = []
        x0 = y0 = self.margin
        w, h = self.rect.size
        dx = self.size[0] + self.spacing
        dy = self.size[1] + self.spacing

        for x in range(x0, w, dx):
            for y in range(y0, h, dy):
                tile = pygame.Surface(self.size, pygame.SRCALPHA)
                tile.blit(self.image, (0, 0), (x, y, *self.size))
                self.tiles.append(tile)

    def __str__(self):
        return f'{self.__class__.__name__} file:{self.file} tile:{self.size}'


# Classe Tilemap
class Tilemap:
    def __init__(self, tileset, size=(10, 20), rect=None):
        self.size = size
        self.tileset = tileset
        self.map = np.zeros(size, dtype=int)

        h, w = self.size
        self.image = pygame.Surface((64 * w, 64 * h))
        if rect:
            self.rect = pygame.Rect(rect)
        else:
            self.rect = self.image.get_rect()

        # Liste d'éléments supplémentaires (bâtiments, arbres, etc.)
        self.elements = []

    # Récupérer la position d'une case pour y afficher la bonne tile
    def get_tile_for_position(self, i, j):
        """
        Détermine la tuile à afficher en fonction de la position (i, j).
        """
        # Récupère la taille de la carte
        m, n = self.size

        # Vérifie si la position (i, j) est un coin
        if i == 0 and j == 0:
            return self.tileset.tiles[0]  # Coin supérieur gauche
        elif i == 0 and j == n - 1:
            return self.tileset.tiles[8]  # Coin supérieur droit
        elif i == m - 1 and j == 0:
            return self.tileset.tiles[2]  # Coin inférieur gauche
        elif i == m - 1 and j == n - 1:
            return self.tileset.tiles[10]  # Coin inférieur droit

        # Vérifie si la position (i, j) est sur un bord, mais pas aux coins
        if i == 0:
            return self.tileset.tiles[4]  # Bord supérieur
        elif i == m - 1:
            return self.tileset.tiles[6] # Bord inférieur
        elif j == 0:
            return self.tileset.tiles[1]  # Bord gauche
        elif j == n - 1:
            return self.tileset.tiles[9] # Bord droit

        # Si c'est une case du centre
        return self.tileset.tiles[5]  # Centre

    # Render une map aléatoire
    def render(self):
        m, n = self.map.shape
        for i in range(m):
            for j in range(n):
                tile = self.tileset.tiles[self.map[i, j]]
                self.image.blit(tile, (j * 64, i * 64))

    # Render une map avec respect des textures de coins et côtés
    def render_normal(self):
        m, n = self.map.shape
        for i in range(m):
            for j in range(n):
                tile = self.get_tile_for_position(i, j)
                self.image.blit(tile, (j * 64, i * 64))

    def set_zero(self):
        self.map = np.zeros(self.size, dtype=int)
        self.render()

    def set_mid(self):
        self.render_normal()

    def set_random(self):
        n = len(self.tileset.tiles)
        self.map = np.random.randint(n, size=self.size)
        self.render()

    def __str__(self):
        return f'{self.__class__.__name__} {self.size}'

# Class Element
class Element:
    def __init__(self, image_file, position):
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect(topleft=position)

    def draw(self, surface):
        surface.blit(self.image, self.rect)


# Classe principale du jeu
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 960))
        pygame.display.set_caption("Tilemap Example")
        self.running = True
        self.clock = pygame.time.Clock()

        # Charger le tileset
        tileset_file = 'assets/Tiny_Swords/Terrain/Ground/Tilemap_Flat.png'  # Remplace par ton fichier de tileset
        self.tileset = Tileset(tileset_file, size=(64, 64), margin=0, spacing=0)

        # Créer une tilemap
        self.tilemap = Tilemap(self.tileset, size=(15, 20))  # Carte de 15x20
        self.tilemap.set_mid()  # Générer une carte aléatoire

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # Recharger une carte aléatoire
                        self.tilemap.set_random()
                    elif event.key == pygame.K_z:  # Réinitialiser la carte
                        self.tilemap.set_zero()
                    elif event.key == pygame.K_m: # Charge une carte avec la tile milieu
                        self.tilemap.set_mid()

            # Dessiner la carte
            self.screen.fill((0, 0, 0))  # Fond noir
            self.screen.blit(self.tilemap.image, (0, 0))  # Afficher la tilemap
            pygame.display.flip()
            self.clock.tick(30)

        pygame.quit()


# Lancer le jeu
if __name__ == "__main__":
    game = Game()
    game.run()
