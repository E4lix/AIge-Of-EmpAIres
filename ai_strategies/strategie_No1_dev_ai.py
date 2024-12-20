import time
from ai_strategies.base_strategies import AIStrategy

class StrategieNo1(AIStrategy):
    def execute(self, units, buildings, game_map, ai):
        for unit in ai.units:  # Limiter aux unités de cette IA
            # Gestion du dépôt des ressources
            if unit.returning_to_town_center:
                path = unit.find_nearest_town_center(game_map,ai)  # Appel avec le bon nombre d'arguments
                if path:
                    next_step = path.pop(0)
                    unit.move(*next_step)
                    if (unit.x, unit.y) == (ai.town_center.x, ai.town_center.y):
                        unit.deposit_resource()
                        unit.returning_to_town_center = False  # Réinitialisation
                        print(f"{unit.unit_type} retourne à la sélection de ressources après dépôt.")

            else:
                # Recherche et choix de la ressource la plus proche disponible
                food_path = unit.find_nearest_farm(game_map,ai)
                wood_path = unit.find_nearest_wood(game_map)
                gold_path = unit.find_nearest_gold(game_map)

                paths = {
                    'Food': (food_path, len(food_path) if food_path else float('inf')),
                    'Wood': (wood_path, len(wood_path) if wood_path else float('inf')),
                    'Gold': (gold_path, len(gold_path) if gold_path else float('inf'))
                }

                # Sélection de la ressource la plus proche
                nearest_resource = min(paths.items(), key=lambda x: x[1][1])
                print(f"{unit.unit_type} sélectionne la ressource la plus proche : {nearest_resource[0]}")


                if nearest_resource[1][0]:  # Si un chemin est trouvé
                    path = nearest_resource[1][0]  # Récupère le chemin complet
                    next_step = path.pop(0)  # Avance d'une étape
                    unit.move_to(*next_step)  # Déplacement case par case

                    # Vérifiez si l'unité est arrivée à destination
                    if not path:  # Si le chemin est vide
                        print(f"{unit.unit_type} est arrivé à destination.")
                        if nearest_resource[0] == 'Food':
                            farm_tile = game_map.grid[unit.y][unit.x]
                            if farm_tile.building and farm_tile.building.building_type == 'Farm' and not farm_tile.building.is_empty():
                                unit.working_farm = farm_tile.building
                                unit.gather_food_from_farm()
                            else:
                                print(f"Aucune ferme valide trouvée à ({unit.x}, {unit.y}) pour {unit.unit_type}.")
                        elif nearest_resource[0] in ['Wood', 'Gold']:
                            unit.gather_resource(game_map)
                    else:
                        print(f"{unit.unit_type} continue à se déplacer. Prochaine étape : {path[0]}")



        # Mise à jour pour l'IA
        ai.population = len(ai.units)
        if ai.can_afford({"Wood": 350}):
            ai.build(game_map, buildings)



