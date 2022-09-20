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


class Cercle:

    def __init__(self, centre, rayon):
        self._centre = centre
        self._r = rayon

    def perimetre(self):
        return self._r * 2

    def surface(self):
        return pi * self._r * self._r

    def __str__(self):
        return "(" + self._r + ";" + self._centre + ")"


cercle = Cercle((1, 0), 5)
print(cercle.perimetre())
print(cercle.surface())
