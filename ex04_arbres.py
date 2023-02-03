class Noeud:
    """Un nœud d’un arbre binaire"""

    def __init__(self, v, g, d):
        self.valeur = v
        self.gauche = g
        self.droit = d

    def __eq__(self, autre_arb):  # Le temps d'exécution de l'algorithme est proportionnel à la taille de la donnée
        if autre_arb is None:
            return False
        return self.valeur == autre_arb \
               and appartient(self.gauche, autre_arb) \
               and appartient(self.droit, autre_arb)


def est_feuille(arb):
    return arb is not None and arb.gauche is None and arb.droit is None


def nb_feuilles(arb):
    if arb is None:
        if est_feuille(arb):
            return 1
        return nb_feuilles(arb.gauche) + nb_feuilles(arb.droit)
    return 0


def nb_noeud_int(arb):
    if arb is None or est_feuille(arb):
        return 0
    return 1 + nb_noeud_int(arb.gauche) + nb_feuilles(arb.droit)


def parcours_feuilles(arb):
    if arb is not None:
        if est_feuille(arb):
            print(arb.value, end=" ")
            return
        parcours_feuilles(arb.gauche)
        parcours_feuilles(arb.droit)


def appartient(arb, v):
    if arb is not None:
        if arb.valeur == v:
            return True
        elif v < arb.valeur:
            return appartient(arb.gauche, v)
        return appartient(arb.droit, v)
    return False


def affiche(arb):
    if arb is not None:
        print("(", end="")
        affiche(arb.gauche)
        print(arb.valeur, end="")
        affiche(arb.droit)
        print(")", end="")


def parfait(h):
    if h == 0:
        return None
    arb_gauche = parfait(h - 1)
    arb_droit = parfait(h - 1)
    return Noeud(0, arb_gauche, arb_droit)


# Les arbres binaires de recherches sont les arbres n°1 et n°2.

def minimum(arb):  # L'élément le plus petit se trouve toujours complètement à droite
    if arb is not None:
        while arb.gauche is not None:
            arb = arb.gauche
        return arb.valeur
    return None


def maximum(arb):  # L'élément le plus grand se trouve toujours complètement à gauche
    if arb is not None:
        while arb.droit is not None:
            arb = arb.droit
        return arb.valeur
    return None


def ajout(arb, v):
    if arb is None:
        return Noeud(v, None, None)
    elif not appartient(arb, v):
        if v < arb.valeur:
            return Noeud(arb.valeur, ajout(arb.gauche, v), arb.droit)
        return Noeud(arb.valeur, arb.gauche, ajout(arb.droit, v))


def est_ABR(arb):
    if arb is None:
        return True
    if arb.gauche is not None and arb.gauche.valeur > arb.valeur:
        return False
    if arb.droit is not None and arb.droit.valeur < arb.valeur:
        return False
    return est_ABR(arb.gauche) and est_ABR(arb.droit)


def remplir(arb, tbl):
    if arb is not None:
        remplir(arb.gauche, tbl)
        tbl.append(arb.valeur)
        remplir(arb.droit, tbl)


class ABR:
    """un arbre binaire de recherche"""

    def __init__(self):
        self.racine = None

    def ajouter(self, v):
        self.racine = ajout(self.racine, v)

    def contient(self, v):
        return appartient(self.racine, v)

    def lister(self):
        return remplir(self.racine, [])


def trier(tbl):
    a = ABR()
    for x in tbl:
        a.ajouter(x)
    return a.lister()


def taille(arb, lettre):
    if lettre != '':
        return 1 + taille(arb, arb[lettre][0] + taille(arb, arb[lettre][1]))
    return 0


a = {'F': ['B', 'G'], 'B': ['A', 'D'], 'A': ['', ''], 'D': ['C', 'E'],
     'C': ['', ''], 'E': ['', ''], 'G': ['', 'I'], 'I': ['', 'H'], 'H': ['', '']}

assert (taille(a, 'F') == 9)


def nb_sup(v, abr):
    if abr is not None:
        if abr.valeur > v:
            return 1 + nb_sup(v, abr.gauche) + nb_sup(v, abr.droit)
        elif abr.valeur < v:
            return nb_sup(v, abr.droit)
        return 1 + nb_sup(v, abr.droit)
    return 0
