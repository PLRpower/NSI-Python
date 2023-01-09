class Noeud:
    '''un nœud d’un arbre binaire'''

    def __init__(self, v, g, d):
        self.valeur = v
        self.gauche = g
        self.droit = d


def est_feuille(arb):
    if arb.gauche is None and arb.droit is None:
        return True
    return False


def nb_feuilles(arb):
