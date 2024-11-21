import pygame
import numpy as np

# Classe Tilemap
class Tilemap:
    def __init__(self, tileset, size, rect=None):
        self.size = size
        self.tileset = tileset
        self.map = np.zeros(size, dtype=int)
        self.overlay_map = np.full(size, -1, dtype=int)

        self.zoom_factor = 1.0  # Facteur de zoom (1.0 = taille normale)

        self.floor_tile = [2, 13, 24]
        self.decor_set = [4, 15, 26]

        h, w = self.size
        self.image = pygame.Surface((32 * w, 32 * h))
        if rect:
            self.rect = pygame.Rect(rect)
        else:
            self.rect = self.image.get_rect()

    def set_zoom(self, zoom):
        self.zoom_factor = max(0.1, zoom)  # Évite un zoom trop petit ou négatif

    # Convertit les coordonnées de la grille en coordonnées pour les textures isométriques
    def iso_to_screen(self, i, j):
        tile_width, tile_height = self.tileset.size
        x = (i - j) * (tile_width // 2)
        y = (i + j) * (tile_height // 4)
        return x, y

    # Render une map aléatoire
    def render_random(self):
        m, n = self.map.shape
        self.image.fill((0, 0, 0, 0))  # Efface l'image précédente avec de la transparence
        for i in range(m):
            for j in range(n):
                tile = self.tileset.tiles[self.map[i, j]]
                screen_x, screen_y = self.iso_to_screen(i, j)
                self.image.blit(tile, (screen_x + self.image.get_width() // 2, screen_y))

    # Render une map cohérente
    def render_normal(self, floor_tile):
        m, n = self.map.shape
        x_offset = 0
        y_offset = -8
        self.image.fill((0, 0, 0, 0))  # Efface l'image précédente avec de la transparence
        # Sol/Terrain
        for i in range(m):
            for j in range(n):
                tile = self.tileset.tiles[np.random.choice(floor_tile)]
                screen_x, screen_y = self.iso_to_screen(i, j)
                self.image.blit(tile, (screen_x + self.image.get_width() // 2, screen_y))
        # Décor
        for i in range(m):
            for j in range(n):
                tile_index = self.overlay_map[i, j]
                if tile_index != -1:  # Vérifier qu'une tuile existe
                    overlay_tile = self.tileset.tiles[tile_index]
                    screen_x, screen_y = self.iso_to_screen(i ,j)
                    self.image.blit(overlay_tile, ((screen_x + x_offset) + self.image.get_width() // 2, screen_y + y_offset))

    def set_random_overlay(self, probability):
        m, n = self.overlay_map.shape
        for i in range(m):
            for j in range(n):
                if np.random.random() < probability:  # Probabilité d'ajouter une tuile
                    self.overlay_map[i, j] = np.random.choice(self.decor_set)
                else:
                    self.overlay_map[i, j] = -1  # Pas de tuile
        self.render_normal(self.floor_tile)

    def set_normal(self):
        self.map = np.zeros(self.size, dtype=int)
        self.render_normal(self.floor_tile)

    def set_random(self):
        n = len(self.tileset.tiles)
        self.map = np.random.randint(n, size=self.size)
        self.render_random()

    def __str__(self):
        return f'{self.__class__.__name__} {self.size}'
