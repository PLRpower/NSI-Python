import pytest


# Valeur maximale d'une liste
def valeur_max(liste):
    maxi = liste[0]
    for valeur in liste:
        if valeur > maxi:
            maxi = valeur
    return maxi


# Valeur maximale d'une liste avec une valeur limite
def valeur_max_limite(liste, limite):
    maxi = liste[0]
    for valeur in liste:
        if maxi < valeur < limite:
            maxi = valeur
    return maxi


# Seconde valeur maximale dans une liste version a
def seconde_valeur_max1(liste):
    assert liste is not None and len(liste) >= 2
    maxi = valeur_max(liste)
    second_maxi = valeur_max_limite(liste, maxi)
    return second_maxi


# Deuxième valeur maximale d'une liste version b
def seconde_valeur_max2(liste):
    assert liste is not None and len(liste) >= 2
    maxi = second_maxi = liste[0]
    for valeur in liste[1:]:
        if valeur > maxi:
            second_maxi = maxi
            maxi = valeur
        elif valeur > second_maxi:
            second_maxi = valeur
    return second_maxi


# Deuxième valeur maximale d'une liste version c
def seconde_valeur_max3(liste):
    assert liste is not None and len(liste) >= 2
    return sorted(liste, reverse=True)[1]


class TestModule:
    # Tests pour la fonction version a
    def test_seconde_valeur_max1(self):
        assert seconde_valeur_max1([4, 2, 7, 5, 9, 1, 5, 3]) == 7
        assert seconde_valeur_max1([1, 1, 1, 1, 1, 1, 1, 1]) == 1
        assert seconde_valeur_max1([3, 3, 1, 2, 1, 1, 2, 1]) == 3
        with pytest.raises(AssertionError):
            seconde_valeur_max1([2])
        with pytest.raises(AssertionError):
            seconde_valeur_max1([])

    # Tests pour la fonction version b
    def test_seconde_valeur_max2(self):
        assert seconde_valeur_max2([4, 2, 7, 5, 9, 1, 5, 3]) == 7
        assert seconde_valeur_max2([1, 1, 1, 1, 1, 1, 1, 1]) == 1
        assert seconde_valeur_max2([3, 3, 1, 2, 1, 1, 2, 1]) == 3
        with pytest.raises(AssertionError):
            seconde_valeur_max2([2])
        with pytest.raises(AssertionError):
            seconde_valeur_max2([])

    # Tests pour la fonction version c
    def test_seconde_valeur_max3(self):
        assert seconde_valeur_max3([4, 2, 7, 5, 9, 1, 5, 3]) == 7
        assert seconde_valeur_max3([1, 1, 1, 1, 1, 1, 1, 1]) == 1
        assert seconde_valeur_max3([3, 3, 1, 2, 1, 1, 2, 1]) == 3
        with pytest.raises(AssertionError):
            seconde_valeur_max3([2])
        with pytest.raises(AssertionError):
            seconde_valeur_max3([])
