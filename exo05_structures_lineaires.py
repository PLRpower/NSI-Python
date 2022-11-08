class Cellule:

    def __init__(self, v, s):
        self.valeur = v
        self.suivante = s


# Exercice 5

def occurences(x, lst):
    if lst is None:
        return 0
    elif lst.valeur == x:
        return 1 + occurences(x, lst.suivante)
    else:
        return occurences(x, lst.suivante)


def occurences_while(x, lst):
    count = 0
    while lst:
        if lst[0] == x:
            count += 1
        lst.pop(0)
    return count


# Exercice 6
def trouver(x, lst):
    if lst is None:
        return None
    elif lst.valeur == x:
        return 0
    else:
        etc = trouver(x, lst.suivant)
        if etc is None:
            return None
        else:
            return etc + 1


def trouve_while(x, lst):
####
