import pytest

from fonctions import deuxieme_max1, deuxieme_max2


class TestMax:

    # Tests pour la fonction version 1
    def test_deuxieme_max1(self):
        assert deuxieme_max1([4, 2, 7, 5, 9, 1, 5, 3]) == 7
        assert deuxieme_max1([3, 3, 1, 2, 1, 1, 2, 1]) == 2
        with pytest.raises(ValueError):
            deuxieme_max1([2])
        with pytest.raises(ValueError):
            deuxieme_max1([])
        with pytest.raises(ValueError):
            deuxieme_max1([1, 1, 1, 1, 1])

    # Tests pour la fonction version 2
    def test_deuxieme_max2(self):
        assert deuxieme_max2([4, 2, 7, 5, 9, 1, 5, 3]) == 7
        assert deuxieme_max2([3, 3, 1, 2, 1, 1, 2, 1]) == 2
        with pytest.raises(ValueError):
            deuxieme_max2([2])
        with pytest.raises(ValueError):
            deuxieme_max2([])
        with pytest.raises(ValueError):
            deuxieme_max2([1, 1, 1, 1, 1])
