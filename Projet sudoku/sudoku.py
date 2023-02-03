# Nom des élèves du groupe : Paul THOMAS
import platform
import tkinter.messagebox


class Grid:
    def __init__(self, grid=None):
        if grid is None:
            self.grid = [[[x for x in range(1, 10)] for _ in range(9)] for _ in range(9)]
        else:
            self.grid = grid

    def __getitem__(self, item):
        row, col = item
        return self.grid[row][col]

    def __setitem__(self, key, value):
        row, col = key
        self.grid[row][col] = value

        for x in range(9):
            self.erase(row, x, value)

        for x in range(9):
            self.erase(x, col, value)

        rounded_row = row - row % 3
        rounded_col = col - col % 3
        [[self.erase(i, j, value) for i in range(rounded_row, rounded_row + 3)] for j in
         range(rounded_col, rounded_col + 3)]

    def erase(self, row, col, value):
        if isinstance(self.grid[row][col], list):
            if value in self.grid[row][col]:
                self.grid[row][col].remove(value)


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
        self.cases = [[None for _ in range(9)] for _ in range(9)]
        [[self.create_block(row, col) for row in range(3)] for col in range(3)]
        self.update_grid()
        tk.Button(text='résoudre automatiqument', bg='#50C878', activebackground='#00A36C',
                  command=lambda: solve_sudoku()).grid()
        _tk.title('Sudoku')

    def create_block(self, row, col):
        frame = tk.Frame(_tk, borderwidth=2, relief='sunken')
        frame.grid(row=row, column=col, sticky='nsew')
        for i in range(3):
            for j in range(3):
                self.cases[row * 3 + i][col * 3 + j] = self.create_box(frame, row * 3 + i, col * 3 + j)
        return frame

    def create_box(self, bloc, row, col):
        case = tk.Frame(bloc, borderwidth=2, relief='groove')
        case.grid(row=row, column=col, sticky='nsew')
        for x in range(3):
            case.columnconfigure(x, minsize=20)
            case.rowconfigure(x, minsize=20)
        numbers = [None] * 9
        for i in range(3):
            for j in range(3):
                value = i * 3 + j + 1
                ch = numbers[value - 1] = tk.Label(case, text=str(value), fg='grey')
                ch.grid(row=i, column=j, sticky='nsew')
                # appeler self.click lorsque l'on clique sur une sous-case
                ch.bind("<Button-1>", lambda ev, v=value: self.click_on_number(row, col, v))
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

    def display_value(self, row, col, value):
        case = self.cases[row][col]
        type = case['type']
        bloc = case['bloc']
        numbers = case['numbers']

        if value is None or value == []:
            # pas de valeur : erreur dans la grille
            # détruire les sous-cases et afficher la case en rouge
            if type != 'error':
                case['type'] = 'error'
                case['case'].destroy
                case['numbers'] = None
                error = case['case'] = tk.Frame(bloc, bg='red', borderwidth=2, relief='groove')
                error.grid(row=row, column=col, sticky='nsew')
                return True

        elif isinstance(value, int):
            # remplacer la grille de chiffres possibles par un chiffre définitif
            if type != 'definitif':
                case['type'] = 'definitif'
                case['case'].destroy
                case['numbers'] = None
                number = case['case'] = tk.Label(bloc, text=value, borderwidth=2, relief='groove', font=(None, 30))
                number.grid(row=row, column=col, sticky='nsew')
        else:
            # mettre à jour les chiffres possibles
            # on "efface" les chiffres non possibles en les affichant en blanc
            for ch in range(9):
                if ch + 1 in value:
                    numbers[ch].config(fg='grey')
                else:
                    numbers[ch].config(fg='white')

    def click_on_number(self, row, col, value):
        case = self.cases[row][col]
        numbers = case['numbers']

        # ne rien faire s'il y a déjà un chiffre définitif
        if numbers is None:
            return

        # ne rien faire si on a cliqué sur un chiffre blanc, donc non autorisé
        if numbers:
            color = numbers[value - 1].cget('fg')
            if color == 'white':
                return

        # affecter le chiffre à la case
        grille[row, col] = value

        # mettre à jour la grille
        self.update_grid()

    def update_grid(self):
        for i in range(9):
            for j in range(9):
                if self.display_value(i, j, grille[i, j]):
                    answer = tk.messagebox.askretrycancel('Défaite', 'Voulez-vous rejouer ?')
                    if answer:
                        grille.__init__()
                        self.__init__()
                        break
                    _tk.destroy()
                    break


def solve_sudoku():
    for row in range(9):
        for col in range(9):
            for value in range(1, 10):
                if solve_box(row, col, value):
                    if isinstance(grille.grid[row][col], list):
                        for x in range(9):
                            if isinstance(grille.grid[row][x], list):
                                if len(grille.grid[row][x]) == 1:
                                    return

                        for x in range(9):
                            if isinstance(grille.grid[x][col], list):
                                if len(grille.grid[x][col]) == 1:
                                    return

                        rounded_row = row - row % 3
                        rounded_col = col - col % 3
                        for i in range(3):
                            for j in range(3):
                                if isinstance(grille.grid[i + rounded_row][j + rounded_col], list):
                                    if len(list(grille.grid[i + rounded_row][j + rounded_col])) == 1:
                                        return
                        display.click_on_number(row, col, value)


def solve_box(row, col, value):
    for x in range(9):
        if grille.grid[row][x] == value:
            return False

    for x in range(9):
        if grille.grid[x][col] == value:
            return False

    rounded_row = row - row % 3
    rounded_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if grille.grid[i + rounded_row][j + rounded_col] == value:
                return False
    return True


grille = Grid()
display = Display()
tk.mainloop()
