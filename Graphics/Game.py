import pygame
import numpy as np
import Tileset
import Tilemap

# Classe principale du jeu
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("Tilemap Example")
        self.running = True
        self.clock = pygame.time.Clock()

        # Charger le tileset
        tileset_file = '../assets/Fantasy_Tileset/spritesheet.png'  # Remplace par ton fichier de tileset
        self.tileset = Tileset.Tileset(tileset_file, size=(32, 32), margin=0, spacing=0)

        # Créer une tilemap
        self.tilemap = Tilemap.Tilemap(self.tileset, size=(120, 120))  # Carte de 120x120
        self.tilemap.set_random()  # Générer une carte aléatoire

    # Redimensionne la tilemap selon le facteur de zoom
    def draw_tilemap(self):
        zoomed_image = pygame.transform.scale(
            self.tilemap.image,
            (int(self.tilemap.image.get_width() * self.tilemap.zoom_factor),
             int(self.tilemap.image.get_height() * self.tilemap.zoom_factor))
        )
        # Dessiner la tilemap zoomée sur l'écran
        self.screen.blit(zoomed_image, (0, 0))

    def draw_move_map(self):
        """
        Dessine la tilemap déplacée en fonction des coordonnées de self.tilemap.rect.
        """
        # Créer une surface zoomée si un zoom est appliqué
        zoomed_image = pygame.transform.scale(
            self.tilemap.image,
            (int(self.tilemap.image.get_width() * self.tilemap.zoom_factor),
             int(self.tilemap.image.get_height() * self.tilemap.zoom_factor)))

        # Calculer la position pour centrer la map dans la fenêtre
        map_x = (self.screen.get_width() - zoomed_image.get_width()) // 2
        map_y = (self.screen.get_height() - zoomed_image.get_height()) // 2

        # Ajouter le décalage dû au déplacement
        map_x += self.tilemap.rect.x
        map_y += self.tilemap.rect.y

        # Dessiner l'image déplacée
        self.screen.blit(zoomed_image, (map_x, map_y))

    def run(self):
        # Limite le déplacement pour ne pas sortir de la map
        max_x = self.tilemap.image.get_width() - self.tilemap.rect.width
        max_y = self.tilemap.image.get_height() - self.tilemap.rect.height
        self.tilemap.rect.x = max(0, min(self.tilemap.rect.x, max_x))
        self.tilemap.rect.y = max(0, min(self.tilemap.rect.y, max_y))

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # Recharger une carte aléatoire
                        self.tilemap.set_random()
                    elif event.key == pygame.K_a:  # Réinitialiser la carte
                        self.tilemap.set_normal()
                        self.tilemap.set_random_overlay(probability=0.05)
                    elif event.key == pygame.K_p:  # Touche "+" pour zoomer
                        self.screen.fill((0, 0, 0))
                        self.tilemap.set_zoom(self.tilemap.zoom_factor + 0.1)
                    elif event.key == pygame.K_m:  # Touche "-" pour dézoomer
                        self.screen.fill((0, 0, 0))
                        self.tilemap.set_zoom(self.tilemap.zoom_factor - 0.1)
                    elif event.key == pygame.K_z:
                        self.tilemap.rect.y += 100
                    elif event.key == pygame.K_s:
                        self.tilemap.rect.y -= 100
                    elif event.key == pygame.K_d:
                        self.tilemap.rect.x -= 100
                    elif event.key == pygame.K_q:
                        self.tilemap.rect.x += 100

            # Dessiner la carte
            self.screen.fill((0, 0, 0))  # Fond noir
            map_x = (self.screen.get_width() - self.tilemap.image.get_width()) // 2
            map_y = 0  # Optionnellement, ajuste verticalement
            # self.screen.blit(self.tilemap.image, (map_x, map_y)) Commenté pour n'afficher que la map gérant le zoom
            self.draw_move_map()  # Affiche la map avec zoom
            pygame.display.flip()
            self.clock.tick(30)

        pygame.quit()

# Lancer le jeu
if __name__ == "__main__":
    game = Game()
    game.run()