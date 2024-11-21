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
        self.objects = []  # Liste des objets uniques
        self.map = np.zeros(size, dtype=int) # Carte du terrain de la map

        h, w = self.size
        self.image = pygame.Surface((64 * w, 64 * h))
        if rect:
            self.rect = pygame.Rect(rect)
        else:
            self.rect = self.image.get_rect()

    # Récupérer la position d'une case pour y afficher la bonne tile
    def get_tile_for_position(self, i, j):
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
        # Rendre les objets uniques
        for obj in self.objects:
            self.image.blit(obj.image, obj.position)

    # Render une map avec respect des textures de coins et côtés
    def render_normal(self):
        m, n = self.map.shape
        for i in range(m):
            for j in range(n):
                tile = self.get_tile_for_position(i, j)
                self.image.blit(tile, (j * 64, i * 64))
        # Rendre les objets uniques
        for obj in self.objects:
            self.image.blit(obj.image, obj.position)

    # Render une map avec uniquement la case du coin supérieur gauche
    def set_zero(self):
        self.map = np.zeros(self.size, dtype=int)
        self.render()

    # Render une map normal
    def set_mid(self):
        self.render_normal()

    # Render une map aléatoire
    def set_random(self):
        n = len(self.tileset.tiles)
        self.map = np.random.randint(n, size=self.size)
        self.render()

    # Ajouter des buissons aléatoirement
    def add_bushes(self, count):
        h, w = self.size
        available_positions = [(x, y) for x in range(h) for y in range(w)]
        np.random.shuffle(available_positions)  # Mélanger les positions
        positions = available_positions[:count]  # Sélectionner `count` positions

        for pos in positions:
            x, y = pos
            self.map[x, y] = 16  # Placer le buisson dans la carte

        self.render_normal()

    # Ajouter des objets
    def add_object(self, image_path, grid_position):
        x, y = grid_position
        pixel_position = (y * 64, x * 64)  # Convertit la position de la grille en pixels
        game_object = GameObject(image_path, pixel_position)
        self.objects.append(game_object)

        self.render_normal()

    def __str__(self):
        return f'{self.__class__.__name__} {self.size}'

# Class GameObject
class GameObject:
    def __init__(self, image_path, position):
        self.image = pygame.image.load(image_path).convert_alpha()  # Chargement avec transparence
        self.position = position  # Position en pixels (x, y)

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

        # Affiche la tilemap créé
        self.tilemap.set_mid()

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
                    elif event.key == pygame.K_m: # Charge une carte normale
                        self.tilemap.set_mid()
                    elif event.key == pygame.K_l:
                        self.tilemap.add_object('assets/Tiny_Swords/Factions/Knights/Buildings/House/House_Blue.png',
                                                (5, 5))
                        self.tilemap.add_object('assets/Tiny_Swords/Factions/Knights/Buildings/House/House_Blue.png',
                                                (6, 8))
                        self.tilemap.set_mid()
                    elif event.key == pygame.K_b:  # Ajouter des buissons
                        self.tilemap.add_bushes(count=20)  # Indices des tuiles buissons





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
