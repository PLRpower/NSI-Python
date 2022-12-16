from PIL import Image


def echange_circulaire(pix, x, y, t):
    n = t // 2
    for i in range(x, x + n):
        for j in range(y, y + n):
            tmp = pix[i, j]
            pix[i, j] = pix[i, j + n]
            pix[i, j + n] = pix[i + n, j + n]
            pix[i + n, j + n] = pix[i + n, j]
            pix[i + n, j] = tmp


def rotation_rec(pix, x, y, t):
    if t <= 1:
        return

    echange_circulaire(pix, x, y, t)

    n = t // 2
    rotation_rec(pix, x, y, n)
    rotation_rec(pix, x + n, y, n)
    rotation_rec(pix, x, y + n, n)
    rotation_rec(pix, x + n, y + n, n)


def rotation(pix):
    rotation_rec(pix, 0, 0, largeur)
    save("arrow_rotation.png")


def save(name):
    img.save("data/out/" + name)


img = Image.open("data/in/arrow.png")
largeur, hauteur = img.size
px = img.load()


# rotation(px)


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
    if g > d:
        return tab[d]

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


def fusion_2(L1, L2):
    n1 = len(L1)
    n2 = len(L2)
    L12 = [0] * (n1 + n2)
    i1 = 0
    i2 = 0
    i = 0
    while i1 < n1 and i2 < n2:
        if L1[i1] < L2[i2]:
            L12[i] = L1[i1]
            i1 += 1
        else:
            L12[i] = L2[i2]
            i2 += 1
        i += 1
    while i1 < n1:
        L12[i] = L1[i1]
        i1 += 1
        i += 1
    while i2 < n2:
        L12[i] = L2[i2]
        i2 += 1
        i += 1
    return L12


def chercher(T, n, i, j):
    if i < 0 or j > len(T) - 1:
        print("Erreur")
        return None
    if i > j:
        return None
    m = (i + j) // 2
    if T[m] < n:
        return chercher(T, n, m, j)
    elif T[m] > n:
        return chercher(T, n, i, m)
    else:
        return m


assert (chercher([1, 5, 6, 6, 9, 12], 9, 0, 5) == 4)


class Cellule:
    def __init__(self, murNord, murEst, murSud, murOuest):
        self.murs = {'N': murNord, 'E': murEst, 'S': murSud, 'O': murOuest}


cellule = Cellule(True, False, True, True)


class Labyrinthe:
    def __init__(self, hauteur, longueur):
        self.grille = self.construire_grille(hauteur, longueur)

    def construire_grille(self, hauteur, longueur):
        grille = []
        for i in range(hauteur):
            ligne = []
            for j in range(longueur):
                cellule = Cellule(True, True, True, True)
                ligne.append(cellule)
            grille.append(ligne)
        return grille

    def creer_passage(self, c1_lig, c1_col, c2_lig, c2_col):
        cellule1 = self.grille[c1_lig][c1_col]
        cellule2 = self.grille[c2_lig][c2_col]
        # cellule 2 au Nord de cellule1
        if c1_lig - c2_lig == 1 and c1_col == c2_col:
            cellule1.murs['N'] = False
            cellule2.murs['S'] = False
        # cellule2 à l’Ouest de cellule1
        elif c1_lig == c2_lig and c1_col - c2_col == 1:
            cellule1.murs['O'] = False
            cellule2.murs['E'] = False

    def creer_labyrinthe(self, ligne, colonne, haut, long):
        if haut == 1:  # Cas de base
            for k in range(long):
                self.creer_passage(ligne, k, ligne, k + 1)
        elif long == 1:  # Cas de base
            for k in range(haut):
                self.creer_passage(k, colonne, k + 1, colonne)
        # Suite ...


def tri_fusion2(L):
    n = len(L)
    if n <= 1:
        return L
    print(L)
    mg = moitie_gauche(L)
    md = moitie_droite(L)
    L1 = tri_fusion2(mg)
    L2 = tri_fusion2(md)
    return fusion2(L1, L2)


def moitie_droite(L):
    milieu = len(L) // 2
    return L[:milieu]


def moitie_gauche(L):
    milieu = len(L) // 2
    return L[milieu:]


def fusion2(L1, L2):
    L = []
    n1 = len(L1)
    n2 = len(L2)
    i1 = 0
    i2 = 0
    while i1 < n1 or i2 < n2:
        e1 = L1[i1]
        e2 = L2[i2]
        if i1 >= n1:
            L.append(e2)
            i2 += 1
        elif i2 >= n2:
            L.append(e1)
            i1 += 1
        else:
            if e1 > e2:
                L.append(e2)
                i1 += 1
            else:
                L.append(e1)
                i2 += 1
    return L
