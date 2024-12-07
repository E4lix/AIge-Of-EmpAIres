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
        

#        # Étape 3 : Si tous les ennemis sont morts, récolte du bois
        if not ai.enemy_units:
            print("ils sont tous raides")
            ai.generate_villager(game_map, units)
            ai.generate_villager(game_map, units)

 #           print("Tous les ennemis sont éliminés. Les villageois commencent à récolter du bois.")
  #          for unit in ai.units:
   #             if unit.unit_type == 'Villager':
     #               wood_path = unit.find_nearest_wood(game_map)
           #         if wood_path:
       #                 next_step = wood_path.pop(0)
             #           unit.move(*next_step)
              #          unit.gather_resource(game_map)

        ai.population = len(ai.units)
 





