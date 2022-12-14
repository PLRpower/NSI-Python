from random import random, choice
from tkinter import *

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

from Carte import Carte


class Params:
    """Classe gérant les paramètres"""

    # Paramètres non modifiables lors de l’exécution :
    border = 1
    largeur_pixels = 900
    hauteur_pixels = 600

    def __init__(self):
        # Paramètres modifiables à la volée :
        self.dt = 100
        self.auto = True

        self.fen_para = Toplevel()  # Fenêtre de réglages
        self.fen_para.resizable(width=FALSE, height=FALSE)
        self.fen_para.protocol('WM_DELETE_WINDOW', hide_param)
        self.fen_para.title("Paramètres")
        self.fen_para.withdraw()

        tailles = ("petit", "moyen", "grand")
        self.taille = StringVar(self.fen_para, value=tailles[0])
        self.optiontaille = OptionMenu(self.fen_para, self.taille, *tailles)
        self.taille.trace("w", lambda *e: self.change_taille())
        # la fonction self.change_taille() est appelée
        # lorsque la valeur de self.taille change
        self.optiontaille.pack()

        self.tore = BooleanVar(self.fen_para, value=False)
        self.checktore = Checkbutton(self.fen_para, text="Tore", variable=self.tore,
                                     onvalue=True, offvalue=False)
        self.checktore.pack()

        self.bouton_close = Button(self.fen_para, text="Fermer", command=hide_param)
        self.bouton_close.pack()

        # paramètres éventuellement modifiables juste avant réinitialisation :
        self.niveau_herbe = 20

        self.taille_largeur = {"petit": 25, "moyen": 35, "grand": 50}
        # largeur en cases selon la taille
        self.taille_lapin = {"petit": 10, "moyen": 20, "grand": 50}
        # nombre de lapins selon la taille
        self.taille_loup = {"petit": 5, "moyen": 7, "grand": 20}
        # nombre de loups selon la taille

        self.nouvelle_largeur(self.taille_largeur[self.taille.get()])

    def nouvelle_largeur(self, l):
        """Définit les longueurs en fonction du nombre l de cases en largeur"""
        self.largeur = l
        self.taille_case = Params.largeur_pixels // l
        self.hauteur = Params.hauteur_pixels // self.taille_case

    def change_taille(self):
        """Effectue le changement de largeur puis réinitialise le terrain"""
        self.nouvelle_largeur(self.taille_largeur[self.taille.get()])
        init()


class Animal:
    """Classe mère pour chaque animal"""

    def __init__(self, age_max, age_repro, metabo, meta_max, conso, meta_repro, classe, valeur_repas=0):
        self.age = 0
        self.age_max = age_max
        self.age_repro = age_repro
        self.metabo = metabo
        self.meta_max = meta_max
        self.meta_repro = meta_repro
        self.conso = conso
        self.classe = classe
        self.valeur_repas = valeur_repas

    def se_reproduit(self):
        """Indique par un booléen si l’animal se reproduit"""
        if self.age >= self.age_repro and self.metabo >= self.meta_repro:
            return random() > 0.5
        else:
            return False

    def nourrir(self, quantite=None):
        """Nourrit l’animal d’une quantité donnée ou de la valeur d’un repas"""
        if quantite is None:
            self.metabo = min(self.meta_max, self.metabo + self.valeur_repas)
        else:
            self.metabo = min(self.meta_max, self.metabo + quantite)

    def vieillir(self):
        """vieillit l’animal"""
        self.age += 1
        self.metabo -= self.conso

    def meurt(self):
        """Indique si l’animal meurt"""
        return self.age >= self.age_max or self.metabo <= 0


class Loup(Animal):
    def __init__(self):
        Animal.__init__(self, metabo=100, meta_max=200, conso=2, age_max=50, age_repro=10, meta_repro=120,
                        classe="loup", valeur_repas=10)


class Lapin(Animal):
    def __init__(self):
        Animal.__init__(self, metabo=20, meta_max=45, conso=3, age_max=25, age_repro=10, meta_repro=40, classe="lapin",
                        valeur_repas=5)


def cases_voisines(x, y):
    voisins = []
    # Si le tore est activé, on ajoute les cases voisines
    if carte.params.tore.get():
        voisins.append(((x - 1) % carte.params.largeur, y))
        voisins.append(((x + 1) % carte.params.largeur, y))
        voisins.append((x, (y - 1) % carte.params.hauteur))
        voisins.append((x, (y + 1) % carte.params.hauteur))
    # Si le tore est désactivé, on vérifie si les cases voisines sont bien dans la carte
    else:
        if x > 0:
            voisins.append((x - 1, y))
        if x < carte.params.largeur - 1:
            voisins.append((x + 1, y))
        if y > 0:
            voisins.append((x, y - 1))
        if y < carte.params.hauteur - 1:
            voisins.append((x, y + 1))
    return voisins


def vieillir_animaux():
    """Fait vieillir chaque animal selon les règles.
    Si, ce faisant, un animal meurt, on l’élimine du terrain"""
    for (x, y), (animal, _) in list(carte.animal.items()):
        animal.vieillir()  # Faire vieillir l'animal
        if animal.meurt():  # Vérifier si l'animal meurt
            carte.elimine_animal(x, y)  # Le supprimer de la carte


def nourrir_animaux():
    """Nourrit chaque animal selon les règles"""
    for (x, y), (animal, _) in carte.animal.items():
        if animal.classe == "lapin":  # Si l'animal est un lapin
            carte.coupe_herbe(x, y)  # Couper l'herbe
            animal.nourrir()  # Nourrir le lapin

def reproduire_animaux():
    """Fait se reproduire les animaux selon les règles"""
    for (x0, y0), (animal, _) in list(carte.animal.items()):
        if animal.se_reproduit():  # Si l'animal est capable de se reproduire
            while True:  # Tant que la case générée aléatoirement est occupée, en générer une autre
                x, y = choice(cases_voisines(x0, y0))  # Case aléatoire autour de l'animal
                if (x, y) not in carte.animal.keys():  # Si il n'y a pas d'autre animal dans cette case
                    if animal.classe == "lapin":
                        carte.place_animal(Lapin(), x, y)  # Placer un lapin
                    else:
                        carte.place_animal(Loup(), x, y)  # Placer un loup
                    break


def deplacer_animaux():
    """Fait se déplacer les animaux selon les règles"""
    for (x0, y0) in list(carte.animal.keys()):
        herbe = {}
        for x, y in cases_voisines(x0, y0):  # Parcourir les cases voisines
            herbe[(x, y)] = carte.herbe[x][y][0]  # Sauvegarder la taille de l'herbe de la case*
        herbe_trie = sorted(herbe.items(), key=lambda x: x[1], reverse=True)[0][
            1]  # Trier la taille de l'herbe (décroissant)
        maximum_herbe = [case for case in herbe_trie if case[1] == herbe_trie]  # Trouver les valeurs maximum de l'herbe
        case_aleatoire = choice(maximum_herbe)[0]  # Faire un choix aléatoire parmi le maximum d'herbe
        x, y = case_aleatoire
        if (x, y) not in carte.animal.keys():  # Si il n'y a pas d'autre animal dans cette case
            carte.bouge_animal(x0, y0, x, y)  # Bouger l'animal dans la case choisie
        else:
            herbe_trie.pop(case_aleatoire)
            continue


def cycle():
    """Exécute un cycle et le redémarre si on est en mode auto"""
    global continuer

    vieillir_animaux()
    nourrir_animaux()
    reproduire_animaux()
    deplacer_animaux()
    carte.faire_pousser_herbe()

    graph.ajoute_point()
    if bouton_graph.cget('text') == "Cacher":  # Graphique ouvert
        graph.update()

    if carte.params.auto:
        continuer = carte.after(carte.params.dt, cycle)
        # Relancera la fonction cycle après carte.params.dt ms


def demarrer():
    """Démarre l’exécution répétée des cycles"""
    carte.params.auto = True
    bouton_start.configure(text="Stopper", command=stop)
    bouton_pas.configure(state='disabled')
    bouton_reset.configure(state='disabled')
    bouton_param.configure(state='disabled')
    cycle()


def pas():
    """Fait exécuter un seul cycle"""
    carte.params.auto = False
    cycle()


def stop():
    """Stoppe l’exécution des cycles"""
    carte.after_cancel(continuer)
    bouton_start.configure(text="Démarrer", command=demarrer)
    bouton_pas.configure(state='normal')
    bouton_reset.configure(state='normal')
    bouton_param.configure(state='normal')


class Graph():
    def __init__(self):
        self.x = []  # liste de valeurs d’unité de temps (abscisse x)
        self.g = []  # liste des nombres de cases vides/sol libre (ground)
        self.r = []  # liste des nombres de lapins (rabbit)
        self.w = []  # liste des nombres de loups (wolf)

        self.graph = Toplevel()  # fenêtre d’affichage du graphique
        self.graph.resizable(width=FALSE, height=FALSE)
        self.graph.protocol('WM_DELETE_WINDOW', hide_graph)
        self.graph.title("Courbe")

        self.fig, self.ax = plt.subplots()  # figure

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph)
        self.canvas.get_tk_widget().pack()
        self.canvas.draw()  # affiche la figure
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.graph)
        self.toolbar.update()  # met en place la barre d’outils
        self.withdraw()  # cache la fenêtre

    def get_vector(self):
        """Obtient et retourne les quantités de sol libre, lapins et loups
        sous forme de liste"""
        pass

    def reinit(self):
        """Réinitialise les données du graphique
        avec le vecteur initial puis le réaffiche"""
        pass

    def update(self):
        """Met à jour/réaffiche le graphique"""
        pass

    def ajoute_point(self):
        """Ajoute un point en mettant à jour
        les contenus des quatre listes de valeurs"""
        pass

    def withdraw(self):
        """Retire la fenêtre du graphique"""
        self.graph.withdraw()

    def deiconify(self):
        """Affiche la fenêtre du graphique
        et le met à jour"""
        self.graph.deiconify()
        self.update()


def show_graph():
    """Montrer le graphique"""
    bouton_graph.configure(text="Cacher", command=hide_graph)
    graph.deiconify()


def hide_graph():
    """Cacher le graphique"""
    bouton_graph.configure(text="Courbe", command=show_graph)
    graph.withdraw()


def show_param():
    """Affiche la fenêtre des paramètres"""
    for child in zone_boutons.winfo_children():
        child.configure(state='disabled')
    carte.params.fen_para.deiconify()


def hide_param():
    """Cache la fenêtre des paramètres"""
    carte.params.fen_para.withdraw()
    for child in zone_boutons.winfo_children():
        child.configure(state='normal')


def exemples():
    """Exemples d’utilisations d’éléments du programme"""

    # Les exemples suivants sont seulement là pour illustrer les méthodes

    # Exemples d’utilisation de la carte :
    carte.place_animal(Lapin(), 12, 0)  # Crée et place quelques animaux
    carte.place_animal(Lapin(), 2, 7)
    carte.place_animal(Loup(), 24, 7)

    print("Nombre d’animaux :", len(carte.animal))

    carte.bouge_animal(24, 7, 10, 6)  # Déplace un des animaux
    un = carte.coupe_herbe(20, 10)  # Coupe l’herbe d’une case
    print("quantité d'herbe coupée :", un)
    carte.elimine_animal(12, 0)  # Élimine un des animaux

    # Exemples d’utilisation des animaux
    (x, y), (animal, _) = list(carte.animal.items())[0]  # On prend un animal
    # (par une méthode qui n'est pas à utiliser par la suite)

    print(animal.classe)  # classe de l’animal (voir plus loin une autre manière)
    for _ in range(10):
        animal.vieillir()
        animal.nourrir(5)  # pour un lapin, il faut donner la quantité d’herbe
        animal.nourrir()  # pour les loups, la quantité ne dépend pas du lapin
    for _ in range(3):
        animal.vieillir()
        print("âge :", animal.age)
        animal.nourrir(10)
        print("métabolisme :", animal.metabo)
        print("Se reproduit ?", animal.se_reproduit())
    while not animal.meurt():
        animal.vieillir()
    print("meurt à l’âge de", animal.age, "ans")
    carte.elimine_animal(x, y)

    carte.place_animal(Lapin(), 5, 0)  # Place un nouveau lapin

    for (x, y) in [(24, 7), (5, 0)]:
        if (x, y) in carte.animal.keys():  # Tester la présence d’un animal
            print("Il y a un animal présent en", str((x, y)))
            classe = carte.animal[(x, y)][0].classe  # classe de l’animal
            print("Sa classe est :", classe)
        else:
            print("Aucun animal présent en", str((x, y)))

    print("Valeur de l’option tore :", carte.params.tore.get())
    print("Valeur de l’option taille :", carte.params.taille.get())
    # Ces deux variables sont particulières


def init():
    """Réinitialise le terrain et le graphique.
    Place des lapins et loups en fonction des paramètres"""
    carte.reinit()
    graph.reinit()

    generation()

    # exemples()
    pass


def generation():
    """Réinitialise le terrain et le graphique.
    Place des lapins et loups en fonction des paramètres"""
    carte.place_animal(Lapin(), 12, 0)  # Crée et place quelques animaux
    carte.place_animal(Lapin(), 2, 7)
    carte.place_animal(Loup(), 24, 7)


def _quit():
    fenetre.quit()  # arrête le mainloop
    fenetre.destroy()


if __name__ == '__main__':
    fenetre = Tk()
    fenetre.config(bg='white')
    fenetre.title('Proies prédateurs')
    fenetre.resizable(width=FALSE, height=FALSE)
    fenetre.protocol('WM_DELETE_WINDOW', _quit)

    carte = Carte(fenetre, Params())  # Crée et place le terrain appelé carte
    graph = Graph()

    zone_boutons = Frame(fenetre, bg="white")
    zone_boutons.pack()
    bouton_start = Button(zone_boutons, text="Démarrer", command=demarrer)
    bouton_start.grid(column=0, row=0)
    bouton_pas = Button(zone_boutons, text="Un pas", command=pas)
    bouton_pas.grid(column=1, row=0)
    bouton_reset = Button(zone_boutons, text="Reset", command=init)
    bouton_reset.grid(column=0, row=1, sticky="ew")
    bouton_graph = Button(zone_boutons, text="Courbe", command=show_graph)
    bouton_graph.grid(column=1, row=1, sticky="ew")
    bouton_param = Button(zone_boutons, text="Paramètres", command=show_param)
    bouton_param.grid(column=0, columnspan=2, row=2, sticky="ew")

    init()

    fenetre.mainloop()
