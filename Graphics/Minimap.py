import pygame
from pygame import SRCALPHA


class Minimap:
    def __init__(self, tilemap, screen, scale_factor, position):
        self.tilemap = tilemap
        self.scale_factor = scale_factor
        self.position = position

        # Dimensions de la minimap
        screen_width, screen_height = screen.get_size()
        self.minimap_width, self.minimap_height = [dim for dim in self.tilemap.size]
        self.image = pygame.Surface((self.minimap_width + (0.15 * screen_width), self.minimap_height + (0.15 * screen_height)))
        self.update_minimap()

    def update_minimap(self):
        """
        Met à jour la minimap avec la taille adaptée, fond transparent, et affichage correct.
        """
        # Calcul de la taille de la minimap en fonction de la taille de la tilemap
        tilemap_width = self.tilemap.image.get_width()
        tilemap_height = self.tilemap.image.get_height()

        # Application de l'échelle et du zoom
        minimap_width = int(tilemap_width * self.scale_factor)
        minimap_height = int(tilemap_height * self.scale_factor)

        # Création d'une surface transparente
        self.image = pygame.Surface((minimap_width, minimap_height//2), pygame.SRCALPHA)
        # self.image.fill((0, 0, 0, 0))  # Fond transparent

        # Redimensionnement de l'image de la tilemap
        scaled_tilemap = pygame.transform.scale(
            self.tilemap.image, (minimap_width, minimap_height)
        )

        # Affichage de l'image redimensionnée sur la minimap
        self.image.blit(scaled_tilemap, (0, 0))

    def draw(self, screen):
        """
        Affiche la minimap sur l'écran.
        """
        screen.blit(self.image, self.position)
