import pygame

# Chargement de Tileset
class Tileset:
    def __init__(self, file, size, margin, spacing):
        self.file = file # Fichier du tileset
        self.size = size # Taille du tileset complet
        self.margin = margin # Marge externe entre les tiles
        self.spacing = spacing # Marge interne entre les tiles
        self.image = pygame.image.load(file) # Charge l'image dans pygame
        self.rect = self.image.get_rect() # Renvoie un rectangle correspondant aux dimensions et à la position de l'image
        self.tiles = [] # Liste des tiles du tileset
        self.load() # Charge le tileset

    def load(self):
        """
        Charge le fichier choisit pour le séparer en une liste de tiles numérotés colonnes par colonnes, lignes par lignes

        Return:
            list: Liste des tiles
        """
        self.tiles = []
        x0 = y0 = self.margin
        w, h = self.rect.size
        dx = self.size[0] + self.spacing
        dy = self.size[1] + self.spacing

        # On parcourt le tileset colonnes par colonnes, lignes par lignes.
        # Les tiles sont donc indexées de haut en bas puis de gauche à droite.
        for x in range(x0, w, dx):
            for y in range(y0, h, dy):
                tile = pygame.Surface(self.size, pygame.SRCALPHA) # Paramètres SRCALPHA pour transparence du fond des tiles
                tile.fill((0, 0, 0, 0))  # Efface tout pour garantir la transparence
                tile.blit(self.image, (0, 0), (x, y, *self.size))
                self.tiles.append(tile)

    def __str__(self):
        return f'{self.__class__.__name__} file:{self.file} tile:{self.size}'
