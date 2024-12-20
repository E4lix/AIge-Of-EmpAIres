import pygame
import numpy as np

# Classe Tilemap
class Tilemap:
    def __init__(self, tileset, size, rect=None):
        self.size = size # Taille de la map
        self.tileset = tileset # Tileset utilisé pour les textures de la map
        self.map = np.zeros(size, dtype=int) # Matrice des coordonnées de la map
        self.overlay_map = np.full(size, -1, dtype=int) # Matrice des coordonnées de l'overlay décor

        self.zoom_factor = 1.0  # Facteur de zoom (1.0 = taille normale)

        self.floor_tile = [2, 13, 24] # Liste des tiles pour le sol
        self.decor_set = [48, 59, 70, 81, 92] # Liste des tiles pour le décor

        h, w = self.size
        self.image = pygame.Surface((32 * w + 32, 32 * h - 32)) # + 32 car sinon il manque une demi case à droite
        if rect:
            self.rect = pygame.Rect(rect)
        else:
            self.rect = self.image.get_rect()

    def set_zoom(self, zoom):
        """
        Gère le niveau de zoom sur la map

        Args:
            zoom: float représentant le niveau de zoom
        """
        self.zoom_factor = max(0.1, zoom)  # Évite un zoom trop petit ou négatif

    # Convertit les coordonnées de la grille en coordonnées pour les textures isométriques
    def iso_to_screen(self, i, j):
        """
        Calcul les coordonnées des élements entrée pour les convertir en coordonnées isométriques

        Args:
            i: Abscisse de l'élément
            j: Ordonné de l'élément

        Return:
            int: Abscisse et Ordonné en coordonnées isométriques
        """
        tile_width, tile_height = self.tileset.size
        x = (i - j) * (tile_width // 2)
        y = (i + j) * (tile_height // 4)
        return x, y

    # Render une map aléatoire
    def render_random(self):
        """
        Génère une map avec des tiles sélectionnées aléatoirement
        """
        m, n = self.map.shape
        self.image.fill((0, 0, 0, 0))  # Efface l'image précédente avec de la transparence
        for i in range(m):
            for j in range(n):
                tile = self.tileset.tiles[self.map[i, j]]
                screen_x, screen_y = self.iso_to_screen(i, j)
                self.image.blit(tile, (screen_x + self.image.get_width() // 2, screen_y))

    # Render une map cohérente
    def render_normal(self, floor_tile):
        """
        Génère une map avec des tiles sélectionnées dans une liste cohérente pour les différents élements

        Args:
            floor_tile: Liste des tiles utilisées pour le sol
        """
        m, n = self.map.shape
        x_offset = -2 # Valeur trouvée à tâtons
        y_offset = -10 # Valeur trouvée à tâtons
        self.image.fill((0, 0, 0, 0))  # Efface l'image précédente avec de la transparence
            # Sol/Terrain
        for i in range(m):
            for j in range(n):
                tile = self.tileset.tiles[np.random.choice(floor_tile)] # Choisis une tile aléatoire parmi la liste proposée
                x, y = self.iso_to_screen(i, j) # Adapte les coordonnées à l'affichage iso
                self.image.blit(tile, (x + self.image.get_width() // 2, y))
            # Décor
        for i in range(m):
            for j in range(n):
                tile_index = self.overlay_map[i, j]
                if tile_index != -1:  # Vérifier qu'une tuile existe
                    overlay_tile = self.tileset.tiles[tile_index]
                    screen_x, screen_y = self.iso_to_screen(i ,j)
                    self.image.blit(overlay_tile, ((screen_x + x_offset) + self.image.get_width() // 2, screen_y + y_offset))

    # Spécifie le placement aléatoire de l'overlay décor
    def set_random_overlay(self, probability):
        """
        Génère des obstacles tiles d'objets placés aléatoirement sur la map

        Args:
            probability: Probabilité d'apparition d'un objet
        """
        m, n = self.overlay_map.shape
        for i in range(m):
            for j in range(n):
                if np.random.random() < probability:  # Probabilité d'ajouter une tuile
                    self.overlay_map[i, j] = np.random.choice(self.decor_set)
                else:
                    self.overlay_map[i, j] = -1  # Pas de tuile
        self.render_normal(self.floor_tile)

    # Crée une map cohérente
    def set_normal(self):
        """
        Crée et affiche une map cohérente
        """
        self.map = np.zeros(self.size, dtype=int)
        self.render_normal(self.floor_tile)

    # Crée une map randomisée
    def set_random(self):
        """
        Crée et affiche une map aléatoire
        """
        n = len(self.tileset.tiles)
        self.map = np.random.randint(n, size=self.size)
        self.render_random()

    def __str__(self):
        return f'{self.__class__.__name__} {self.size}'
