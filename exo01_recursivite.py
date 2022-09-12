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
    else:
        return 1 + nombre_de_chiffres(n // 10)


# Exercice 6
def nombre_de_bits(n):
    print(n.bit_count())
