from turtle import *


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


# Exercice 9
def koch(n):
    if n == 0:
        forward(30)
        return
    koch(n - 1)
    left(60)
    koch(n - 1)
    right(120)
    koch(n - 1)
    left(60)
    koch(n - 1)
