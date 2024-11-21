import pygame
import numpy as np

# Chargement de Tileset
class Tileset:
    def __init__(self, file, size, margin, spacing):
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
                tile.fill((0, 0, 0, 0))  # Efface tout pour garantir la transparence
                tile.blit(self.image, (0, 0), (x, y, *self.size))
                self.tiles.append(tile)

    def __str__(self):
        return f'{self.__class__.__name__} file:{self.file} tile:{self.size}'


# Classe Tilemap
class Tilemap:
    def __init__(self, tileset, size, rect=None):
        self.size = size
        self.tileset = tileset
        self.map = np.zeros(size, dtype=int)

        h, w = self.size
        self.image = pygame.Surface((32 * w, 32 * h))
        if rect:
            self.rect = pygame.Rect(rect)
        else:
            self.rect = self.image.get_rect()

    # Convertit les coordonnées de la grille en coordonnées pour les textures isométriques
    def iso_to_screen(self, i, j):
        tile_width, tile_height = self.tileset.size
        x = (i - j) * (tile_width // 2)
        y = (i + j) * (tile_height // 4)
        return x, y

    # Render une map aléatoire
    def render(self):
        m, n = self.map.shape
        self.image.fill((0, 0, 0, 0))  # Efface l'image précédente avec de la transparence
        for i in range(m):
            for j in range(n):
                tile = self.tileset.tiles[self.map[i, j]]
                screen_x, screen_y = self.iso_to_screen(i, j)
                self.image.blit(tile, (screen_x + self.image.get_width() // 2, screen_y))

    def set_zero(self):
        self.map = np.zeros(self.size, dtype=int)
        self.render()

    def set_random(self):
        n = len(self.tileset.tiles)
        self.map = np.random.randint(n, size=self.size)
        self.render()

    def __str__(self):
        return f'{self.__class__.__name__} {self.size}'


# Classe principale du jeu
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 960))
        pygame.display.set_caption("Tilemap Example")
        self.running = True
        self.clock = pygame.time.Clock()

        # Charger le tileset
        tileset_file = '../assets/Fantasy_Tileset/spritesheet.png'  # Remplace par ton fichier de tileset
        self.tileset = Tileset(tileset_file, size=(32, 32), margin=0, spacing=0)

        # Créer une tilemap
        self.tilemap = Tilemap(self.tileset, size=(60, 60))  # Carte de 120x120
        self.tilemap.set_random()  # Générer une carte aléatoire

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

            # Dessiner la carte
            self.screen.fill((0, 0, 0))  # Fond noir
            map_x = (self.screen.get_width() - self.tilemap.image.get_width()) // 2
            map_y = 0  # Optionnellement, ajuste verticalement
            self.screen.blit(self.tilemap.image, (map_x, map_y))
            pygame.display.flip()
            self.clock.tick(30)

        pygame.quit()


# Lancer le jeu
if __name__ == "__main__":
    game = Game()
    game.run()
