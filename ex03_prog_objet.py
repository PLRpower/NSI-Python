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
        self._d = d
        self._g = g
