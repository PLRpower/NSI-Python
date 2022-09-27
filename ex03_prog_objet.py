from math import pi
from math import sqrt


# Exercice 1
class Point:

    def __init__(self, x, y):
        self._x = x
        self._y = y

    def coordonnees(self):
        return self._x, self._y

    def normes(self):
        return sqrt(self._x ** 2 - self._y ** 2)

    def distance(self, p):
        x1, y1 = self.coordonnees()
        x2, y2 = p.coordonnees()
        v = Point(x2 - x1, y2 - y1)
        return v.normes()

    def __str__(self):
        x, y = self.coordonnees()
        return "(" + str(x) + ";" + str(y) + ")"


# Exercice 2
class Cercle:

    def __init__(self, centre, rayon):
        self._centre = centre
        self._rayon = rayon

    def perimetre(self):
        return pi * self._rayon * 2

    def surface(self):
        return pi * self._rayon ** 2

    def __str__(self):
        return Point.__str__(Point(self._rayon, self._centre))

    def appartient(self, p):
        return True if p.distance(self._centre) == self._rayon else False


# Exercice 3
class Date:

    def __init__(self, jour, mois, annee):
        self._jour = jour
        self._mois = mois
        self._annee = annee

    def mois(self):
        liste = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet",
                 "août", "septembre", "octobre", "novembre", "décembre"]
        return liste[self._mois - 1]

    def __str__(self):
        return str(self._jour) + " " + self.mois() + " " + str(self._annee)

    def __lt__(self, d2):
        jour, mois, annee = d2
        if self._annee < annee:
            return True
        elif self._annee > annee:
            return False
        elif self._mois < mois:
            return True
        elif self._mois > mois:
            return False
        elif self._jour < jour:
            return True
        else:
            return False


# Exercice 4
class Tableau:

    def __init__(self, imin, imax, v):
        self._imin = imin
        self._v = v

        self._tab = []
        for i in range(imin, imax):
            self._tab.append(v)

    def indice_valide(self, i):
        if self._imin <= i <= self._imin + self.__len__():
            raise IndexError(i)

    def __len__(self):
        return len(self._tab)

    def __getitem__(self, item):
        self.indice_valide(item)
        return self._tab[item]

    def __setitem__(self, key, value):
        self.indice_valide(key)
        self._tab[key] = value

    def __str__(self):
        string = ""
        for i in range(self._imin, self._imin + self.__len__()):
            string += str(self._tab[i]) + " "
        return string


# Exercice 5
class TaBiDir:

    def __init__(self, g, d):
        self.g = g
        self.d = d

    def imin(self):
        return - len(self.g)

    def imax(self):
        return len(self.d) - 1

    def append(self, v):
        self.d.append(v)

    def prepend(self, v):
        self.g = self.g.insert(0, v)

    def __getitem__(self, item):
        if self.imin() <= 1 <= self.imax():
            if item >= 0:
                return self.d[item]
            return self.g[item]
        raise IndexError(item)

    def __setitem__(self, key, value):
        if self.imin() <= 1 <= self.imax():
            if key >= 0:
                self.d[key] = value
            self.g[key] = value
        raise IndexError(key)

    def __str__(self):
        return str(self.g + self.d)


t = TaBiDir([1, 2, 3], [5, 6, 7])
print(t)


class Carte:
    """Initialise Couleur (entre 1 à 4), et Valeur (entre 1 à 13)"""

    def __init__(self, c, v):
        self.Couleur = c
        self.Valeur = v

    """Renvoie le nom de la Carte As, 2, ... 10, Valet, Dame, Roi"""

    def getNom(self):
        if (self.Valeur > 1 and self.Valeur < 11):
            return str(self.Valeur)
        elif self.Valeur == 11:
            return "Valet"
        elif self.Valeur == 12:
            return "Dame"
        elif self.Valeur == 13:
            return "Roi"
        else:
            return "As"

    """Renvoie la couleur de la Carte (pique, coeur, carreau, trefle)"""

    def getCouleur(self):
        return ['pique', 'coeur', 'carreau', 'trefle'][self.Couleur - 1]


class PaquetDeCarte:

    def __init__(self):
        self.contenu = []

    """Remplit le paquet de cartes"""
    # def remplir(self):
    # A compléter

    """Renvoie la Carte qui se trouve à la position donnée"""
    # def getCarteAt(self, pos):
    # A compléter
