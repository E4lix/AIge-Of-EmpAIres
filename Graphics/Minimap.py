import pygame

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
        self.image.fill((0, 0, 0))  # Réinitialise l'image de la minimap
        for i in range(self.tilemap.size[0]):
            for j in range(self.tilemap.size[1]):
                tile = self.tilemap.tileset.tiles[self.tilemap.map[i, j]]
                x, y = self.tilemap.iso_to_screen(i, j)
                minimap_x = int(x * self.scale_factor)
                minimap_y = int(y * self.scale_factor)

                # Appliquer un zoom sur chaque tuile
                tile_width, tile_height = self.tilemap.tileset.size
                zoomed_tile = pygame.transform.scale(tile, (
                int(tile_width * self.scale_factor), int(tile_height * self.scale_factor)))
                self.image.blit(zoomed_tile, (minimap_x, minimap_y))

    def draw(self, screen):
        """Affiche la minimap sur l'écran."""
        screen.blit(self.image, self.position)
