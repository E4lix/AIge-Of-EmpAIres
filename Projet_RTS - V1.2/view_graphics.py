import pygame #get.pressed quit
import sys
import time
from model import Map, Unit, Building

# Dimensions
tile_size = 40 # tuiles 
screen_width = 1600 
screen_height = 900

# Initialize PyGame
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("AIge of EmpAIres")

# Importation des sprites depuis le dossier 'images'
def load_images():
    wood_img = pygame.image.load('images/wood.png').convert_alpha()
    gold_img = pygame.image.load('images/gold.png').convert_alpha()
    town_center_img = pygame.image.load('images/town_center.png').convert_alpha()
    villager_img = pygame.image.load('images/villager.png').convert_alpha()
    farm_img = pygame.image.load('images/farm.png').convert_alpha()  
    grass_img = pygame.image.load('images/grass.png').convert_alpha() 

    # redimensionnement
    wood_img = pygame.transform.scale(wood_img, (tile_size, tile_size))
    gold_img = pygame.transform.scale(gold_img, (tile_size, tile_size))
    town_center_img = pygame.transform.scale(town_center_img, (tile_size, tile_size))
    villager_img = pygame.transform.scale(villager_img, (tile_size, tile_size))
    farm_img = pygame.transform.scale(farm_img, (tile_size, tile_size))  
    grass_img = pygame.transform.scale(grass_img, (tile_size, tile_size)) 

    return {
        'Wood': wood_img,
        'Gold': gold_img,
        'Town Center': town_center_img,
        'Villager': villager_img,
        'Farm': farm_img, 
        'Grass': grass_img
    }

# Afficher la map à l'écran (il y a surement de l'optimisation à faire par ici car à mon avis on calcul toutes les tuiles alors qu'on en voit qu'une partie)
def render_map(screen, game_map, units, buildings, view_x, view_y, max_width, max_height):
    screen.fill((0, 0, 0))  # Ecran noir
    images = load_images()

    # Affiche seulement une portion de la carte, c'est notre vu du jeu 
    for y in range(view_y, min(view_y + max_height, game_map.height)):
        for x in range(view_x, min(view_x + max_width, game_map.width)):
            tile = game_map.grid[y][x]
            tile_pos = (x - view_x) * tile_size, (y - view_y) * tile_size  # Adjust position based on view

            # Cases vide
            screen.blit(images['Grass'], tile_pos)

            # Cases ressources
            if tile.resource == 'Wood':
                screen.blit(images['Wood'], tile_pos)
            elif tile.resource == 'Gold':
                screen.blit(images['Gold'], tile_pos)

            # batiments
            if tile.building:
                if tile.building.building_type == 'Town Center':
                    screen.blit(images['Town Center'], tile_pos)
                elif tile.building.building_type == 'Farm':
                    screen.blit(images['Farm'], tile_pos)  # Display farm
                elif tile.building.building_type == 'Barracks':
                    # Add more buildings here, for example, barracks if needed
                    pass

    # Rendu unités
    for unit in units:
        if view_x <= unit.x < view_x + max_width and view_y <= unit.y < view_y + max_height: # l'unité est t-elle présente dans notre vu du jeu?
            unit_pos = (unit.x - view_x) * tile_size, (unit.y - view_y) * tile_size
            screen.blit(images['Villager'], unit_pos)

    pygame.display.flip()  # Update the screen

# Bouger la map
def handle_input_pygame(view_x, view_y, max_width, max_height, game_map):
    """Gère les touches ZQSD pour le scrolling en mode Pygame."""
    keys = pygame.key.get_pressed()

    if keys[pygame.K_z]:
        view_y = max(0, view_y - 1)
        print(f"Moving up, view_y: {view_y}")
    if keys[pygame.K_s]:
        view_y = min(game_map.height - max_height, view_y + 1)
        print(f"Moving down, view_y: {view_y}")
    if keys[pygame.K_q]:
        view_x = max(0, view_x - 1)
        print(f"Moving left, view_x: {view_x}")
    if keys[pygame.K_d]:
        view_x = min(game_map.width - max_width, view_x + 1)
        print(f"Moving right, view_x: {view_x}")

    return view_x, view_y


