import pygame
import pygame_menu
import pygame_menu.themes

# Définitions des constantes
HAUTEUR_PAGE = 650
LARGEUR_PAGE = 900

pygame.init()
surface = pygame.display.set_mode((LARGEUR_PAGE, HAUTEUR_PAGE))

# Définitions des fonctions
def ChoisirDifficulte(value, difficulty):
    # Do the job here !
    pass

def LancerUnePartie():
    # Do the job here !
    pass

def ChoisirNbrBots(Number, Value):
    # Choix du nombre de bots
    pass

def ParametreDeJeu():
    # Paramètrages de la partie
    pass

# Définitions des différents menus
menu = pygame_menu.Menu('Welcome', LARGEUR_PAGE, HAUTEUR_PAGE,
                       theme=pygame_menu.themes.THEME_DARK)

parametre_menu = pygame_menu.Menu('Paramètres', LARGEUR_PAGE, HAUTEUR_PAGE,
                                  theme=pygame_menu.themes.THEME_DARK)

menu.add.text_input('Name : ', default='Vincent Hugo')
menu.add.button('Jouer', LancerUnePartie)
menu.add.button('Paramètres', parametre_menu)
menu.add.button('Quitter', pygame_menu.events.EXIT)

parametre_menu.add.selector('Nombres de Joueurs : ', [('1', 1), ('2', 2)], onchange=ChoisirNbrBots)
parametre_menu.add.selector('Difficulté des Bots : ', [('Hard', 1), ('Easy', 2)], onchange=ChoisirDifficulte)
parametre_menu.add.selector('Stratégie des Bots : ', [('Aggressif', 1), ('Défenseur', 2)])

# Lancement de la fenêtre
menu.mainloop(surface)
