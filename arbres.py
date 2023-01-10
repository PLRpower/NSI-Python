class Noeud:
    '''un nœud d’un arbre binaire'''

    def __init__(self, v, g, d):
        self.valeur = v
        self.gauche = g
        self.droit = d

    def __eq__(self, autre_arb):  # Le temps d'exécution de l'algorithme est proportionnel à la taille de la donnée
        if autre_arb is None:
            return False
        elif self.valeur != autre_arb.valeur:
            return False
        elif (self.gauche is None) != (autre_arb.gauche is None):
            return False
        elif self.gauche and autre_arb.gauche and self.gauche != autre_arb.gauche:
            return False
        elif (self.droit is None) != (autre_arb.droit is None):
            return False
        elif self.droit and autre_arb.droit and self.droit != autre_arb.droit:
            return False
        return True


def est_feuille(arb):
    return arb is not None and arb.gauche is None and arb.droit is None


def nb_feuilles(arb):
    if arb is None:
        return 0
    elif est_feuille(arb):
        return 1
    return nb_feuilles(arb.gauche) + nb_feuilles(arb.droit)


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
    if arb is None:
        return False
    elif arb.valeur == v:
        return True
    return appartient(arb.gauche, v) or appartient(arb.droit, v)


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
    else:
        arb_gauche = parfait(h - 1)
        arb_droit = parfait(h - 1)
        return Noeud(0, arb_gauche, arb_droit)


arb = Noeud('A', Noeud('B', None, Noeud('C', None, None)), Noeud('D', None, None))

affiche(arb)
