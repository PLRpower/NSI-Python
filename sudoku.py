# Nom des élèves du groupe : Paul THOMAS
import tkinter.messagebox
import platform


class Grid:
    def __init__(self):
        self.table = [[[_p for _p in range(1, 10)] for _i in range(9)] for _j in range(9)]

    def __getitem__(self, item):
        i, j = item
        return self.table[i][j]

    def __setitem__(self, key, value):
        i, j = key
        self.table[i][j] = value
        rounded_value_i = i - (i % 3)
        rounded_value_j = j - (j % 3)
        [[self.erase(p, q, value) for p in range(rounded_value_i, rounded_value_i + 3)] for q in
         range(rounded_value_j, rounded_value_j + 3)]

        for p in range(9):
            self.erase(i, p, value)
            self.erase(p, j, value)

    def erase(self, i, j, value):
        if isinstance(self.table[i][j], list):
            if value in self.table[i][j]:
                self.table[i][j].remove(value)


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

if platform.mac_ver()[0] != '' and platform.python_version_tuple()[0] != '2':
    exit('TkInter crashes on this Mac with Python 3. Use Python 2.x')
if platform.python_version_tuple()[0] == '2':
    import Tkinter as tk
else:
    import tkinter as tk

_tk = tk.Tk()


class Display:

    def __init__(self):
        self.cases = [[None for _i in range(9)] for _j in range(9)]
        [[self.create_block(i, j) for i in range(3)] for j in range(3)]
        tk.mainloop()

    def create_block(self, i, j):
        f = tk.Frame(_tk, borderwidth=2, relief='sunken')
        f.grid(row=i, column=j, sticky='nsew')
        for n in range(3):
            for m in range(3):
                self.cases[i * 3 + n][j * 3 + m] = self.create_box(f, i * 3 + n, j * 3 + m)
        return f

    def create_box(self, bloc, n, m):
        case = tk.Frame(bloc, borderwidth=2, relief='groove')
        case.grid(row=n, column=m, sticky='nsew')
        for p in range(3):
            case.columnconfigure(p, minsize=20)
            case.rowconfigure(p, minsize=20)
        numbers = [None] * 9
        for p in range(3):
            for q in range(3):
                v = p * 3 + q + 1
                ch = numbers[v - 1] = tk.Label(case, text=str(v), fg='grey')
                ch.grid(row=p, column=q, sticky='nsew')
                # appeler self.click lorsque l'on clique sur une sous-case
                ch.bind("<Button-1>", lambda ev, v=v: self.click_on_number(n, m, v))
        # une case est représentée par un dictionnaire avec :
        #   - son état : 'chiffres', 'definitif', 'erreur' (s'il n'y a plus de chiffres possibles)
        #   - le bloc auquel elle appartient
        #   - le widget Tk qui la représente
        #   - la liste des chiffres qu'elle contient (si type == 'chiffres') ou None (si type == 'definitif')
        return {
            'type': 'numbers',
            'bloc': bloc,
            'case': case,
            'numbers': numbers
        }

    def display_value(self, i, j, v):
        case = self.cases[i][j]
        type = case['type']
        bloc = case['bloc']
        numbers = case['numbers']

        if v is None or v == []:
            # pas de valeur : erreur dans la grille
            # détruire les sous-cases et afficher la case en rouge
            if type != 'error':
                case['type'] = 'error'
                case['case'].destroy
                case['numbers'] = None
                error = case['case'] = tk.Frame(bloc, bg='red', borderwidth=2, relief='sunken')
                error.grid(row=i, column=j, sticky='nsew')
                tkinter.messagebox.askretrycancel(title='Défaite', message='Vous avez perdu ! Voulez-vous rejouer ?')
        elif isinstance(v, int):
            # remplacer la grille de chiffres possibles par un chiffre définitif
            if type != 'definitif':
                case['type'] = 'definitif'
                case['case'].destroy
                case['numbers'] = None
                number = case['case'] = tk.Label(bloc, text=v, font=(None, 30), borderwidth=2, relief='sunken')
                number.grid(row=i, column=j, sticky='nsew')
        else:
            # mettre à jour les chiffres possibles
            # on "efface" les chiffres non possibles en les affichant en blanc
            for ch in range(9):
                if ch + 1 in v:
                    numbers[ch].config(fg='grey')
                else:
                    numbers[ch].config(fg='white')

    def click_on_number(self, i, j, v):
        case = self.cases[i][j]
        numbers = case['numbers']

        # ne rien faire s'il y a déjà un chiffre définitif
        if numbers is None:
            return

        # ne rien faire si on a cliqué sur un chiffre blanc, donc non autorisé
        if numbers:
            color = numbers[v - 1].cget('fg')
            if color == 'white':
                return

        # affecter le chiffre à la case
        grid[i, j] = v

        # mettre à jour la grille
        for i in range(9):
            for j in range(9):
                self.display_value(i, j, grid[i, j])


grid = Grid()
display = Display()
