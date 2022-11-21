class Cellule:
    """Une cellule d’une liste chaînée"""

    def __init__(self, v, s):
        self.valeur = v
        self.suivante = s


class Pile:
    """Structure de pile"""

    def __init__(self):
        self.contenu = None
        self._taille = 0

    def est_vide(self):
        return self.contenu is None

    def empiler(self, e):
        self.contenu = Cellule(e, self.contenu)
        self._taille += 1

    def depiler(self):
        if self.est_vide():
            raise IndexError('dépiler sur une pile vide')
        else:
            self._taille -= 1
            v = self.contenu.valeur
            self.contenu = self.contenu.suivante
            return v

    def consulter(self):
        if self.est_vide():
            raise IndexError('consulter sur une pile vide')
        else:
            return self.contenu.valeur

    def vider(self):
        self.contenu = None

    def taille(self):
        return self._taille


# Exercice 2
def calcP(expr):
    pile = Pile()
    for element in expr.split(" "):

        if element == "+":  # Si l'élément est un '+'
            premier = pile.depiler()
            deuxieme = pile.depiler()
            pile.empiler(premier + deuxieme)

        elif element == "*":  # Si l'élément est un '*'
            premier = pile.depiler()
            deuxieme = pile.depiler()
            pile.empiler(premier * deuxieme)

        else:
            try:  # Si l'élément est un nombre
                pile.empiler(float(element))
            except SyntaxError:  # Si l'élément n'est ni un nombre, ni un opérateur binaire
                raise SyntaxError("Expression mal formée")

    return pile.consulter()


assert (calcP("1 2 3 * + 4 *") == 28.0)


# Exercice 3
def parentheses(s, f):
    pile = Pile()
    for i, x in enumerate(s):
        if i == f:
            return pile.depiler()
        elif x == "(":
            pile.empiler(i)
        elif x == ")":
            pile.depiler()


# Exercice 4
def parentheses2(expr):
    pile = Pile()
    for i in expr:
        if i == "(":
            pile.empiler(i)
        elif i == ")":
            if pile.est_vide():
                return False
            if pile.consulter() == "(":
                pile.depiler()

    if pile.est_vide():
        return True
    return False


# Exercice 5
def simplifie(pile, ops):
    pile = Pile()
    while not pile.est_vide():
        element = pile.consulter()
        if element == "(":
            pile.empiler(element)

        elif element == ")":
            return  ##

        elif element == "+":
            premier = pile.depiler()
            deuxieme = pile.depiler()
            pile.empiler(premier + deuxieme)

        elif element == "*":
            premier = pile.depiler()
            deuxieme = pile.depiler()
            pile.empiler(premier * deuxieme)

        else:  # Si l'élément est un nombre
            pile.empiler(element)


# Exercice 6
class PileBornee:
    def __init__(self, c):
        self.contenu = None
        self._max = c
        self._taille = 0

    def est_vide(self):
        return self.contenu is None

    def est_pleine(self):
        return self.contenu == self._max

    def empiler(self, e):
        if not self.est_pleine():
            self.contenu = Cellule(e, self.contenu)
            self._taille += 1
        else:
            raise IndexError('empiler sur une pile pleine')

    def depiler(self):
        if self.est_vide():
            raise IndexError('dépiler sur une pile vide')
        else:
            self._taille -= 1
            v = self.contenu.valeur
            self.contenu = self.contenu.suivante
            return v

    def consulter(self):
        if self.est_vide():
            raise IndexError('consulter sur une pile vide')
        else:
            return self.contenu.valeur

    def vider(self):
        self.contenu = None

    def taille(self):
        return self._taille


# Exercice 6
class FileBornee:
    def __init__(self, c):
        self.contenu = None
        self._max = c
        self._taille = 0

    def est_vide(self):
        return self.contenu is None

    def est_pleine(self):
        return self.contenu == self._max

    def empiler(self, e):
        if not self.est_pleine():
            self.contenu = Cellule(e, self.contenu)
            self._taille += 1
        else:
            raise IndexError('empiler sur une pile pleine')

    def depiler(self):
        if self.est_vide():
            raise IndexError('dépiler sur une pile vide')
        else:
            self._taille -= 1
            v = self.contenu.valeur
            self.contenu = self.contenu.suivante
            return v

    def consulter(self):
        if self.est_vide():
            raise IndexError('consulter sur une pile vide')
        else:
            return self.contenu.valeur

    def vider(self):
        self.contenu = None

    def taille(self):
        return self._taille
