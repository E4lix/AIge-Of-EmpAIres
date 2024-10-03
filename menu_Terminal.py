# Menu de "AIge of EmpAIres" en Interface Shell
# Ce programme va permettre d'avoir un menu sur l'interface Terminal pour sélectionner les différents paramètres qui
# composent notre jeu. Les élements seront le Lancement d'une partie, la Sélection des Bots, les Paramètres de jeu et
# enfin l'option Quitter le jeu

# Importations des Librairies

# Définitions des fonctions
def LancerUnePartie():
    # Protocole de la partie
    return 1


def SelectionDesBots():
    return 1


def ParametresDeJeu():
    def textParametres():
        print("Menu des Paramètres \n")
        print("Veuillez Sélectionner le paramètre à modifier : \n")
        print("1 - Taille de la map \n2 - Richesse des Ressources \n3 - Menu Principal")

    textParametres()
    Choix = int(input("Votre choix : "))
    while Choix != '':
        if Choix == 1:
            n = int(input("Hauteur de la map : "))
            while n<120:
                n = int(input("Minimum 120, Hauteur de la map : "))
            
            textParametres()
            Choix = int(input("Nouveau Choix : "))
        
        if Choix == 2:
            print("Lean - 50F, 200W, 50G, 1 centre-ville, 3 villageois.")
            print("Mean - 2000 (F, W, G), 1 centre-ville, 3 villageois.")
            print("Marines - 20000 (F, W, G), 3 centres-villes, 15 villageois, 2 casernes/écuries/stands de tir.")
            Richesse = input("Choix de la richesse de la map : ")
            ListeChoix = ["Lean","Mean","Marines"]
            while Richesse not in ListeChoix:
                Richesse = input("Choix Invalide, Nouveau Choix : ")

            textParametres()
            Choix = int(input("Nouveau Choix : "))

        if Choix == 3:
            return Richesse
        

def menu():
    def textMenuPrincipal():
        print("Menu Principal \n")
        print("1 - Lancer une partie \n2 - Sélection des Bots \n3 - Paramètres de jeu \n4 - Quitter le jeu \n")

    textMenuPrincipal()

    # Choix de l'utilisateur
    Choix = int(input("Veuillez sélectionner une option : "))

    while Choix != '':
        if Choix == 1:
            print("Choix 1 - Lancer une partie")
            LancerUnePartie()
            textMenuPrincipal()
            Choix = int(input("Nouveau Choix : "))
        if Choix == 2:
            print("Choix 2 - Sélection des Bots")
            SelectionDesBots()
            textMenuPrincipal()
            Choix = int(input("Nouveau Choix : "))
        if Choix == 3:
            print("Choix 3 - Paramètres du Jeu")
            Richesse = ParametresDeJeu()
            textMenuPrincipal()
            Choix = int(input("Nouveau Choix : "))
        if Choix == 4:
            print("Fin du Jeu, Merci d'avoir joué \n")
            return 1
        else:
            Choix = int(input("Veuillez entrer un choix valide : "))


# Programme Principal
menu()
