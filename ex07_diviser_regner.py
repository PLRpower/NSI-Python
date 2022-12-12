from PIL import Image


def echange_circulaire(px, x, y, t):
    n = t // 2
    for i in range(x, x + n):
        for j in range(y, y + n):
            tmp = px[i, j]
            px[i, j] = px[i, j + n]
            px[i, j + n] = px[i + n, j + n]
            px[i + n, j + n] = px[i + n, j]
            px[i + n, j] = tmp


def rotation_rec(px, x, y, t):
    if t <= 1:
        return

    echange_circulaire(px, x, y, t)

    n = t // 2
    rotation_rec(px, x, y, n)
    rotation_rec(px, x + n, y, n)
    rotation_rec(px, x, y + n, n)
    rotation_rec(px, x + n, y + n, n)


def rotation(px):
    rotation_rec(px, 0, 0, largeur)
    save("arrow_rotation.png")


def save(name):
    img.save("data/out/" + name)


img = Image.open("data/in/arrow.png")
largeur, hauteur = img.size
px = img.load()
rotation(px)


def fusion(l1, l2):
    l = []
    i, j = 0, 0

    while i < len(l1) and j < len(l2):
        if l1[i] < l2[j]:
            l.append(l1[i])
            i += 1
        else:
            l.append(l2[j])
            j += 1

    while i < len(l1):
        l.append(l1[i])
        i += 1

    while j < len(l2):
        l.append(l2[j])
        j += 1

    return l


def tri_fusion(l):
    if len(l) <= 1:
        return l
    else:
        milieu = len(l) // 2
        l1 = l[:milieu]
        l2 = l[milieu:]
        return fusion(tri_fusion(l1), tri_fusion(l2))


def somme_max_rec(tab, g, d):
    if g == d:
        return 'test'

    m = (g + d) // 2

    max_gauche = tab[m]
    somme = max_gauche
    for i in range(m - 1, g - 1, -1):
        somme += i
        if somme > max_gauche:
            max_gauche = somme

    max_droite = float('-inf')
    somme = 0
    for i in range(m + 1, d + 1):
        somme += i
        if somme > max_droite:
            max_droite = somme

    max_milieu = max(max_gauche, m, max_droite)

    max_gauche = somme_max_rec(tab, max_gauche, max_milieu)
    max_droite = somme_max_rec(tab, max_milieu, max_droite)

    return max(max_gauche, max_droite, max_milieu)


def somme_max(tab):
    g = 0
    d = len(tab)
    return somme_max_rec(tab, g, d)


somme_max([2, -4, 1, 9, -6, 7, -3])
