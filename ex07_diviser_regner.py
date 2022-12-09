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
            l.append()
            i =
