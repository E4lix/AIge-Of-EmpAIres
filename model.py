import random
import heapq  # Pour la recherche de chemin
import time



class Tile:
    def __init__(self):
        self.resource = None  # Peut être une ressource comme 'Wood', 'Gold', etc.
        self.building = None  # Référence à un objet Building s'il y en a un
        self.unit = None      # Référence à un objet Unit s'il y en a une


class Map:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[Tile() for _ in range(width)] for _ in range(height)]  
        self.tile_dict_resources = {}  # Indexation des tuiles avec ressources
        self.tile_dict_buildings = {}  # Indexation des tuiles avec bâtiments




    def debug_tile_dict(self):
        """Affiche toutes les tuiles enregistrées dans les dictionnaires de ressources et de bâtiments."""
        print("Tuiles contenant des ressources :")
        for key, tile in self.tile_dict_resources.items():
            print(f"Coordonnée : {key}, Ressource : {tile.resource}")

        print("\nTuiles contenant des bâtiments :")
        for key, tile in self.tile_dict_buildings.items():
            building = tile.building.building_type if tile.building else None
            print(f"Coordonnée : {key}, Bâtiment : {building}")



    def is_empty(self, x, y):
        """Vérifie si une position est vide."""
        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            return False
        tile = self.grid[y][x]
        return not (tile.resource or tile.building or tile.unit)


    def update_tile_index(self, x, y):
        """Mise à jour des index pour les tuiles contenant des ressources ou des bâtiments."""
        key = f"{x},{y}"
        tile = self.grid[y][x]

        # Mise à jour des ressources
        if tile.resource:
            self.tile_dict_resources[key] = tile
        elif key in self.tile_dict_resources:
            del self.tile_dict_resources[key]

        # Mise à jour des bâtiments
        if tile.building:
            self.tile_dict_buildings[key] = tile
        elif key in self.tile_dict_buildings:
            del self.tile_dict_buildings[key]




    def get_tiles_with_resource(self, resource_type):
        """Récupère les coordonnées des tuiles contenant une ressource spécifique."""
        return [
            (int(key.split(',')[0]), int(key.split(',')[1]))
            for key, tile in self.tile_dict_resources.items()
            if tile.resource == resource_type
        ]


    def get_tiles_with_building(self, building_type):
        """Renvoie les coordonnées des tuiles contenant un type spécifique de bâtiment."""
        return [
            (int(key.split(',')[0]), int(key.split(',')[1]))
            for key, tile in self.tile_dict_buildings.items()
            if tile.building and tile.building.building_type == building_type
        ]




    def generate_forest_clusters(self, num_clusters, cluster_size):
        for _ in range(num_clusters):
            start_x = random.randint(0, self.width - 1)
            start_y = random.randint(0, self.height - 1)
            self._create_cluster(start_x, start_y, cluster_size, 'Wood')

    def generate_gold_clusters(self, num_clusters):
        for _ in range(num_clusters):
            start_x = random.randint(0, self.width - 1)
            start_y = random.randint(0, self.height - 1)
            cluster_size = random.randint(3, 10)
            self._create_cluster(start_x, start_y, cluster_size, 'Gold')

    def _create_cluster(self, x, y, size, resource_type):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (-1, 1), (1, -1)]
        tiles_to_fill = set([(x, y)])  # Utiliser un ensemble pour éviter les doublons

        while tiles_to_fill and size > 0:
            current_x, current_y = tiles_to_fill.pop()
            if 0 <= current_x < self.width and 0 <= current_y < self.height:
                tile = self.grid[current_y][current_x]
                if tile.resource is None and tile.building is None:
                    tile.resource = resource_type
                    self.update_tile_index(current_x, current_y)  # Mise à jour de tile_dict
                    size -= 1

                    random.shuffle(directions)
                    for dx, dy in directions:
                        new_x, new_y = current_x + dx, current_y + dy
                        if (new_x, new_y) not in tiles_to_fill and 0 <= new_x < self.width and 0 <= new_y < self.height:
                            tiles_to_fill.add((new_x, new_y))


    def place_building(self, building, x, y, buildings_list=None):
        if 0 <= x < self.width and 0 <= y < self.height:
            tile = self.grid[y][x]
            tile.building = building
            self.update_tile_index(x, y)  # Assure que les indices sont mis à jour
            if building.building_type not in ['Wood', 'Gold']:  # Évite d'écraser les ressources
                self.tile_dict_buildings[f"{x},{y}"] = tile  # Ajout explicite
            if buildings_list is not None:
                buildings_list.append(building)
            print(f"Bâtiment {building.building_type} placé à ({x}, {y})")









class Building:
    def __init__(self, building_type, x, y, owner=None):
        self.building_type = building_type  # Par exemple, 'Town Center'
        self.x = x
        self.y = y
        self.costs = {
            'Town Center': {'Wood': 200, 'Gold': 50},
            'House': {'Wood': 50, 'Gold': 0},
            'Barracks': {'Wood': 150, 'Gold': 50},
            'Farm': {'Wood': 60, 'Gold': 0}  # Coût de la ferme
        }
        self.owner = owner  
        self.population_capacity = 0  # Capacité maximale de population pour certains bâtiments
        self.occupied = False  

        if self.building_type == 'House': # Pas encore implémenté
            self.population_capacity = 5  # Chaque maison ajoute de la population
        if self.building_type == 'Farm':
            self.food_capacity = 300 

    def get_construction_cost(self):
        """Renvoie le coût de construction pour ce type de bâtiment."""
        return self.costs.get(self.building_type, {'Wood': 0, 'Gold': 0})

    
    def gather_food(self, amount):
        """Récolte la nourriture de la ferme jusqu'à épuisement."""
        if self.food_capacity > 0:
            gathered = min(amount, self.food_capacity)
            self.food_capacity -= gathered
            return gathered
        return 0

    def is_empty(self):
        return self.food_capacity <= 0

    def is_occupied(self):
        """Vérifie si la ferme est occupée par un villageois."""
        return self.occupied

    def occupy(self):
        """Marque la ferme comme étant occupée."""
        self.occupied = False

    def free(self):
        """Libère la ferme pour qu'un autre villageois puisse l'utiliser."""
        self.occupied = False

    def __repr__(self):
        return f"<{self.building_type} at ({self.x}, {self.y})>"


UNIT_STATS = {
    'Villager': {'health': 100, 'attack_power': 10, 'attack_range': 1},
    'Soldier': {'health': 150, 'attack_power': 20, 'attack_range': 1},
    'Archer': {'health': 80, 'attack_power': 15, 'attack_range': 3},
    'Cavalier': {'health': 200, 'attack_power': 25, 'attack_range': 1}
}


class Unit:
    def __init__(self, unit_type, x, y, ai):
        self.unit_type = unit_type  # Par exemple : 'Villager'
        self.x = x  # Position x sur la carte
        self.y = y  # Position y sur la carte
        self.ai = ai
        self.resource_collected = 0  # Quantité de ressources que l'unité a collectée
        self.max_capacity = 20  # Quantité maximale que le villageois peut porter
        self.returning_to_town_center = False  # Si le villageois retourne au Town Center pour déposer les ressources
        self.current_resource = None  # Type de ressource en train d'être collectée
        self.working_farm = None  # Référence à la ferme sur laquelle le villageois travaille
        stats = UNIT_STATS.get(unit_type) #, {'health': 100, 'attack_power': 10, 'attack_range': 1})
        self.health = stats['health']
        self.attack_power = stats['attack_power']
        self.attack_range = stats['attack_range']
        self.target = None  # Cible actuelle

    def move(self, new_x, new_y):
        self.x = new_x
        self.y = new_y
    
    #LOGIQUE COMBAT
    def move_to(self, target_x, target_y):
        """Déplace l'unité d'une case vers la direction de la cible."""
        if self.x < target_x:
            self.x += 1
        elif self.x > target_x:
            self.x -= 1

        if self.y < target_y:
            self.y += 1
        elif self.y > target_y:
            self.y -= 1

        print(f"{self.unit_type} se déplace vers ({target_x}, {target_y}). Nouvelle position : ({self.x}, {self.y}).")

    def can_attack(self, target):
        """Vérifie si cette unité peut attaquer une cible."""
        if self.ai == target.ai:
            return False  # Ne peut pas attaquer ses propres unités
        distance = abs(self.x - target.x) + abs(self.y - target.y)
        return distance <= self.attack_range

    def attack(self, target):
        """Inflige des dégâts à une unité cible."""
        if self.can_attack(target):
            target.take_damage(self.attack_power)
            print(f"{self.unit_type} attaque {target.unit_type} pour {self.attack_power} dégâts.")
        else:
            print(f"{self.unit_type} est hors de portée pour attaquer {target.unit_type}.")

    def take_damage(self, damage):
        """Inflige des dégâts à l'unité."""
        self.health -= damage
        print(f"{self.unit_type} reçoit {damage} dégâts. Santé restante : {self.health}")
        if self.health <= 0:
            self.health = 0
            print(f"{self.unit_type} est détruit.")
            if self in self.ai.units:
                self.ai.units.remove(self)  # Supprime l'unité de la liste des unités
                print(f"{self.unit_type} retiré des unités de {self.ai}.")
            else:
                print(f"[DEBUG] {self.unit_type} déjà supprimé des unités de {self.ai}.")

    
    def launch_attack(self, ai):#inutilisé 
        """Envoyer toutes les unités militaires attaquer la base ennemie."""
        for unit in ai.units:
            if unit.unit_type in ['Soldier', 'Archer', 'Cavalier']:
                enemy_base = ai.enemy_base
                unit.move_to(enemy_base.x, enemy_base.y)
                print(f"{unit.unit_type} se dirige vers la base ennemie.")

    

    
    #LOGIQUE RESSOURCES

    def gather_resource(self, game_map):
        """ Récolte une ressource si le villageois est sur une case contenant une ressource """
        tile = game_map.grid[self.y][self.x]
        if tile.resource:
            resource_type = tile.resource
            amount = min(20, self.max_capacity - self.resource_collected)
            self.resource_collected += amount  # Récolte 20 unités de ressource (ou moins si la capacité max est atteinte)
            print(f"{self.unit_type} récolte {amount} unités de {resource_type} à ({self.x}, {self.y}).")
            self.current_resource = resource_type  # Stocke le type de ressource
            if self.resource_collected >= self.max_capacity:
                print(f"{self.unit_type} a atteint sa capacité maximale en {resource_type}.")
                self.returning_to_town_center = True  # Le villageois retourne au Town Center
            tile.resource = None  # La ressource est épuisée sur cette case

    def gather_food_from_farm(self):
        """Récolte la nourriture de la ferme en continu jusqu'à épuisement."""
        if not self.working_farm:
            print(f"{self.unit_type} n'a pas de ferme assignée.")
            return

        if self.working_farm.is_empty():
            print(f"Ferme à ({self.working_farm.x}, {self.working_farm.y}) est épuisée.")
            self.working_farm.free()
            self.working_farm = None
            return

        if not self.working_farm.is_occupied():
            self.working_farm.occupy()
            print(f"{self.unit_type} commence à récolter dans la ferme à ({self.working_farm.x}, {self.working_farm.y}).")

        current_time = time.time()
        if not hasattr(self, 'action_end_time'):
            self.action_end_time = current_time + 2  # Test

        if current_time >= self.action_end_time:
            amount = min(20, self.max_capacity - self.resource_collected)
            food_gathered = self.working_farm.gather_food(amount)
            self.resource_collected += food_gathered
            self.current_resource = 'Food'
            print(f"{self.unit_type} récolte {food_gathered} unités de nourriture.")

            if self.resource_collected >= self.max_capacity:
                print(f"{self.unit_type} a atteint sa capacité maximale en nourriture.")
                self.returning_to_town_center = True
                self.working_farm.free()
                self.working_farm = None
            else:
                self.action_end_time = current_time + 5  # Prochaine récolte




    def deposit_resource(self):
        if self.current_resource:
            town_center = self.ai.town_center
            if (self.x, self.y) == (town_center.x, town_center.y):
                print(f"{self.unit_type} dépose {self.resource_collected} unités de {self.current_resource} au Town Center de l'IA.")
                self.ai.update_resources(self.current_resource, self.resource_collected)
                self.resource_collected = 0
                self.returning_to_town_center = False
                self.current_resource = None
            else:
                print(f"{self.unit_type} retourne au Town Center pour déposer les ressources.")
                path = self.find_nearest_town_center(self.ai.game_map, self.ai.buildings)
                if path:
                    next_step = path[0]
                    self.move(next_step[0], next_step[1])





    def find_nearest_farm(self, game_map, ai):
        farms = [
            building for building in ai.buildings
            if building.building_type == 'Farm' and not building.is_empty() and not building.is_occupied()
        ]
        if not farms:
            print(f"Aucune ferme disponible pour {self.unit_type} à ({self.x}, {self.y}).")
            return None

        closest_farm = min(
            farms,
            key=lambda farm: abs(farm.x - self.x) + abs(farm.y - self.y),
            default=None
        )
        if closest_farm:
            return [(closest_farm.x, closest_farm.y)]
        return None







    def find_nearest_gold(self, game_map):
        """Trouve l'or le plus proche."""
        path = self.find_path(game_map, (self.x, self.y), 'Gold')
        if path:
            print(f"Chemin trouvé vers l'or : {path}")
            return path
        print(f"Aucun chemin vers l'or trouvé pour {self.unit_type} à ({self.x}, {self.y})")
        return None

    def find_nearest_wood(self, game_map):
        """Trouve le bois le plus proche."""
        path = self.find_path(game_map, (self.x, self.y), 'Wood')
        if path:
            print(f"Chemin trouvé vers le bois : {path}")
            return path
        print(f"Aucun chemin vers le bois trouvé pour {self.unit_type} à ({self.x}, {self.y})")
        return None


    def find_nearest_town_center(self, game_map, ai):
        town_centers = [
            (int(key.split(',')[0]), int(key.split(',')[1]))
            for key, tile in game_map.tile_dict_buildings.items()
            if tile.building and tile.building.building_type == 'Town Center' and tile.building.owner == ai
        ]
        if not town_centers:
            print(f"Aucun Town Center allié disponible pour {self.unit_type} à ({self.x}, {self.y}).")
            return None

        closest_town_center = min(town_centers, key=lambda tc: abs(tc[0] - self.x) + abs(tc[1] - self.y), default=None)
        if closest_town_center:
            return self.find_path(game_map, (self.x, self.y), 'Town Center', closest_town_center)
        return None













    def find_path(self, game_map, start, target_type, target_position=None, owner=None):
        def heuristic(a, b):
            # Calcul du coût heuristique (distance de Manhattan)
            return abs(a[0] - b[0]) + abs(a[1] - b[1])

        open_list = []
        heapq.heappush(open_list, (0, start))
        came_from = {}
        cost_so_far = {start: 0}

        # Déplacement orthogonal et diagonal
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

        # Déterminer la position cible si non spécifiée
        if not target_position:
            if target_type in ['Wood', 'Gold', 'Food']:
                target_tiles = game_map.get_tiles_with_resource(target_type)
            else:
                target_tiles = [
                    (int(key.split(',')[0]), int(key.split(',')[1]))
                    for key, tile in game_map.tile_dict_buildings.items()
                    if tile.building and tile.building.building_type == target_type and tile.building.owner == owner
                ]
            if not target_tiles:
                print(f"Aucune tuile contenant {target_type} n'a été trouvée.")
                return None
            target_position = min(target_tiles, key=lambda t: heuristic(start, t))

        # Boucle principale pour trouver le chemin
        while open_list:
            _, current = heapq.heappop(open_list)

            # Chemin trouvé
            if current == target_position:
                return self.reconstruct_path(came_from, current)

            # Exploration des voisins
            for dx, dy in directions:
                next_node = (current[0] + dx, current[1] + dy)

                # Vérifier que la position est valide sur la carte
                if 0 <= next_node[0] < game_map.width and 0 <= next_node[1] < game_map.height:
                    # Calcul du coût pour ce déplacement (diagonal = 1.4, orthogonal = 1)
                    move_cost = 1.4 if dx != 0 and dy != 0 else 1
                    new_cost = cost_so_far[current] + move_cost

                    # Mise à jour si un meilleur chemin est trouvé
                    if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                        cost_so_far[next_node] = new_cost
                        priority = new_cost + heuristic(next_node, target_position)
                        heapq.heappush(open_list, (priority, next_node))
                        came_from[next_node] = current

        # Si aucun chemin trouvé
        print(f"Aucun chemin trouvé vers {target_type}.")
        return None







    def reconstruct_path(self, came_from, current):
        """ Recrée le chemin à partir de la position courante """
        path = []
        while current in came_from:
            path.append(current)
            current = came_from[current]
        path.reverse()  # On inverse le chemin pour partir de la position de départ
        return path



# test opti 

    def get_tiles_with_resource(self, resource_type):
        """Renvoie toutes les tuiles contenant un type spécifique de ressource."""
        return [
            (x, y) for y, row in enumerate(self.grid) 
            for x, tile in enumerate(row) 
            if tile.resource == resource_type
        ]
