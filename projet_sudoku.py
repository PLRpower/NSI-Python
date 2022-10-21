# coding: utf-8

#
# Projet Sudoku
#

# Nom des élèves du groupe :

# On veut représenter les valeurs possibles pour chaque case de la grille
# (au début toutes les valeurs de 1 à 9) et mettre ces listes à jour
# automatiquement lorsque l’on fixe la valeur d’une case.

class Grille:
    def __init__(self, grille=None):
        """ Initialise la grille avec le contenu de celle-ci """

        if grille is None:  # S'il n'y a pas de grille définie au départ
            self.tableau = [[[x for x in range(1, 10)] for _ in range(9)] for _ in
                            range(9)]  # Créer un tableau bidirectionnel contenant des listes de 1 à 9.
        else:  # Si la grille est déjà définie au départ
            self.tableau = grille  # Définir le tableau par la grille choisie au départ

    def __getitem__(self, c):
        """ Retourne le chiffre affecté à la case c=(i,j),
        ou bien la liste des chiffres possibles de cette case """

        ligne, colonne = c  # Obtenir la ligne et la colonne de la case choisie.
        return self.tableau[ligne][colonne]  # Renvoyer le contenu de cette case.

    def __setitem__(self, c, v):
        """ Affecte la valeur v à la case c=(i,j)
        et met à jour l‘information sur la grille
        selon les règles du sudoku"""

        ligne, colonne = c  # Obtenir la ligne et la colonne de la case choisie.
        self.tableau[ligne][colonne] = v  # Remplacer le contenu de cette case par le contenu souhaité.

        [self.erase(ligne, x, v) for x in range(9)]  # Supprimer toutes les mêmes valeurs dans la ligne.

        [self.erase(y, colonne, v) for y in range(9)]  # Supprimer toutes les mêmes valeurs dans la colonne.

        box_x = (ligne // 3) * 3
        box_y = (colonne // 3) * 3
        [[self.erase(i, j, v) for i in range(box_x, box_x + 3)] for j in range(box_y, box_y + 3)]
        # Supprimer toutes les mêmes valeurs dans le carré.

    def erase(self, ligne, colonne,
              valeur):  # Fonction permettant de supprimer une valeur choisie dans une case choisie.
        if isinstance(self.tableau[ligne][colonne],
                      list):  # Si la case choisie est une liste (donc numéro non définitif).
            if valeur in self.tableau[ligne][colonne]:  # Si la valeur choisie est dans la liste
                self.tableau[ligne][colonne].remove(valeur)  # Supprimer cette valeur dans la case.


##* Signaler la fin de la partie (perdue ou gagnée) et empêcher d’agir lorsque
##  l’on clique sur une case alors que c’est fini
##* Faire apparaître un bouton lorsque la partie se termine qui propose de recommencer,
##  et recommencer quand on clique dessus (il faudra pour cela définir une fonction init())
##* Permettre de charger une partie à partir d’une liste de valeurs préremplies ;
##  Autrement dit mettre un argument supplémentaire à la fonction __init__
##  de Grille et utiliser cela pour initialiser avec une grille de départ
##* Résolution automatique (quand c’est possible) en cliquant sur un bouton
##* Permettre de revenir en arrière (nécessite de garder un historique de ce qui a été fait)
##* Permettre de jouer sans « tricher », simplement en entrant la valeur au clavier
##  sur une case donnée (choix du mode à choisir en début de partie)
##
## Toute autre idée intéressante est bienvenue

# Eviter le bug qui plante MacOS avec TkInter et Python3 !
import platform
import tkinter.messagebox

if platform.mac_ver()[0] != '' and platform.python_version_tuple()[0] != '2':
    exit('TkInter crashes on this Mac with Python 3. Use Python 2.x')

# Importer la bonne version de TkInter
if (platform.python_version_tuple()[0] == '2'):
    import Tkinter as tk
else:
    import tkinter as tk

_root = tk.Tk()


class Affichage:
    """ Représente l'affichage de la grille de Sudoku """

    # La grille est formée de 9 blocs (pour pouvoir afficher leurs bords).
    # Chaque bloc contient 9 cases.
    # Chaque case affiche soit le nombre choisi,
    # soit les nombres possibles, en découpant la case en 9 sous-cases,
    # soit une erreur (fond rouge)

    def __init__(self):
        # initialiser le tableau de cases contenant l'état de chaque case
        self.cases = [[None for i in range(9)] for j in range(9)]
        # créer les 9 blocs, leurs cases et leurs sous-cases
        [[self.creer_bloc(i, j) for i in range(3)] for j in range(3)]

    def creer_bloc(self, i, j):
        """ Crée une grille de 3x3 blocs et la remplit de cases """
        f = tk.Frame(_root, borderwidth=2, relief='sunken')
        f.grid(row=i, column=j, sticky='nsew')
        for n in range(3):
            for m in range(3):
                self.cases[i * 3 + n][j * 3 + m] = self.creer_case(f, i * 3 + n, j * 3 + m)
        return f

    def creer_case(self, bloc, n, m):
        """ Crée les 9 cases d'un bloc, chacune contenant 9 sous-cases pour les chiffres """
        case = tk.Frame(bloc, borderwidth=2, relief='sunken')
        case.grid(row=n, column=m, sticky='nsew')
        for p in range(3):
            case.columnconfigure(p, minsize=20)
            case.rowconfigure(p, minsize=20)
        chiffres = [None] * 9
        for p in range(3):
            for q in range(3):
                v = p * 3 + q + 1
                ch = chiffres[v - 1] = tk.Label(case, text=str(v), fg='grey')
                ch.grid(row=p, column=q, sticky='nsew')
                # appeler self.click lorsque l'on clique sur une sous-case
                ch.bind("<Button-1>", lambda ev, v=v: self.click(n, m, v))
        # une case est représentée par un dictionnaire avec :
        #   - son état : 'chiffres', 'definitif', 'erreur' (s'il n'y a plus de chiffres possibles)
        #   - le bloc auquel elle appartient
        #   - le widget Tk qui la représente
        #   - la liste des chiffres qu'elle contient (si type == 'chiffres') ou None (si type == 'definitif')
        return {
            'type': 'chiffres',
            'bloc': bloc,
            'case': case,
            'chiffres': chiffres
        }

    def afficher_valeur(self, i, j, v):
        """ Afficher la valeur v dans la case i,j.
            v peut être un tableau de valeurs possibles,
            un chiffre définitif, ou None en cas d'erreur """
        case = self.cases[i][j]
        type = case['type']
        bloc = case['bloc']
        chiffres = case['chiffres']

        if v == None or v == []:
            # pas de valeur : erreur dans la grille
            # détruire les sous-cases et afficher la case en rouge
            if type != 'erreur':
                case['type'] = 'erreur'
                case['case'].destroy
                case['chiffres'] = None
                erreur = case['case'] = tk.Frame(bloc, bg='red', borderwidth=2, relief='sunken')
                erreur.grid(row=i, column=j, sticky='nsew')
                return 'erreur'  # Renvoyer le signal d'une erreur (pour signaler la fin de la partie)
        elif isinstance(v, int):
            # remplacer la grille de chiffres possibles par un chiffre définitif
            if type != 'definitif':
                case['type'] = 'definitif'
                case['case'].destroy
                case['chiffres'] = None
                chiffre = case['case'] = tk.Label(bloc, text=v, font=(None, 30), borderwidth=2, relief='sunken')
                chiffre.grid(row=i, column=j, sticky='nsew')
        else:
            # mettre à jour les chiffres possibles
            # on "efface" les chiffres non possibles en les affichant en blanc
            for ch in range(1, 10):
                if ch in v:
                    chiffres[ch - 1].config(fg='grey')
                else:
                    chiffres[ch - 1].config(fg='white')

    def click(self, i, j, v):
        """ Fonction de rappel lorsque l'on clique sur un chiffre """
        case = self.cases[i][j]
        chiffres = case['chiffres']

        # ne rien faire s'il y a déjà un chiffre définitif
        if chiffres == None:
            return

        # ne rien faire si on a cliqué sur un chiffre blanc, donc non autorisé
        if chiffres:
            color = chiffres[v - 1].cget('fg')
            if color == 'white':
                return

        # affecter le chiffre à la case
        grille[(i, j)] = v

        # mettre à jour la grille
        for i in range(9):
            for j in range(9):
                self.afficher_valeur(i, j, grille[(i, j)])

        self.check_end()

    def check_end(self):
        end = True
        for i in range(9):
            for j in range(9):
                case = self.cases[i][j]
                type = case['type']

                if type != 'definitif':
                    end = False

                if type == 'erreur':
                    answer = tk.messagebox.askretrycancel('Défaite',
                                                          'Voulez-vous rejouer ?')  # Envoyer une alerte, proposant de rejouer.
                    if answer:  # Si il décide de rejouer.
                        grille.__init__()  # Régénérer la grille.
                        self.__init__()  # Régénérer l'affichage.
                        break  # Arrêter les boucles.
                    _root.destroy()  # Fermer la page.
                    break  # Arrêter les boucles.
        if end is True:
            answer = tk.messagebox.askyesno('Victoire',
                                            'Voulez-vous rejouer ?')  # Envoyer une alerte, proposant de rejouer.
            if answer:  # Si il décide de rejouer.
                grille.__init__()  # Régénérer la grille.
                self.__init__()  # Régénérer l'affichage.
            _root.destroy()  # Fermer la page.


# créer la grille
grille = Grille()
# afficher la grille
ecran = Affichage()
# boucle d'interaction
tk.mainloop()
