import random
import heapq  # Pour la recherche de chemin


from building import Building
from map import Tile, Map
from ia import AI

class Unit:
    def __init__(self, unit_type, x, y):
        self.unit_type = unit_type  # Par exemple : 'Villager'
        self.x = x  # Position x sur la carte
        self.y = y  # Position y sur la carte
        self.resource_collected = 0  # Quantité de ressources que l'unité a collectée
        self.max_capacity = 50  # Quantité maximale que le villageois peut porter
        self.returning_to_town_center = False  # Si le villageois retourne au Town Center pour déposer les ressources
        self.current_resource = None  # Type de ressource en train d'être collectée
        self.working_farm = None  # Référence à la ferme sur laquelle le villageois travaille

    def move(self, new_x, new_y):
        self.x = new_x
        self.y = new_y

    def gather_resource(self, game_map):
        """ Récolte une ressource si le villageois est sur une case contenant une ressource """
        tile = game_map.grid[self.y][self.x]
        if tile.resource:
            resource_type = tile.resource
            amount = min(20, self.max_capacity - self.resource_collected)
            self.resource_collected += amount  # Récolte 20 unités de ressource (ou moins si la capacité max est atteinte)
            self.current_resource = resource_type  # Stocke le type de ressource
            if self.resource_collected >= self.max_capacity:
                self.returning_to_town_center = True  # Le villageois retourne au Town Center
            tile.resource = None  # La ressource est épuisée sur cette case

    def gather_food_from_farm(self):
        """Récolte de la nourriture dans une ferme."""
        if self.working_farm:
            if self.working_farm.is_empty():
                self.working_farm.free()  # Libérer la ferme lorsqu'elle est épuisée
                self.working_farm = None  # Ne plus travailler dans cette ferme
                return  # Arrêter immédiatement la récolte

            # Si la ferme n'est pas occupée, le villageois commence à travailler
            if not self.working_farm.is_occupied():
                self.working_farm.occupy()  # Marquer la ferme comme occupée
                amount = min(20, self.max_capacity - self.resource_collected)
                food_gathered = self.working_farm.gather_food(amount)
                self.resource_collected += food_gathered
                self.current_resource = 'Food'

                if self.resource_collected >= self.max_capacity:
                    self.returning_to_town_center = True
                    self.working_farm.free()  # Libérer la ferme après avoir atteint la capacité maximale
                    self.working_farm = None  # Ne plus travailler dans cette ferme

    def deposit_resource(self, building):
        """Le villageois dépose les ressources au Town Center."""
        if building and building.building_type == 'Town Center' and self.current_resource:
            building.deposit_resource(self.current_resource, self.resource_collected)
            self.resource_collected = 0  # Le villageois a déposé toutes les ressources
            self.returning_to_town_center = False  # Le villageois reprend la collecte
            self.current_resource = None  # Réinitialiser la ressource collectée

    def find_nearest_farm(self, game_map):
        """Recherche la ferme la plus proche qui contient de la nourriture et qui n'est pas occupée."""
        path = self.find_path(game_map, (self.x, self.y), 'Farm')
        if path:
            # Récupération de la tuile et du bâtiment sur cette tuile
            farm_tile = game_map.grid[path[-1][1]][path[-1][0]]
            if farm_tile.building and not farm_tile.building.is_occupied() and not farm_tile.building.is_empty():
                return path
            else:
                return None
        else:
            return None


    def find_nearest_gold(self, game_map):
        """ Utilise une recherche de chemin pour trouver l'or le plus proche """
        path = self.find_path(game_map, (self.x, self.y), 'Gold')
        return path

    def find_nearest_wood(self, game_map):
        """ Utilise une recherche de chemin pour trouver le bois le plus proche """
        path = self.find_path(game_map, (self.x, self.y), 'Wood')
        return path

    def find_nearest_food(self, game_map):
        """ Utilise une recherche de chemin pour trouver la nourriture la plus proche """
        path = self.find_path(game_map, (self.x, self.y), 'Food')
        return path

    def find_nearest_town_center(self, game_map, buildings):
        """ Recherche du chemin vers le Town Center le plus proche """
        town_center = buildings[0]
        # Si le villageois est déjà sur la même tuile que le Town Center
        if (self.x, self.y) == (town_center.x, town_center.y):
            return None  # Pas besoin de trouver un chemin

        path = self.find_path(game_map, (self.x, self.y), 'Town Center', town_center)
        return path

    def find_path(self, game_map, start, target_type, target_building=None):
        """ Recherche un chemin vers une destination donnée (bois, or, ou bâtiment spécifique) """
        def heuristic(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])  # Distance Manhattan

        open_list = []
        heapq.heappush(open_list, (0, start))  # Ajouter la position initiale
        came_from = {}
        cost_so_far = {start: 0}

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Gauche, Droite, Haut, Bas

        while open_list:
            _, current = heapq.heappop(open_list)

            # Vérification pour le bois
            if target_type == 'Wood' and game_map.grid[current[1]][current[0]].resource == 'Wood':              
                return self.reconstruct_path(came_from, current)  # Retourner le chemin trouvé

            # Vérification pour l'or
            if target_type == 'Gold' and game_map.grid[current[1]][current[0]].resource == 'Gold':
                
                return self.reconstruct_path(came_from, current)  # Retourner le chemin trouvé

            # Vérification pour le Town Center
            if target_type == 'Town Center' and target_building and (current[0], current[1]) == (target_building.x, target_building.y):
                return self.reconstruct_path(came_from, current)

            # Vérification pour une ferme
            if target_type == 'Farm' and isinstance(game_map.grid[current[1]][current[0]].building, Building) and game_map.grid[current[1]][current[0]].building.building_type == 'Farm':
                return self.reconstruct_path(came_from, current)

            # Exploration des voisins
            for dx, dy in directions:
                next_node = (current[0] + dx, current[1] + dy)
                if 0 <= next_node[0] < game_map.width and 0 <= next_node[1] < game_map.height:
                    new_cost = cost_so_far[current] + 1
                    if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                        cost_so_far[next_node] = new_cost
                        priority = new_cost + heuristic(next_node, (self.x, self.y))
                        heapq.heappush(open_list, (priority, next_node))
                        came_from[next_node] = current

        return None

    def reconstruct_path(self, came_from, current):
        """ Recrée le chemin à partir de la position courante """
        path = []
        while current in came_from:
            path.append(current)
            current = came_from[current]
        path.reverse()  # On inverse le chemin pour partir de la position de départ
        return path

