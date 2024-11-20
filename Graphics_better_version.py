import pygame
import os

file = 'assets/Tiny_Swords/Terrain/Ground/Tilemap_Flat.png'

# Vérification de l'existence du fichier à ouvrir
if not os.path.exists(file):
    raise FileNotFoundError(f"Le fichier '{file}' est introuvable.")

# Chargement de l'image
image = pygame.image.load(file)
rect = image.get_rect()
print(image)

# Initialisation de Pygame
pygame.init()

# Configuration de la fenêtre
screen = pygame.display.set_mode(rect.size)
pygame.display.set_caption("AIge-of-EmpAIres")

# Affichage initial
screen.blit(image, rect)
pygame.display.flip()

# Boucle Principal
game_running = True
clock = pygame.time.Clock()

while game_running:
   for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False
   clock.tick(60)  # Limite à 60 FPS

pygame.quit()