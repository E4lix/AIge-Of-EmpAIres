import curses
import time
import os
import pygame
import sys
import signal
from model import Map, Unit, Building
from view import display_with_curses, handle_input, init_colors
from view_graphics import handle_input_pygame, render_map, screen_width, screen_height, TILE_WIDTH, TILE_HEIGHT, initialize_graphics
from game_utils import save_game_state, load_game_state

from ai_strategies.base_strategies import AI

from ai_strategies.strategie_aggressive import StrategieAggressive
from ai_strategies.strategie_No1_dev_ai import StrategieNo1 

current_strategy = StrategieNo1()

last_update_time = 0  # Initialiser last_update_time avant la boucle principale du jeu

# Constants
SAVE_DIR = "saves"

# Global Variables
units, buildings, game_map, ai, ai = None, None, None, None, None
ais = []  # Liste contenant toutes les IA des joueurs
def initialize_strategies(ais):
    """Associe une stratégie différente à chaque IA."""
    from ai_strategies.strategie_No1_dev_ai import StrategieNo1
    from ai_strategies.strategie_aggressive import StrategieAggressive
    strategies = []
    for i, ai in enumerate(ais):
        if i % 2 == 0:
            strategies.append(StrategieNo1())
        else:
            strategies.append(StrategieAggressive())
    return strategies

def list_saves():
    saves = [f for f in os.listdir(SAVE_DIR) if f.endswith(".pkl")]
    return saves

def load_existing_game(filename):
    global units, buildings, game_map, ais
    loaded_units, loaded_buildings, loaded_map, loaded_ais = load_game_state(filename)
    if loaded_units and loaded_buildings and loaded_map and loaded_ais:
        units, buildings, game_map, ais = loaded_units, loaded_buildings, loaded_map, loaded_ais
    else:
        print("[ERROR] Chargement échoué. Le fichier est corrompu ou n'existe pas.")

def load_existing_game_curses(stdscr):
    saves = list_saves()
    if not saves:
        stdscr.addstr(5, 0, "[INFO] Aucune sauvegarde trouvée.")
        stdscr.refresh()
        time.sleep(2)
        return

    selected_option = 0
    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "Choisissez une sauvegarde à charger:")
        for i, save in enumerate(saves):
            if i == selected_option:
                stdscr.addstr(i + 1, 0, save, curses.A_REVERSE)
            else:
                stdscr.addstr(i + 1, 0, save)
        stdscr.refresh()

        key = stdscr.getch()
        if key == curses.KEY_DOWN:
            selected_option = (selected_option + 1) % len(saves)
        elif key == curses.KEY_UP:
            selected_option = (selected_option - 1) % len(saves)
        elif key == ord('\n'):  # Touche entrée
            # Charger la partie sélectionnée
            load_existing_game(os.path.join(SAVE_DIR, saves[selected_option]))

            # Réinitialiser les stratégies après le chargement
            strategies = initialize_strategies(ais)

            # Après chargement, lancez directement la partie avec curses
            curses.wrapper(game_loop_curses, strategies)
            return  # Quitte la fonction après avoir lancé la boucle de jeu

def load_existing_game_graphics(screen, font):
    saves = list_saves()
    if not saves:
        render_text(screen, font, "[INFO] Aucune sauvegarde trouvée.", (20, 50))
        pygame.display.flip()
        time.sleep(2)
        return

    selected_option = 0
    running = True
    while running:
        screen.fill((0, 0, 0))
        render_text(screen, font, "Choisissez une sauvegarde à charger:", (20, 20))
        for i, save in enumerate(saves):
            color = (255, 255, 255) if i == selected_option else (100, 100, 100)
            render_text(screen, font, save, (20, 60 + i * 40), color)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(saves)
                elif event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(saves)
                elif event.key == pygame.K_RETURN:
                    load_existing_game(os.path.join(SAVE_DIR, saves[selected_option]))
                    strategies = initialize_strategies(ais)

                    game_loop_graphics(screen, strategies)
                    return


def clear_input_buffer(stdscr):
    stdscr.nodelay(True)
    while True:
        key = stdscr.getch()
        if key == -1:
            break
    stdscr.nodelay(False)



def signal_handler(sig, frame):
    print("[INFO] Exiting due to CTRL+C")
    curses.endwin()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def reset_curses():
    curses.endwin()
    time.sleep(0.1)
    sys.stdout.flush()

def reset_graphics():
    try:
        import pygame
        pygame.quit()
    except ImportError:
        pass
    time.sleep(0.1)

def switch_mode(new_mode):
    save_game_state(units, buildings, game_map, ais)
    if new_mode == 'graphics':
        reset_curses()
        game_loop_graphics(screen, strategies)  
    elif new_mode == 'terminal':
        reset_graphics()
        curses.wrapper(game_loop_curses, strategies)
        pygame.quit()


def switch_strategy(ais, strategies, ai_to_switch, new_strategy):
    """
    Change dynamiquement la stratégie d'une IA.

    Args:
        ais (list): Liste des IA dans le jeu.
        strategies (list): Liste des stratégies associées aux IA.
        ai_to_switch (AI): L'IA dont la stratégie doit être changée.
        new_strategy (AIStrategy): La nouvelle stratégie à appliquer.
    """
    index = ais.index(ai_to_switch)  # Trouve l'index de l'IA
    strategies[index] = new_strategy  # Met à jour la stratégie de cette IA
    print(f"La stratégie de l'IA {index + 1} a été changée en {new_strategy.__class__.__name__}.")



#-------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------
#------Boucle de MAJ des events et des IA
#-------------------------------------------------------------------------------------
def update_game(units, buildings, game_map, ais, strategies, delay, last_update_time):
    """
    Met à jour le jeu en utilisant la stratégie spécifiée pour les actions IA.

    Args:
        units (list): Liste des unités du jeu.
        buildings (list): Liste des bâtiments du jeu.
        game_map (Map): Carte du jeu.
        ai (AI): L'objet représentant l'IA du ai.
        strategy (AIStrategy): Stratégie actuellement utilisée pour l'IA.
        delay (float): Délai minimum entre les mises à jour.
        last_update_time (float): Temps de la dernière mise à jour.
    
    Returns:
        float: Temps de la dernière mise à jour (actualisé si nécessaire).
    """
    current_time = time.time() #voir aussi time.perf_counter pour plus de precision au besoin
    if current_time - last_update_time > delay:
        for ai, strategy in zip(ais, strategies):
            # Exécute la stratégie actuelle
            strategy.execute(units, buildings, game_map, ai)

            # Vérifie si les ennemis sont absents et change de stratégie
            if not ai.enemy_units and isinstance(strategy, StrategieAggressive):
                print(f"[INFO] IA {ais.index(ai) + 1} n'a plus d'ennemis.")
                new_strategy = StrategieNo1()
                switch_strategy(ais, strategies, ai, new_strategy)

        return current_time
    return last_update_time

def escape_menu_curses(stdscr):
    options = ["1. Sauvegarder", "2. Charger", "3. Reprendre", "4. Retour au Menu Principal", "5. Quitter"]
    selected_option = 0

    while True:
        stdscr.clear()
        for i, option in enumerate(options):
            if i == selected_option:
                stdscr.addstr(i, 0, option, curses.A_REVERSE)  # Option surlignée
            else:
                stdscr.addstr(i, 0, option)
        stdscr.refresh()

        key = stdscr.getch()
        if key == curses.KEY_DOWN:
            selected_option = (selected_option + 1) % len(options)
        elif key == curses.KEY_UP:
            selected_option = (selected_option - 1) % len(options)
        elif key == ord('\n'):  # Touche entrée
            if selected_option == 0:  # Sauvegarder
                clear_input_buffer(stdscr)
                stdscr.addstr(5, 0, "Nom de la sauvegarde :")
                stdscr.refresh()

                save_name = ""
                while True:
                    key = stdscr.getch()
                    if key == ord('\n'):
                        if save_name.strip() == "":
                            stdscr.addstr(6, 0, "Erreur : le nom ne peut pas être vide.")
                            stdscr.refresh()
                            time.sleep(2)
                        else:
                            break
                    elif key in [curses.KEY_BACKSPACE, 127]:
                        save_name = save_name[:-1]
                        stdscr.addstr(6, 0, " " * 20)  # Efface la ligne précédente
                        stdscr.addstr(6, 0, save_name)
                        stdscr.refresh()
                    elif 32 <= key <= 126:  # Caractères imprimables uniquement
                        save_name += chr(key)
                        stdscr.addstr(6, 0, save_name)
                        stdscr.refresh()

                try:
                    save_game_state(units, buildings, game_map, ais, os.path.join(SAVE_DIR, f"{save_name}.pkl"))
                except Exception as e:
                    stdscr.addstr(7, 0, f"Erreur : {str(e)}")
                    stdscr.refresh()
                    time.sleep(2)

            elif selected_option == 1:  # Charger
                load_existing_game_curses(stdscr)
                return  # Après chargement, lancez la boucle de jeu

            elif selected_option == 2:  # Reprendre
                return  # Quitte le menu et reprend la partie

            elif selected_option == 3:  # Retour au Menu Principal
                curses.wrapper(main_menu_curses_internal)
                return

            elif selected_option == 4:  # Quitter
                sys.exit(0)

        elif key == 27:  # Touche Échap pour quitter le menu
            return  # Quitte le menu pour reprendre la partie



def input_text_pygame(screen, font, prompt):
    input_text = ""
    running = True

    while running:
        screen.fill((0, 0, 0))
        prompt_surface = font.render(prompt, True, (255, 255, 255))
        input_surface = font.render(input_text, True, (255, 255, 255))
        screen.blit(prompt_surface, (20, 50))
        screen.blit(input_surface, (20, 100))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if input_text.strip() != "":
                        return input_text
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.key in (pygame.K_ESCAPE, pygame.K_F12):  # Échappe ou F12 pour annuler
                    return None
                elif 32 <= event.key <= 126:  # Caractères imprimables uniquement
                    input_text += event.unicode


def escape_menu_graphics(screen):
    font = pygame.font.Font(None, 36)
    options = ["1. Sauvegarder", "2. Charger", "3. Reprendre", "4. Retour au Menu Principal", "5. Quitter"]
    selected_option = 0
    running = True

    while running:
        screen.fill((0, 0, 0))
        for i, option in enumerate(options):
            color = (255, 255, 255) if i == selected_option else (100, 100, 100)
            text = font.render(option, True, color)
            screen.blit(text, (20, 50 + i * 40))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(options)
                elif event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(options)
                elif event.key == pygame.K_ESCAPE:  # Touche Échap pour quitter le menu
                    running = False
                elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:  # Touche entrée
                    if selected_option == 0:  # Sauvegarder
                        save_name = input_text_pygame(screen, font, "Nom de la sauvegarde :")
                        if save_name:
                            save_game_state(units, buildings, game_map, ais, os.path.join(SAVE_DIR, f"{save_name}.pkl"))
                    elif selected_option == 1:  # Charger
                        load_existing_game_graphics(screen, font)
                        return  # Après chargement, lancez la boucle de jeu

                    elif selected_option == 2:  # Reprendre
                        running = False  # Quitte le menu et reprend la partie

                    elif selected_option == 3:  # Retour au Menu Principal
                        main_menu_graphics()
                        return

                    elif selected_option == 4:  # Quitter
                        sys.exit(0)


def game_loop_curses(stdscr, strategies):

    global units, buildings, game_map, ai

    max_height, max_width = stdscr.getmaxyx()
    max_height -= 1
    max_width -= 1
    view_x, view_y = 0, 0

    stdscr.nodelay(True)
    stdscr.timeout(100)

    last_update_time = time.time()

    init_colors()

    while True:
        current_time = time.time()

        # Gère les entrées utilisateur et affiche la carte en curses
        view_x, view_y = handle_input(stdscr, view_x, view_y, max_height, max_width, game_map)
        display_with_curses(stdscr, game_map, units, buildings, ais, view_x, view_y, max_height, max_width)
        last_update_time = update_game(units, buildings, game_map, ais, strategies, delay=0.01, last_update_time=last_update_time)

        key = stdscr.getch()
        if key == curses.KEY_F12:
            reset_curses()
            screen = initialize_graphics()
            game_loop_graphics(screen, strategies)
            break
        elif key == 27:  # Touche Échap pour ouvrir le menu
            escape_menu_curses(stdscr)

def game_loop_graphics(screen, strategies):

    global units, buildings, game_map, ai

    # Initialiser pygame pour le mode graphique
    screen = initialize_graphics()

    running = True
    clock = pygame.time.Clock()
    view_x, view_y = 0, 0
    max_width = screen_width // TILE_WIDTH
    max_height = screen_height // TILE_HEIGHT
    last_update_time = time.time()

    while running:
        current_time = time.time()
        
        # Gère les entrées utilisateur pour le scrolling de la carte
        view_x, view_y = handle_input_pygame(view_x, view_y, max_width, max_height, game_map)
        
        # Mise à jour du jeu à intervalles réguliers
        last_update_time = update_game(units, buildings, game_map, ais, strategies, delay=0.05, last_update_time=last_update_time)


        # Rendu de la carte et des unités
        render_map(screen, game_map, units, buildings, ais, view_x, view_y, max_width, max_height)



        # Gérer les événements Pygame (fermeture de fenêtre, bascule de mode, menu)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F12:
                    pygame.quit()
                    curses.wrapper(lambda stdscr: game_loop_curses(stdscr, strategies))
                    return
                elif event.key == pygame.K_ESCAPE:
                    escape_menu_graphics(screen)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()



def main_menu_curses():
    curses.wrapper(main_menu_curses_internal)

def main_menu_curses_internal(stdscr):
    options = ["1. Charger une partie", "2. Nouvelle partie", "3. Quitter"]
    selected_option = 0

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "Menu Principal:")
        for i, option in enumerate(options):
            if i == selected_option:
                stdscr.addstr(i + 1, 0, option, curses.A_REVERSE)  # Option surlignée
            else:
                stdscr.addstr(i + 1, 0, option)
        stdscr.refresh()

        key = stdscr.getch()
        if key == curses.KEY_DOWN:
            selected_option = (selected_option + 1) % len(options)
        elif key == curses.KEY_UP:
            selected_option = (selected_option - 1) % len(options)
        elif key == ord('\n'):  # Touche entrée
            if selected_option == 0:  # Charger une partie
                load_existing_game_curses(stdscr)
            elif selected_option == 1:  # Nouvelle partie
                start_new_game_curses(stdscr)
            elif selected_option == 2:  # Quitter
                sys.exit(0)


def start_new_game_curses(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 0, "Réglage de la nouvelle partie:")

    # Options configurables
    input_fields = [
        ("Taille de la carte (par défaut 120x120): ", "120"),
        ("Nombre de joueurs (IA) (par défaut 2): ", "2"),
        ("Nombre de clusters de bois (par défaut 10): ", "10"),
        ("Nombre de clusters d'or (par défaut 4): ", "4")
    ]
    input_values = []

    curses.echo()
    for idx, (prompt, default) in enumerate(input_fields):
        stdscr.addstr(idx + 1, 0, prompt)
        stdscr.addstr(idx + 1, len(prompt), default)  # Affiche la valeur par défaut
        stdscr.move(idx + 1, len(prompt))  # Place le curseur à la bonne position

        value = ""
        while True:
            key = stdscr.getch()

            if key == ord('\n'):  # Touche Entrée
                if value.strip() == "":
                    value = default  # Si aucune entrée, utilise la valeur par défaut
                break
            elif key in [curses.KEY_BACKSPACE, 127]:  # Touche Backspace
                value = value[:-1]
                stdscr.addstr(idx + 1, len(prompt), " " * (len(value) + 10))  # Efface la ligne précédente
                stdscr.addstr(idx + 1, len(prompt), value)
                stdscr.move(idx + 1, len(prompt) + len(value))
            elif 32 <= key <= 126:  # Caractères imprimables uniquement
                value += chr(key)
                stdscr.addstr(idx + 1, len(prompt), value)
                stdscr.move(idx + 1, len(prompt) + len(value))

        input_values.append(value)

    # Récupération des valeurs
    try:
        map_size = int(input_values[0])
        if map_size < 120:  # Taille minimale imposée
            stdscr.addstr(len(input_fields) + 2, 0, "Erreur : La taille minimale de la carte est 120x120. Valeur forcée à 120.")
            stdscr.refresh()
            time.sleep(2)
            map_size = 120
        num_players = int(input_values[1])
        wood_clusters = int(input_values[2])
        gold_clusters = int(input_values[3])
    except ValueError:
        stdscr.addstr(len(input_fields) + 2, 0, "Erreur : Entrée invalide, utilisation des valeurs par défaut.")
        stdscr.refresh()
        time.sleep(2)
        map_size = 120
        num_players = 2
        wood_clusters = 10
        gold_clusters = 4

    # Initialisation de la nouvelle partie
    global units, buildings, game_map, ais
    game_map = Map(map_size, map_size)
    game_map.generate_forest_clusters(num_clusters=wood_clusters, cluster_size=40)
    game_map.generate_gold_clusters(num_clusters=gold_clusters)

    ais = []
    units = []
    buildings = []

    # Créer les IA, Town Centers, et assigner les unités
    for i in range(num_players):
        town_center_x, town_center_y = 10 + i * 20, 10 + i * 20
        ai = AI([], [])  # Crée une nouvelle IA
        ais.append(ai)

        town_center = Building('Town Center', town_center_x, town_center_y, owner=ai)
        ai.town_center = town_center  # Ajoutez cette ligne pour associer explicitement le Town Center à l'IA

        game_map.place_building(town_center, town_center_x, town_center_y, buildings)
        buildings.append(town_center)
        ai.buildings.append(town_center)  # Associe le bâtiment à l'IA

        for j in range(3):  # 3 unités par IA
            villager_x, villager_y = town_center_x + j, town_center_y + j
            villager = Unit('Villager', villager_x, villager_y, ai)
            units.append(villager)
            ai.units.append(villager)

    # Configuration des ennemis pour chaque IA
    for ai in ais:
        ai.set_enemies([a for a in ais if a != ai])

    # Initialisation des stratégies
    strategies = initialize_strategies(ais)

    # Debug : afficher les bâtiments de chaque IA
    for i, ai in enumerate(ais):
        print(f"IA {i + 1} possède les bâtiments : {[b.building_type for b in ai.buildings]} avec Town Center à ({ai.town_center.x}, {ai.town_center.y})")


    # Debug : vérifier les tuiles de la carte
    game_map.debug_tile_dict()

    # Lancer la boucle de jeu en passant `strategies` en paramètre
    curses.wrapper(game_loop_curses, strategies)



def main_menu_graphics():
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    font = pygame.font.Font(None, 36)
    options = ["1. Charger une partie", "2. Nouvelle partie", "3. Quitter"]
    selected_option = 0
    running = True

    while running:
        screen.fill((0, 0, 0))
        for i, option in enumerate(options):
            color = (255, 255, 255) if i == selected_option else (100, 100, 100)
            text = font.render(option, True, color)
            screen.blit(text, (20, 50 + i * 40))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(options)
                elif event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(options)
                elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    if selected_option == 0:  # Charger une partie
                        load_existing_game_graphics(screen, font)
                    elif selected_option == 1:  # Nouvelle partie
                        start_new_game_graphics(screen, font)
                    elif selected_option == 2:  # Quitter
                        sys.exit(0)


def start_new_game_graphics(screen, font):
    input_fields = [
        ("Taille de la carte (par défaut 120x120): ", "120"),
        ("Nombre de joueurs (IA) (par défaut 2): ", "2"),
        ("Nombre de clusters de bois (par défaut 10): ", "10"),
        ("Nombre de clusters d'or (par défaut 4): ", "4")
    ]
    input_values = []

    # Saisie des paramètres par l'utilisateur
    for prompt, default in input_fields:
        input_text = default
        running = True
        while running:
            screen.fill((0, 0, 0))
            prompt_surface = font.render(prompt, True, (255, 255, 255))
            input_surface = font.render(input_text, True, (255, 255, 255))
            screen.blit(prompt_surface, (20, 50))
            screen.blit(input_surface, (20, 100))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        running = False
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    elif 32 <= event.key <= 126:
                        input_text += event.unicode

        input_values.append(input_text)

    # Validation des entrées
    try:
        map_size = int(input_values[0])
        if map_size < 120:  # Taille minimale imposée
            map_size = 120
        num_players = int(input_values[1])
        wood_clusters = int(input_values[2])
        gold_clusters = int(input_values[3])
    except ValueError:
        map_size = 120
        num_players = 2
        wood_clusters = 10
        gold_clusters = 4

    # Initialisation de la nouvelle partie
    global units, buildings, game_map, ais
    game_map = Map(map_size, map_size)
    game_map.generate_forest_clusters(num_clusters=wood_clusters, cluster_size=40)
    game_map.generate_gold_clusters(num_clusters=gold_clusters)

    ais = []
    units = []
    buildings = []

    # Création des joueurs IA, Town Centers, et assignation des unités
    for i in range(num_players):
        town_center_x, town_center_y = 10 + i * 20, 10 + i * 20
        ai = AI([], [])  # Crée une nouvelle IA
        ais.append(ai)

        town_center = Building('Town Center', town_center_x, town_center_y, owner=ai)
        ai.town_center = town_center  # Associe explicitement le Town Center à l'IA

        game_map.place_building(town_center, town_center_x, town_center_y, buildings)
        buildings.append(town_center)
        ai.buildings.append(town_center)  # Associe le bâtiment à l'IA

        for j in range(3):  # 3 unités par IA
            villager_x, villager_y = town_center_x + j, town_center_y + j
            villager = Unit('Villager', villager_x, villager_y, ai)
            units.append(villager)
            ai.units.append(villager)

    # Configuration des ennemis pour chaque IA
    for ai in ais:
        ai.set_enemies([a for a in ais if a != ai])

    # Initialisation des stratégies
    strategies = initialize_strategies(ais)

    # Debug : afficher les bâtiments de chaque IA
    for i, ai in enumerate(ais):
        print(f"IA {i + 1} possède les bâtiments : {[b.building_type for b in ai.buildings]} avec Town Center à ({ai.town_center.x}, {ai.town_center.y})")

    # Debug : vérifier les tuiles de la carte
    game_map.debug_tile_dict()

    # Lancer la boucle graphique
    game_loop_graphics(screen, strategies)




def render_text(screen, font, text, position, color=(255, 255, 255)):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, position)



def init_game():
    global units, buildings, game_map, ai, ai
    os.makedirs(SAVE_DIR, exist_ok=True)
    if loaded_units and loaded_buildings and loaded_map and loaded_ai:
        units, buildings, game_map, ai = loaded_units, loaded_buildings, loaded_map, loaded_ai
    else:
        game_map = Map(max(120, 120), max(120, 120))
        game_map.generate_forest_clusters(num_clusters=10, cluster_size=40)
        game_map.generate_gold_clusters(num_clusters=4)
        town_center = Building('Town Center', 10, 10)
        game_map.place_building(town_center, 10, 10)
        ai = AI(buildings, units)  # Initialisation de l'objet AI
        villager = Unit('Villager', 9, 9, ai)
        villager2 = Unit('Villager', 12, 9, ai)
        villager3 = Unit('Villager', 9, 12, ai)
        units = [villager, villager2, villager3]
        buildings = [town_center]
        ai = AI(ai, buildings, units)  # Passage de l'objet ai à l'IA

def main():
    # Ne pas initialiser pygame à moins que le mode graphique soit spécifié
    if 'graphics' in sys.argv:
        main_menu_graphics()
    else:
        main_menu_curses()

if __name__ == "__main__":
    main()
