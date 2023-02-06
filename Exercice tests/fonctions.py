
# Valeur maximale d'une liste
def maximum(liste):
    if not liste:
        raise ValueError
    maxi = liste[0]
    for valeur in liste:
        if valeur > maxi:
            maxi = valeur
    return maxi


# Valeur maximale d'une liste avec une valeur limite
def maximum_inf(liste, limite):
    maxi = float('-inf')
    for valeur in liste:
        if maxi < valeur < limite:
            maxi = valeur
    if maxi == float('-inf'):
        raise ValueError
    else:
        return maxi


# Seconde valeur maximale dans une liste version 1
def deuxieme_max1(liste):
    if not list or len(liste) < 2:
        raise ValueError
    maxi = maximum(liste)
    second_maxi = maximum_inf(liste, maxi)
    return second_maxi


# Deuxième valeur maximale d'une liste version 2

def deuxieme_max2(liste):
    liste_unique = set(liste)
    if not liste or len(liste) <= 1 or len(liste_unique) == 1:
        raise ValueError
    liste_unique.remove(max(liste_unique))
    second_maxi = max(liste_unique)
    return second_maxi
