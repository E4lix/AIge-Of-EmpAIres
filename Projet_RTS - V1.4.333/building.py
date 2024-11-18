import random
import heapq  # Pour la recherche de chemin

class Building:
    def __init__(self, building_type, x, y):
        self.building_type = building_type  # Par exemple, 'Town Center'
        self.x = x
        self.y = y
        self.resources = {
            'Wood': 0,
            'Gold': 0,
            'Food': 0
        }
        self.costs = {
            'Town Center': {'Wood': 200, 'Gold': 50},
            'House': {'Wood': 50, 'Gold': 0},
            'Barracks': {'Wood': 150, 'Gold': 50},
            'Farm': {'Wood': 60, 'Gold': 0}  # Coût de la ferme
        }
        self.population_capacity = 0  # Capacité maximale de population pour certains bâtiments
        self.occupied = False  # Assurez-vous que cet attribut est bien initialisé

        # Ajuster la capacité selon le type de bâtiment
        if self.building_type == 'House':
            self.population_capacity = 5  # Chaque maison ajoute de la population
        if self.building_type == 'Farm':
            self.food_capacity = 300  # Chaque ferme contient 300 unités de nourriture

    def get_construction_cost(self):
        """Renvoie le coût de construction pour ce type de bâtiment."""
        return self.costs.get(self.building_type, {'Wood': 0, 'Gold': 0})

    def deposit_resource(self, resource_type, amount):
        """Le villageois dépose des ressources dans le bâtiment (par exemple, un Town Center)."""
        if resource_type in self.resources:
            self.resources[resource_type] += amount

    def gather_food(self, amount):
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
        self.occupied = True

    def free(self):
        """Libère la ferme pour qu'un autre villageois puisse l'utiliser."""
        self.occupied = False

    def __repr__(self):
        return f"<{self.building_type} at ({self.x}, {self.y})>"