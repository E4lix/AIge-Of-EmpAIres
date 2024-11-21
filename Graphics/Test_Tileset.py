import pygame

# Initialisation de Pygame
pygame.init()

file = '../assets/Fantasy_Tileset/spritesheet.png'

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
                tile = pygame.Surface(self.size)
                tile.blit(self.image, (0, 0), (x, y, *self.size))
                self.tiles.append(tile)

    def __str__(self):
        return f'{self.__class__.__name__} file:{self.file} tile:{self.size}'

# Création d'un Tileset
tileset = Tileset(file, size=(32, 32), margin=0, spacing=0)

# Affichage des informations du Tileset
print(tileset)

# Vérification du nombre de tuiles chargées
print(f"Nombre de tuiles : {len(tileset.tiles)}")

# Affichage de la première tuile (à titre d'exemple)
screen = pygame.display.set_mode((640, 480))
screen.blit(tileset.tiles[0], (100, 100))
screen.blit(tileset.tiles[0], (116, 116))
pygame.display.flip()

# Attente pour voir le résultat
pygame.time.wait(5000)
pygame.quit()
