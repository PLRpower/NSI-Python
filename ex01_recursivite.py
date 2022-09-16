# Exercice 1
def fact(n):
    if n == 0:
        return 1
    return n * fact(n - 1)


# Exercice 2
def multiplication_russe(x, y):
    if x == 0:
        return 0
    elif x % 2 == 0:
        multiplication_russe((x // 2), (2 * y))
        return
    multiplication_russe((x // 2), (2 * y) + y)


# Exercice 3
def suite(n, a, b):
    if n == 0:
        return a
    elif n == 1:
        return b
    return 3 * suite(n - 1, a, b) + 2 * suite(n - 2, a, b) + 5


# Exercice 4
def recursive_boucle(i, k):
    if i <= k:
        print(i, end=" ")
        recursive_boucle(i + 1, k)


# Exercice 5
def nombre_de_chiffres(n):
    if n < 10:
        return 1
    return 1 + nombre_de_chiffres(n // 10)


# Exercice 7
def appartient(v, t, i):
    if i >= len(t):
        return False
    elif t[i] == v:
        return True
    return appartient(v, t, i + 1)


# Exercice 8
def dichotomie_rec(val, tab, a, b):
    c = (a + b) // 2
    if tab[c] == val:
        return c
    elif a == b:
        return -1


from turtle import *


# Exercice 9
def koch(n, l):
    if n == 0:
        forward(l)
        return
    koch(n - 1, l // 3)
    left(60)
    koch(n - 1, l // 3)
    right(120)
    koch(n - 1, l // 3)
    left(60)
    koch(n - 1, l // 3)


def propager(m, i, j, val):
    propager_rec(m, i, j, val)
    return m


# Exercice 10
def propager_rec(m, i, j, val):
    if m[i][j] == 1:
        m[i][j] = val

        if i + 1 < len(m) and m[i + 1][j] == 1:
            propager(m, i + 1, j, val)

        if not i - 1 < 0 and m[i - 1][j] == 1:
            propager(m, i - 1, j, val)

        if j + 1 < len(m) and m[i][j + 1] == 1:
            propager(m, i, j + 1, val)

        if not j - 1 < 0 and m[i][j - 1] == 1:
            propager(m, i, j - 1, val)


M = [[0, 0, 1, 0], [0, 1, 0, 1], [1, 1, 1, 0], [0, 1, 1, 0]]


# Exercice 11 (1)
def echange(lst, i1, i2):
    v2 = i2
    lst[i2] = lst[i1]
    lst[i1] = lst[v2]


# Exercice 11 (2)
"""
Les valeurs qui peuvent être renvoyés pas l'apel randint(0, 10) sont :
0 1 9 10
"""

# Exercice 11 (3)
"""
a) La fonction melange() se termine toujours car la variable ind tend vers - l'infini,
et est vérifiée avec la condition 'if ind > 0'

b) Pour une liste de longueur n, il y a n appels récursifs de la fonction melange
effectués, sans compter l'appel initial.

c) 
[0, 1, 2, 3, 4]
[0, 1, 4, 3, 2]
[0, 3, 4, 1, 2]
[0, 3, 4, 1, 2]
[3, 0, 4, 1, 2]

d)
"""

from random import *


def melange(lst, ind):
    while ind > 0:
        print(lst)
        j = randint(0, int)
        echange(lst, ind, j)
        ind -= 1
    print(lst)


lst = [v for v in range(5)]
melange(lst, 4)
