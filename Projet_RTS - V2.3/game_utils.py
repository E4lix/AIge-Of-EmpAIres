import pickle
import os
from ai_strategies.base_strategies import AI

def save_game_state(units, buildings, game_map, ais, filename="saves/default_game.pkl"):
    with open(filename, "wb") as file:
        pickle.dump((units, buildings, game_map, ais), file)
    print(f"[INFO] Game saved to {filename}")

def load_game_state(filename="saves/default_game.pkl"):
    if os.path.exists(filename):
        try:
            with open(filename, "rb") as file:
                units, buildings, game_map, ais = pickle.load(file)

                # Réinitialiser les dictionnaires pour la carte
                game_map.tile_dict_resources = {}
                game_map.tile_dict_buildings = {}

                # Reindexer les ressources et bâtiments après chargement
                for y, row in enumerate(game_map.grid):
                    for x, tile in enumerate(row):
                        game_map.update_tile_index(x, y)

                print(f"[INFO] Game loaded from {filename}")
                return units, buildings, game_map, ais
        except Exception as e:
            print(f"[ERROR] Failed to load game: {e}")
    else:
        print(f"[WARNING] Save file {filename} does not exist.")
    return None, None, None, None
