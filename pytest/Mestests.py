import pytest

from fonctions import maximum as maximum, maximum_inf as maximum_inf, deuxieme_max2 as dm  # , deuxieme_max_bis as dm


class TestMax:
    def test_1(self):
        assert dm([7, 6]) == 6  # deux valeurs a>b
        assert dm([6, 7]) == 6  # deux valeurs a<b
        assert dm([1, 7, 5, 6, 3]) == 6  # cas quelconque
        assert dm([-5, -1, -3, -7]) == -3  # valeurs négatives
        assert dm([8, 5, 2, 7, 1]) == 7  # max premier
        assert dm([5, 2, 7, 1, 8]) == 7  # max dernier
        assert dm([7, 5, 8, 2, 1]) == 7  # deux premiers, max quelconque
        assert dm([7, 2, 3, 8]) == 7  # deux premiers, max dernier
        assert dm([2, 8, 3, 7]) == 7  # deux derniers, max quelconque
        assert dm([8, 2, 3, 7]) == 7  # deux derniers, max premier
        assert dm([7, 74, 2, 3, 74, 3]) == 7  # 2 fois max, deux avant
        assert dm([2, 74, 7, 3, 74, 3]) == 7  # 2 fois max, deux entre
        assert dm([74, 2, 7, 3, 74, 3]) == 7  # 2 fois max, dont un premier, deux entre
        assert dm([74, 2, 74, 3, 7, 3]) == 7  # 2 fois max, deux après

    def test_inf(self):
        assert dm([7, float('-inf')]) == float('-inf')
        assert dm([float('-inf'), 5]) == float('-inf')
        assert dm([7, 7, float('-inf'), 7, float('-inf')]) == float('-inf')

    def test_fails_intermediaires(self):
        with pytest.raises(ValueError):
            maximum([])
        with pytest.raises(ValueError):
            maximum_inf([5, 6, 7, 4], 3)
        with pytest.raises(ValueError):
            maximum_inf([5, 4, 7, 6], 4)
        with pytest.raises(ValueError):
            maximum_inf([5, 5], 5)

    def test_fails_dm_vide(self):
        with pytest.raises(ValueError):
            dm([])

    def test_fails_dm_longueur_1(self):
        with pytest.raises(ValueError):
            dm([5])

    def test_fails_dm_unique(self):
        with pytest.raises(ValueError):
            dm([3, 3, 3])

    def test_fails_types(self):
        with pytest.raises(TypeError):
            dm([5, None, 'as'])
