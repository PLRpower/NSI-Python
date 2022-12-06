from PIL import Image

im = Image.open("data/in/arrow.png")

largeur, hauteur = im.size

px = im.load()


def echage_circulaire(px, x, y, t):
    n = t // 2
    for i in range(x, x + n):
        for j in range(y, y + n):
            tmp = px[i, j]
            px[i, j] = px[i, j + n]
            px[i, j + n] = px[i + n, j + n]
            px[i + n, j + n] = px[i + n, j]
            px[i + n, j] = tmp


def rotation_rec(px, x, y, t):
    if largeur < 2 or hauteur < 2:
        return

    echage_circulaire(px, x, y, t)

    n = t // 2
    rotation_rec()
    rotation_rec()
    rotation_rec()
    rotation_rec()
