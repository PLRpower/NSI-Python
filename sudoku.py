# Nom des élèves du groupe : Paul THOMAS

class Grille:
    def __init__(self):
        self.contenu = [[[_p for _p in range(1, 10)] for _i in range(9)] for _j in range(9)]

    def __getitem__(self, item):
        i, j = item
        return self.contenu[i][j]

    def __setitem__(self, key, value):
        i, j = key
        self.contenu[i][j] = [value]
        for a in range(9):
            for b in range(9):
                liste = self.contenu[a][b]
                self[a][b] = liste.remove(value)
                print(liste)


# Signaler la fin de la partie (perdue ou gagnée) et empêcher d’agir lorsque
#  l’on clique sur une case alors que c’est fini
# Faire apparaître un bouton lorsque la partie se termine qui propose de recommencer,
#  et recommencer quand on clique dessus (il faudra pour cela définir une fonction init())
# Permettre de charger une partie à partir d’une liste de valeurs préremplies ;
#  Autrement dit mettre un argument supplémentaire à la fonction __init__
#  de Grille et utiliser cela pour initialiser avec une grille de départ
# Résolution automatique (quand c’est possible) en cliquant sur un bouton
# Permettre de revenir en arrière (nécessite de garder un historique de ce qui a été fait)
# Permettre de jouer sans « tricher », simplement en entrant la valeur au clavier
#  sur une case donnée (choix du mode à choisir en début de partie)

import platform

if platform.mac_ver()[0] != '' and platform.python_version_tuple()[0] != '2':
    exit('TkInter crashes on this Mac with Python 3. Use Python 2.x')

if platform.python_version_tuple()[0] == '2':
    import Tkinter as tk
else:
    import tkinter as tk

_tk = tk.Tk()


class Affichage:
    def __init__(self):
        # initialiser le tableau de cases contenant l'état de chaque case
        self.cases = [[None for _i in range(9)] for _j in range(9)]
        # créer les 9 blocs, leurs cases et leurs sous-cases
        [[self.creer_bloc(i, j) for i in range(3)] for j in range(3)]
        _tk.title('Sudoku')
        tk.mainloop()

    def creer_bloc(self, i, j):
        """ Crée une grille de 3x3 blocs et la remplit de cases """
        frame = tk.Frame(_tk, borderwidth=2, relief='sunken')
        frame.grid(row=i, column=j, sticky='nsew')
        for n in range(3):
            for m in range(3):
                self.cases[i * 3 + n][j * 3 + m] = self.creer_case(frame, i * 3 + n, j * 3 + m)
        return frame

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


# -- programme principal

# créer la grille
grille = Grille()
Affichage()
