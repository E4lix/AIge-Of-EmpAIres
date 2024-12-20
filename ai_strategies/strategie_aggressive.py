from ai_strategies.base_strategies import AIStrategy

class StrategieAggressive(AIStrategy):
    def execute(self, units, buildings, game_map, ai):

        for unit in ai.units:
            if unit.unit_type in ['Soldier', 'Archer', 'Cavalier', 'Villager']:
                target = ai.find_target(unit, game_map, ai)
                if target:
                    print(f"{unit.unit_type} à ({unit.x}, {unit.y}) attaque {target.unit_type} à ({target.x}, {target.y}).")
                    ai.unit_attack(unit, target)
                else:
                    print(f"{unit.unit_type} à ({unit.x}, {unit.y}) n'a pas de cible.")
        

#        
        if not ai.enemy_units:
            print(f"{ai} a terassé tous ses ennemies")
            ai.generate_villager(game_map, units)
            ai.generate_villager(game_map, units)


        ai.population = len(ai.units)
 





