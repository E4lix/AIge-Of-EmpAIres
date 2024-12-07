import curses

def init_colors():
    """Initialise les couleurs pour l'affichage."""
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Vert pour le bois
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Jaune pour l'or
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Blanc pour les tuiles vides
    curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)  # Cyan pour les villageois par défaut
    curses.init_pair(5, curses.COLOR_RED, curses.COLOR_BLACK)  # Rouge pour le Town Center
    curses.init_pair(6, curses.COLOR_MAGENTA, curses.COLOR_BLACK)  # Magenta pour les fermes
    curses.init_pair(7, curses.COLOR_BLUE, curses.COLOR_BLACK)  # Bleu pour les casernes
    # Couleurs spécifiques pour chaque joueur
    curses.init_pair(8, curses.COLOR_BLUE, curses.COLOR_BLACK)   # Joueur 1
    curses.init_pair(9, curses.COLOR_RED, curses.COLOR_BLACK)    # Joueur 2
    curses.init_pair(10, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Joueur 3
    curses.init_pair(11, curses.COLOR_MAGENTA, curses.COLOR_BLACK)  # Joueur 4



def display_with_curses(stdscr, game_map, units, buildings, ais, view_x, view_y, max_height, max_width):
    stdscr.clear()  # Efface l'écran pour éviter les résidus
    unit_positions = {(unit.x, unit.y): unit for unit in units}  # Associe les unités à leurs positions

    # Affiche la portion visible de la carte en fonction de view_x et view_y
    for y in range(view_y, min(view_y + max_height, game_map.height)):
        for x in range(view_x, min(view_x + max_width, game_map.width)):
            tile = game_map.grid[y][x]
            if (x, y) in unit_positions:
                unit = unit_positions[(x, y)]
                player_idx = ais.index(unit.ai)  # Trouve l'indice du joueur
                color_pair = 8 + player_idx  # Associe la couleur en fonction du joueur

                # Associe une lettre à chaque type d'unité
                unit_display_map = {
                    'Villager': 'V',
                    'Soldier': 'S',
                    'Archer': 'A',
                    'Cavalier': 'C'
                }
                unit_char = unit_display_map.get(unit.unit_type, '?')  # Par défaut, '?' pour les types inconnus
                stdscr.addch(y - view_y, x - view_x, unit_char, curses.color_pair(color_pair))

            elif tile.building:
                owner_ai = next((ai for ai in ais if tile.building in ai.buildings), None)
                if owner_ai:
                    player_idx = ais.index(owner_ai)
                    color_pair = 8 + player_idx  # Couleur du joueur propriétaire
                else:
                    color_pair = 5  # Rouge par défaut pour les bâtiments sans propriétaire
                if tile.building.building_type == 'Town Center':
                    stdscr.addch(y - view_y, x - view_x, 'T', curses.color_pair(color_pair))
                elif tile.building.building_type == 'Farm':
                    stdscr.addch(y - view_y, x - view_x, 'F', curses.color_pair(color_pair))
                elif tile.building.building_type == 'Barracks':
                    stdscr.addch(y - view_y, x - view_x, 'B', curses.color_pair(color_pair))
            elif tile.resource == 'Wood':
                stdscr.addch(y - view_y, x - view_x, 'W', curses.color_pair(1))  # Bois en vert
            elif tile.resource == 'Gold':
                stdscr.addch(y - view_y, x - view_x, 'G', curses.color_pair(2))  # Or en jaune
            else:
                stdscr.addch(y - view_y, x - view_x, '.', curses.color_pair(3))  # Tuile vide

    # Afficher les ressources et informations de chaque joueur
    info_y = 0  # Position Y pour les informations
    for idx, ai in enumerate(ais):
        resources_info = (f"Joueur {idx + 1} - Bois: {ai.resources['Wood']} Or: {ai.resources['Gold']} "
                          f"Nourriture: {ai.resources['Food']} "
                          f"Population: {ai.population}/{ai.population_max}")
        stdscr.addstr(info_y, 0, resources_info[:max_width], curses.color_pair(8 + idx))
        info_y += 1

    stdscr.refresh()





def handle_input(stdscr, view_x, view_y, max_height, max_width, game_map):
    """Gère les touches pour le scrolling ZQSD et les touches fléchées."""
    key = stdscr.getch()

    if key == ord('z') or key == curses.KEY_UP:  # Touche Z ou flèche haut pour monter
        view_y = max(0, view_y - 1)  # Limite supérieure
    elif key == ord('s') or key == curses.KEY_DOWN:  # Touche S ou flèche bas pour descendre
        view_y = min(game_map.height - max_height, view_y + 1)  # Limite inférieure
    elif key == ord('q') or key == curses.KEY_LEFT:  # Touche Q ou flèche gauche pour aller à gauche
        view_x = max(0, view_x - 1)  # Limite gauche
    elif key == ord('d') or key == curses.KEY_RIGHT:  # Touche D ou flèche droite pour aller à droite
        view_x = min(game_map.width - max_width, view_x + 1)  # Limite droite

    return view_x, view_y
