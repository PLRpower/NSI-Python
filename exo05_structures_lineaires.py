# Exercice 1
def identique(l1, l2):
    if l1 is None:
        if l2 is None:
            return True
        else:
            return False
    else:
        if l2 is None:
            return False
        else:
            return l1.valeur == l2.valeur and identique(l1.suivante, l2.suivante)


# Exercice 2
def listeN(n):
    l = None
    if n == 0:
        return l
    else:
        for i in range(n, 0, -1):
            l = Cellule(i, l)
        return l


# Exercice 3
def affiche_liste_recursif(lst):
    if lst is None:
        return
    return affiche_liste_recursif(lst)


class Cellule:

    def __init__(self, v, s):
        self.valeur = v
        self.suivante = s


l1 = Cellule(1, Cellule(2, Cellule(3, None)))
l2 = Cellule(1, Cellule(3, None))
