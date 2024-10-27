import pygame
import sys
import time
from model import Map, Unit, Building

# Constants for the game
tile_size = 40
screen_width = 1600
screen_height = 900


# Load images for the game
def load_images():
    wood_img = pygame.image.load('images/wood.png').convert_alpha()
    gold_img = pygame.image.load('images/gold.png').convert_alpha()
    town_center_img = pygame.image.load('images/town_center.png').convert_alpha()
    villager_img = pygame.image.load('images/villager.png').convert_alpha()
    farm_img = pygame.image.load('images/farm.png').convert_alpha()  # Load farm image
    grass_img = pygame.image.load('images/grass.png').convert_alpha()  # Load grass image

    # Resize images to match the tile size
    wood_img = pygame.transform.scale(wood_img, (tile_size, tile_size))
    gold_img = pygame.transform.scale(gold_img, (tile_size, tile_size))
    town_center_img = pygame.transform.scale(town_center_img, (tile_size, tile_size))
    villager_img = pygame.transform.scale(villager_img, (tile_size, tile_size))
    farm_img = pygame.transform.scale(farm_img, (tile_size, tile_size))  # Resize farm image
    grass_img = pygame.transform.scale(grass_img, (tile_size, tile_size))  # Resize grass image

    return {
        'Wood': wood_img,
        'Gold': gold_img,
        'Town Center': town_center_img,
        'Villager': villager_img,
        'Farm': farm_img,  # Include farm image in the dictionary
        'Grass': grass_img
    }


# Function to initialize graphics when needed
def initialize_graphics():
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("RTS Game")
    return screen

# Render the game map on the screen
def render_map(screen, game_map, units, buildings, view_x, view_y, max_width, max_height):
    screen.fill((0, 0, 0))  # Clear screen with black color
    images = load_images()

    # Render visible portion of the map
    for y in range(view_y, min(view_y + max_height, game_map.height)):
        for x in range(view_x, min(view_x + max_width, game_map.width)):
            tile = game_map.grid[y][x]
            tile_pos = (x - view_x) * tile_size, (y - view_y) * tile_size  # Adjust position based on view

            # Display grass for empty tiles
            screen.blit(images['Grass'], tile_pos)

            # Display resources
            if tile.resource == 'Wood':
                screen.blit(images['Wood'], tile_pos)
            elif tile.resource == 'Gold':
                screen.blit(images['Gold'], tile_pos)

            # Display buildings
            if tile.building:
                if tile.building.building_type == 'Town Center':
                    screen.blit(images['Town Center'], tile_pos)
                elif tile.building.building_type == 'Farm':
                    screen.blit(images['Farm'], tile_pos)  # Display farm
                elif tile.building.building_type == 'Barracks':
                    # Add more buildings here, for example, barracks if needed
                    pass

    # Render units
    for unit in units:
        if view_x <= unit.x < view_x + max_width and view_y <= unit.y < view_y + max_height:
            unit_pos = (unit.x - view_x) * tile_size, (unit.y - view_y) * tile_size
            screen.blit(images['Villager'], unit_pos)

    pygame.display.flip()  # Update the screen

def handle_input_pygame(view_x, view_y,max_width, max_height, game_map):
    """Gère les touches ZQSD pour le scrolling en mode Pygame."""
    keys = pygame.key.get_pressed()

    # Gérer le défilement en fonction des touches pressées
    if keys[pygame.K_z]:
        view_y = max(0, view_y - 1)
        print(f"[DEBUG] Moving up, view_y: {view_y}")
    if keys[pygame.K_s]:
        view_y = min(game_map.height - max_height, view_y + 1)
        print(f"[DEBUG] Moving down, view_y: {view_y}")
    if keys[pygame.K_q]:
        view_x = max(0, view_x - 1)
        print(f"[DEBUG] Moving left, view_x: {view_x}")
    if keys[pygame.K_d]:
        view_x = min(game_map.width - max_width, view_x + 1)
        print(f"[DEBUG] Moving right, view_x: {view_x}")

    return view_x, view_y
