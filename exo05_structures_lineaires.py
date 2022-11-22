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
        return self._taille == self._max

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
        self.tete = None
        self.queue = None
        self._max = c
        self._taille = 0

    def est_vide(self):
        return self.contenu is None

    def est_pleine(self):
        return self._taille == self._max

    def ajouter(self, e):
        if not self.est_pleine():
            c = Cellule(e, self.contenu)
            if self.est_vide():
                self.tete = c
            else:
                self.queue.suivante = c
            self.queue = c
            self._taille += 1
        else:
            raise IndexError('ajouter sur une file pleine')

    def retirer(self):
        if self.est_vide():
            raise IndexError('retirer sur une file vide')
        else:
            self._taille -= 1
            v = self.tete.valeur
            self.tete = self.tete.suivante
            if self.tete is None:
                self.queue = None
            return v


def creer_file(c):
    return FileBornee(c)


def est_vide(p):
    est_vide(p)


def est_pleine(p):
    est_pleine(p)


def ajouter(p, e):
    return p.ajouter(e)


def retirer(p):
    return p.retirer()


def positif(T):
    T2 = list(T)
    T3 = list(T2)
    while T2 != []:
        x = T2.pop()
        if x >= 0:
            T3.append(x)
    T2 = []
    while T3 != []:
        x = T3.pop()
        if x >= 0:
            T2.append(x)
    print("T =", T)
    return T2


class Maillon:
    def __init__(self, v):
        self.valeur = v
        self.suivant = None


class File:
    def __init__(self):
        self.dernier_file = None

    def enfile(self, element):
        nouveau_maillon = Maillon(element)
        nouveau_maillon.suivant = self.dernier_file
        self.dernier_file = element

    def est_vide(self):
        return self.dernier_file is None

    def affiche(self):
        maillon = self.dernier_file
        while maillon is not None:
            print(maillon.valeur)
            maillon =

    def defile(self):
        if not self.est_vide():
            if self.dernier_file.suivant is None:
                resultat = self.dernier_file.valeur
                self.dernier_file = None
                return resultat
            maillon =
            while maillon.suivant.suivant is not None:
                maillon = maillon.suivant
            resultat =
            maillon.suivant = None
            return resultat
        return None
