import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from model import Building, Unit, Tile, Map



class AIStrategy:
    def execute(self, units, buildings, game_map, ai):
        """
        Exécute la stratégie pour une mise à jour du jeu.

        Args:
            units (list): Liste des unités du jeu.
            buildings (list): Liste des bâtiments du jeu.
            game_map (Map): Carte du jeu.
            ai (AI): L'objet représentant l'IA du joueur.
        """
        raise NotImplementedError("Cette méthode doit être implémentée par chaque stratégie.")


#-------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------
#---------Classe pour les comportements communs à chaque stratégie IA
#-------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------
class AI:
    def __init__(self, buildings, units):
        self.resources = {
            'Wood': 1000,
            'Gold': 1000,
            'Food': 500
        }#Ressource du début,  multiples choix dans le menu
        self.victoire = False
        self.buildings = buildings
        self.units = units
        self.town_center = None
        self.enemies = []  # Liste des IA ennemies
        #--
        self.population = len(units)
        self.population_max = sum(b.population_capacity for b in buildings if b.building_type == 'House') + 5  #MAX = 200

#----------------------
#Logique de l'IA : construct, recrute..
    def build(self, game_map, buildings):
        """Méthode pour construire un bâtiment si les ressources sont disponibles."""
        cost = {'Wood': 50, 'Gold': 30}
        if self.can_afford(cost):
            x, y = self.find_valid_build_location(game_map)
            if x is not None and y is not None:
                new_building = Building('Farm', x, y, owner=self)  # Associe le bâtiment à l'IA
                game_map.place_building(new_building, x, y, buildings)
                self.buildings.append(new_building)
                buildings.append(new_building)
                self.pay_resources(cost)
                print(f"Bâtiment {new_building.building_type} construit à ({x}, {y}) par {self}.")

        else:
            print("Pas assez de ressources pour construire.")

    def find_valid_build_location(self, game_map):
        """Trouver une position libre à proximité immédiate du Town Center pour construire une ferme."""
        # Centre du Town Center
        center_x, center_y = self.town_center.x, self.town_center.y

        # Rayon maximum de recherche
        max_radius = 10  # Ajustez ce rayon selon vos besoins

        for radius in range(2, max_radius + 1):  # Volontairement eloigné pour pouvoir observer les deplacements
            for dx in range(-radius, radius + 1):
                for dy in range(-radius, radius + 1):
                    # Ne considère que les cases à exactement `radius` de distance
                    if abs(dx) + abs(dy) == radius:
                        x, y = center_x + dx, center_y + dy

                        # Vérifie que la case est dans les limites de la carte et est vide
                        if 0 <= x < game_map.width and 0 <= y < game_map.height and game_map.is_empty(x, y):
                            # Vérifie que la case respecte l'espace d'un cube autour du Town Center
                            if abs(dx) > 1 and abs(dy) > 1:
                                return x, y

        # Aucun emplacement disponible trouvé
        print(f"Aucun emplacement libre trouvé autour du Town Center dans un rayon de {max_radius} cases.")
        return None, None

    def generate_villager(self, game_map, units):
        """Générer un villageois si les ressources et la population maximale le permettent."""
        cost = {'Food': 50}
        if self.can_afford(cost) and self.population < self.population_max:
            x, y = self.find_valid_build_location(game_map)
            if x is None or y is None:
                print("Erreur : Aucun emplacement valide trouvé pour générer un villageois.")

            if x is not None and y is not None:
                new_villager = Unit('Villager', x, y, self)
                self.units.append(new_villager)  # Ajout à la liste locale
                units.append(new_villager)      # Ajout à la liste globale
                game_map.grid[y][x].unit = new_villager  # Mettre à jour la carte
                print(f"Unité ajoutée sur la carte à ({x}, {y}) : {game_map.grid[y][x].unit.unit_type}")
                self.pay_resources(cost)
                self.update_population(1)
                print(f"Villageois généré à ({x}, {y}). Population actuelle : {self.population}/{self.population_max}")
            else:
                print("Aucun emplacement disponible pour générer un villageois.")
        else:
            print("Pas assez de ressources ou population maximale atteinte pour générer un villageois.")


#----------------------
# economie
    
    def can_afford(self, cost):
        """Vérifie si l'IA peut se permettre de payer un coût spécifique."""
        return all(self.resources[res] >= cost.get(res, 0) for res in cost)

    def pay_resources(self, cost):
        """Déduit les ressources après un achat."""
        if self.can_afford(cost):
            for res in cost:
                self.resources[res] -= cost[res]
                print(f"Paiement de {cost[res]} unités de {res}. Restant : {self.resources[res]}")




#----------------------
#guerre/bataille


    def set_enemies(self, all_ais):
        """Définit les IA ennemies en excluant la propre IA."""
        self.enemies = [ai for ai in all_ais if ai != self]

    @property
    def enemy_units(self):
        """Retourne toutes les unités des IA ennemies."""
        return [unit for enemy in self.enemies for unit in enemy.units]

    
    def unit_attack(self, attacker, target):
        """Permet à une unité d'attaquer une unité adverse."""
        if attacker.can_attack(target): #fonction dans le model (classe Unit)
            damage = attacker.attack_power
            target.take_damage(damage)
            print(f"{attacker.unit_type} attaque {target.unit_type} pour {damage} dégâts.")
            if target.health <= 0:
                print(f"{target.unit_type} a été détruit.")
                if target in target.ai.units:
                    target.ai.units.remove(target)  # Supprime l'unité de la liste des unités ennemies
                    print(f"{target.unit_type} retiré des unités de {target.ai}.")
                else:
                    print(f"[DEBUG] Erreur : {target.unit_type} non trouvé dans les unités de {target.ai}.")
        else:
            print(f"{attacker.unit_type} ne peut pas attaquer {target.unit_type}.")


    def find_target(self, unit, game_map, ai):
        """Trouve une cible prioritaire pour une unité."""
        if not ai.enemy_units:
            print(f"Aucune unité ennemie pour {unit.unit_type} à ({unit.x}, {unit.y}).")
            return None

        # Recherche de la cible la plus proche, même hors de portée
        closest_enemy = min(
            ai.enemy_units,
            key=lambda e: abs(unit.x - e.x) + abs(unit.y - e.y),
            default=None
        )
        if closest_enemy:
            distance = abs(unit.x - closest_enemy.x) + abs(unit.y - closest_enemy.y)
            if distance <= unit.attack_range:
                print(f"{unit.unit_type} trouve une cible à portée : {closest_enemy.unit_type}.")
                return closest_enemy
            else:
                # Déplace l'unité vers l'ennemi le plus proche
                unit.move_to(closest_enemy.x, closest_enemy.y)
                print(f"{unit.unit_type} se déplace vers {closest_enemy.unit_type} à ({closest_enemy.x}, {closest_enemy.y}).")
                return None

        print(f"Aucune cible trouvée pour {unit.unit_type}.")
        return None




#----------------------
#logique de jeu
    def update_resources(self, resource_type, amount):
        if resource_type in self.resources:
            self.resources[resource_type] += amount
            print(f"[AI] Ressources {resource_type} mises à jour : {self.resources[resource_type]} unités.")



    def update_population(self, change):
        """Met à jour la population actuelle."""
        self.population += change
        if self.population < 0:
            self.population = 0  # Empêche une population négative
        print(f"Population mise à jour : {self.population}/{self.population_max}")

    def recalculate_population_max(self):
        self.population_max = sum(b.population_capacity for b in self.buildings)
        print(f"Population maximale recalculée : {self.population_max}")


    def set_victoire(self, status):
        self.victoire = status
        print(f"Victoire: {'Oui' if self.victoire else 'Non'}")
