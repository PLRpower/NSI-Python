import pytest


def maxi(l):
    assert (l is None)
    asse
    if l is None or len(l) < 2:
        raise IndexError
    return sorted(l, reverse=True)[1]


def maxi2(liste):
    if not liste or len(liste) < 2:
        raise IndexError
    maxi = liste[0]
    maxi2 = liste[0]
    for i in range(1, len(liste)):
        if liste[i] > maxi:
            maxi2 = maxi
            maxi = liste[i]
        elif i > maxi2:
            maxi2 = liste[i]
    return maxi2


class TestModule:
    def test_maxi(self):
        assert maxi([4, 2, 7, 5, 9, 1, 5, 3]) == 7

    def test_maxi2(self):
        assert maxi2([4, 2, 7, 5, 9, 1, 5, 3]) == 7

    def test_assert_maxi(self):
        with pytest.raises(AssertionError):
            pytest.fact([4, 5, 4])
