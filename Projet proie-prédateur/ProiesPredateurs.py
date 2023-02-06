#! /usr/bin/python3
# -*- coding: utf-8 -*-

from random import random, randint, shuffle
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

        tailles = ("Petit", "Moyen", "Grand")
        self.taille = StringVar(self.fen_para, value=tailles[0])
        self.optiontaille = OptionMenu(self.fen_para, self.taille, *tailles)
        self.taille.trace("w", lambda *e: self.change_taille())
        # la fonction self.change_taille() est appelée
        # lorsque la valeur de self.taille change
        self.optiontaille.pack()

        self.tore = BooleanVar(self.fen_para, value=False)
        self.checktore = Checkbutton(self.fen_para, text="Tore", variable=self.tore, onvalue=True, offvalue=False)
        self.checktore.pack()

        self.loup_intelligent = BooleanVar(self.fen_para, value=False)
        self.check_loup = Checkbutton(self.fen_para, text="Loups intelligents", variable=self.loup_intelligent,
                                      onvalue=True, offvalue=False)
        self.check_loup.pack()

        self.lapin_intelligent = BooleanVar(self.fen_para, value=False)
        self.check_lapin = Checkbutton(self.fen_para, text="Lapins intelligents", variable=self.lapin_intelligent,
                                       onvalue=True, offvalue=False)
        self.check_lapin.pack()

        self.bouton_close = Button(self.fen_para, text="Fermer", command=hide_param)
        self.bouton_close.pack()

        # paramètres éventuellement modifiables juste avant réinitialisation :
        self.niveau_herbe = 20

        self.taille_largeur = {"Petit": 25, "Moyen": 35, "Grand": 50}
        # largeur en cases selon la taille
        self.taille_lapin = {"Petit": 10, "Moyen": 20, "Grand": 50}
        # nombre de lapins selon la taille
        self.taille_loup = {"Petit": 5, "Moyen": 7, "Grand": 20}
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
        """Vieillit l’animal"""
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
        Animal.__init__(self, metabo=20, meta_max=45, conso=3, age_max=25, age_repro=10, meta_repro=40, classe="lapin")


def cases_voisines(x, y):
    """Retourne la liste des coordonnées des cases voisines (non diagonales).
    Dépend de la valeur de carte.params.tore"""
    voisins = []
    if carte.params.tore.get():  # Si le tore est activé, on ajoute simplement les cases voisines
        voisins.append(((x - 1) % carte.params.largeur, y))
        voisins.append(((x + 1) % carte.params.largeur, y))
        voisins.append((x, (y - 1) % carte.params.hauteur))
        voisins.append((x, (y + 1) % carte.params.hauteur))
    else:  # Si le tore est désactivé, on vérifie si les cases voisines sont bien dans la carte, puis on les ajoute
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
        if animal.meurt():  # Vérifier si l'animal meurt
            carte.elimine_animal(x, y)  # Le supprimer de la carte
        else:
            animal.vieillir()  # Faire vieillir l'animal


def nourrir_animaux():
    """Nourrit chaque animal selon les règles"""
    for (x0, y0), (animal, _) in list(carte.animal.items()):
        if animal.classe == "lapin":  # Si l'animal est un lapin
            herbe = round(carte.herbe[x0][y0][0] / 3)  # Valeur du repas
            animal.nourrir(herbe)  # Nourrir le lapin
            carte.coupe_herbe(x0, y0)  # Couper l'herbe
        else:  # Si l'animal est un loup
            for (x, y) in cases_voisines(x0, y0):  # Parcourir les cases voisines
                if (x, y) in carte.animal and carte.animal[(x, y)][
                    0].classe == "lapin":  # Tester la présence d’un lapin
                    carte.elimine_animal(x, y)  # Éliminer le lapin
                    animal.nourrir()  # Nourrir le loup


def reproduire_animaux():
    """Fait se reproduire les animaux selon les règles"""
    for (x0, y0), (animal, _) in list(carte.animal.items()):
        if animal.se_reproduit():  # Si l'animal est capable de se reproduire
            cases = cases_voisines(x0, y0)
            shuffle(cases)
            for x, y in cases:
                if (x, y) not in carte.animal:  # Si il n'y a pas d'autre animal dans cette case
                    carte.place_animal(Lapin() if animal.classe == "lapin" else Loup(), x, y)
                    break


def deplacer_animaux():
    """Fait se déplacer les animaux selon les règles"""
    for (x0, y0), (animal, _) in list(carte.animal.items()):  # Parcourir les animaux
        if animal.classe == "lapin":  # Si l'animal est un lapin
            deplacer_lapin(x0, y0)  # Déplacer le lapin selon les règles
        elif animal.classe == "loup":  # Si l'animal est un loup
            deplacer_loup(x0, y0)  # Déplacer le loup selon les règles


def deplacer_lapin(x0, y0):
    """Fait se déplacer les lapins selon les règles (lapin intelligent/tore)"""
    if carte.params.lapin_intelligent.get():  # Si l'option "lapins intelligents" est activé
        herbe = {(x, y): carte.herbe[x][y][0] for x, y in
                 cases_voisines(x0, y0)}  # Obtenir la liste de l'herbe autour du lapin avec la hauteur de l'herbe
        herbe_max = max(herbe.items(), key=lambda x: x[1])[1]  # Trouver la valeur de l'herbe la plus haute
        coordonnees_herbe_max = [k for k, v in herbe.items() if
                                 v == herbe_max]  # Trouver toutes les cases ayant l'herbe maximale
        shuffle(coordonnees_herbe_max)
        deplacement(x0, y0, coordonnees_herbe_max)  # Déplacer l'animal dans la première case libre autour de lui.
    else:  # Si l'option "lapins intelligents" est désactivé
        voisins = cases_voisines(x0, y0)  # Obtenir les cases voisines du lapin
        shuffle(voisins)  # Mélanger la liste des cases afin de se déplacer aléatoirement
        deplacement(x0, y0, voisins)  # Se déplacer dans la première case libre de la liste


def deplacer_loup(x0, y0):
    """Fait se déplacer les loups selon les règles (loup intelligent/tore)"""
    lapins = [(x, y) for (x, y), (animal, _) in list(carte.animal.items()) if
              animal.classe == "lapin"]  # Obtenir la liste des coordonnées des lapins
    if lapins and carte.params.loup_intelligent.get():  # S'il reste des lapins et que l'option "loups intelligents" est activé
        lapin_proche = min(lapins, key=lambda coord: calcul_distance(x0, y0, coord[0], coord[
            1]))  # Calculer et obtenir les coordonnés du lapin le plus proche
        cases_autour = sorted(cases_voisines(x0, y0),
                              key=lambda coord: calcul_distance(coord[0], coord[1], lapin_proche[0], lapin_proche[
                                  1]))  # Obtenir les cases voisines dans l'ordre du plus proche au moins proche du lapin
        deplacement(x0, y0, cases_autour)  # Déplacer le loup la première case libre autour de lui
    else:  # Si l'option "loups intelligents" est désactivé
        voisins = cases_voisines(x0, y0)  # Obtenir les cases voisines du loup
        shuffle(voisins)  # Mélanger la liste des cases afin de se déplacer aléatoirement
        deplacement(x0, y0, voisins)  # Se déplacer dans la première case libre de la liste


def calcul_distance(x0, y0, x1, y1):
    """Calcul d'une distance entre deux cases"""
    if carte.params.tore.get():  # Si le tore est activé
        dx = min(abs(x0 - x1), carte.params.largeur - abs(x0 - x1))
        dy = min(abs(y0 - y1), carte.params.largeur - abs(y0 - y1))
        return dx ** 2 + dy ** 2
    else:  # Si le tore est désactivé
        return (x0 - x1) ** 2 + (y0 - y1) ** 2


def deplacement(x0, y0, coordonnees):
    """Déplacement d'un animal sur la première case libre de la liste des cases"""
    for x, y in coordonnees:
        if (x, y) not in carte.animal:  # Si il n'y a pas d'autre animal dans cette case
            carte.bouge_animal(x0, y0, x, y)  # Bouger l'animal dans la case choisie
            break


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


class Graph:
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
        return [self.g, self.r, self.w]

    def reinit(self):
        """Réinitialise les données du graphique
        avec le vecteur initial puis le réaffiche"""
        self.x = []
        self.g = []
        self.r = []
        self.w = []
        self.update()

    def update(self):
        """Met à jour/réaffiche le graphique"""
        self.ax.clear()
        self.ax.plot(self.x, self.g, label='Sol libre')
        self.ax.plot(self.x, self.r, label='Lapins')
        self.ax.plot(self.x, self.w, label='Loups')
        self.ax.legend()
        self.ax.set_xlabel('Temps')
        self.ax.set_ylabel('Quantité')
        self.ax.set_title('Évolution de la population')
        self.canvas.draw()

    def ajoute_point(self):
        """Ajoute un point en mettant à jour
        les contenus des quatre listes de valeurs"""
        lapins = sum(1 for _, (animal, _) in carte.animal.items() if animal.classe == "lapin")
        loups = sum(1 for _, (animal, _) in carte.animal.items() if animal.classe == "loup")
        x_len = len(self.x)
        self.r.append(lapins)
        self.w.append(loups)
        self.g.append(carte.params.largeur * carte.params.hauteur - (lapins + loups))
        self.x.append(x_len + 1)
        self.update()

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


def init():
    """Réinitialise le terrain et le graphique.
    Place des lapins et loups en fonction des paramètres"""
    carte.reinit()
    graph.reinit()

    nb_lapins = carte.params.taille_lapin[
        carte.params.taille.get()]  # Nombre de lapins en fonction de la taille du terrain
    nb_loups = carte.params.taille_loup[
        carte.params.taille.get()]  # Nombre de loups en fonction de la taille du terrain

    generation(nb_lapins, Lapin)
    generation(nb_loups, Loup)


def generation(nombre, animal):
    """Génération aléatoire d'un certain nombre d'animaux sur le terrain"""
    for i in range(nombre):
        while True:  # Tant que la case aléatoire generee est occupée
            x_aleatoire = randint(0, carte.params.largeur - 1)  # Générer une coordonnée
            y_aleatoire = randint(0, carte.params.hauteur - 1)
            if (x_aleatoire, y_aleatoire) not in carte.animal:
                carte.place_animal(animal(), x_aleatoire, y_aleatoire)
                break


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
