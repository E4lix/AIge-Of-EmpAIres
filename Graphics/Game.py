import pygame
import Tilemap
import Tileset
import Minimap

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1600, 900))
        pygame.display.set_caption("AIge of EmpAIres")
        self.running = True
        self.clock = pygame.time.Clock()

        # Charger le tileset
        tileset_file = '../assets/Fantasy_Tileset/spritesheet.png'
        self.tileset = Tileset.Tileset(tileset_file, size=(32, 32), margin=0, spacing=0)

        # Créer une tilemap
        self.tilemap = Tilemap.Tilemap(self.tileset, size=(60, 60))
        self.tilemap.set_random()  # Générer une carte aléatoire

        # Centrer la map au début
        self.map_x = 0
        self.map_y = 0

        # Créer une minimap
        self.minimap = Minimap.Minimap(self.tilemap, self.screen, scale_factor=0.75, position=(10, 10))

    def draw_tilemap(self):
        """Dessine la tilemap zoomée sur l'écran."""
        zoomed_image = pygame.transform.scale(
            self.tilemap.image,
            (int(self.tilemap.image.get_width() * self.tilemap.zoom_factor),
             int(self.tilemap.image.get_height() * self.tilemap.zoom_factor))
        )

        # Calcul du centre de la fenêtre
        screen_center_x = self.screen.get_width() // 2
        screen_center_y = self.screen.get_height() // 2

        # Calcul du décalage nécessaire pour centrer la carte zoomée sur la fenêtre
        zoomed_center_x = zoomed_image.get_width() // 2
        zoomed_center_y = zoomed_image.get_height() // 2

        # Appliquer le décalage pour centrer l'image zoomée
        map_x = screen_center_x - zoomed_center_x + self.map_x
        map_y = screen_center_y - zoomed_center_y + self.map_y

        # Dessiner la carte zoomée à la position calculée
        self.screen.blit(zoomed_image, (map_x, map_y))

    def draw_move_map(self):
        """Dessine la tilemap déplacée en fonction des coordonnées."""
        zoomed_image = pygame.transform.scale(
            self.tilemap.image,
            (int(self.tilemap.image.get_width() * self.tilemap.zoom_factor),
             int(self.tilemap.image.get_height() * self.tilemap.zoom_factor))
        )
        # Calcul du centre de la fenêtre
        screen_center_x = self.screen.get_width() // 2
        screen_center_y = self.screen.get_height() // 2

        # Calcul du décalage nécessaire pour centrer la carte zoomée sur la fenêtre
        zoomed_center_x = zoomed_image.get_width() // 2
        zoomed_center_y = zoomed_image.get_height() // 2

        # Appliquer le décalage pour centrer l'image zoomée
        map_x = screen_center_x - zoomed_center_x + self.map_x
        map_y = screen_center_y - zoomed_center_y + self.map_y

        # Dessiner la carte zoomée à la position calculée
        self.screen.blit(zoomed_image, (map_x, map_y))

    def run(self):
        max_x = self.tilemap.image.get_width() - self.tilemap.rect.width
        max_y = self.tilemap.image.get_height() - self.tilemap.rect.height
        self.tilemap.rect.x = max(0, min(self.tilemap.rect.x, max_x))
        self.tilemap.rect.y = max(0, min(self.tilemap.rect.y, max_y))

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.tilemap.set_random()
                    elif event.key == pygame.K_a:
                        self.tilemap.set_normal()
                        self.tilemap.set_random_overlay(probability=0.05)
                    elif event.key == pygame.K_p:
                        self.tilemap.set_zoom(self.tilemap.zoom_factor + 0.1)
                    elif event.key == pygame.K_m:
                        self.tilemap.set_zoom(self.tilemap.zoom_factor - 0.1)
                    elif event.key == pygame.K_z:
                        self.map_y += 100
                    elif event.key == pygame.K_s:
                        self.map_y -= 100
                    elif event.key == pygame.K_d:
                        self.map_x -= 100
                    elif event.key == pygame.K_q:
                        self.map_x += 100

            self.screen.fill((0, 0, 0))  # Fond noir
            self.draw_move_map()  # Affiche la map avec zoom

            # Met à jour et affiche la minimap
            self.minimap = Minimap.Minimap(self.tilemap, self.screen, scale_factor=0.75, position=(10, 10))
            self.minimap.draw(self.screen)  # Affiche la minimap
            pygame.display.flip()
            self.clock.tick(30)

        pygame.quit()

# Lancer le jeu
if __name__ == "__main__":
    game = Game()
    game.run()
