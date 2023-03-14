class Graphe7:
    """Un graphe orienté représenté par une matrice d'adjacence,
    où les sommets sont les entiers 0, 1, ..., n-1"""

    def __init__(self, n):
        self.n = n
        self.adj = [[0 for _ in range(n)] for _ in range(n)]

    def ajouter_arc(self, s1, s2):
        self.adj[s1][s2] = 1

    def arc(self, s1, s2):
        return self.adj[s1][s2] == 1

    def ordre(self):
        return self.n

    def sommets(self):
        return [s for s in range(self.ordre())]

    def voisins(self, s):
        return [i for i, x in enumerate(self.adj[s]) if x == 1]

    def degre(self, s):
        return len(self.voisins(s))

    def liste_adjacence(self):
        return {s: self.voisins(s) for s in range(self.n)}

    def matrice_adjacence(self):
        return self.adj


G1 = Graphe7(5)
G1.ajouter_arc(0, 1)
G1.ajouter_arc(0, 2)
G1.ajouter_arc(0, 3)
G1.ajouter_arc(1, 2)
G1.ajouter_arc(1, 4)
G1.ajouter_arc(3, 4)

assert G1.ordre() == 5
assert G1.arc(1, 2)
assert not G1.arc(2, 1)
assert G1.voisins(0) == [1, 2, 3]
assert G1.degre(1) == 2


class Graphe8:
    def __init__(self, n):
        self.adj = {}

    def ajouter_sommet(self, s):
        if s not in self.adj:
            self.adj[s] = []

    def ajouter_arete(self, s1, s2):
        self.adj[s1][s2] = 1
        self.adj[s2][s1] = 1

    def arete(self, s1, s2):
        return self.adj[s1][s2] == 1

    def ordre(self):
        return self.n

    def sommets(self):
        return [s for s in range(self.ordre())]

    def voisins(self, s):
        return [i for i, x in enumerate(self.adj[s]) if x == 1]

    def degre(self, s):
        return len(self.voisins(s))

    def liste_adjacence(self):
        return {s: self.voisins(s) for s in range(self.n)}

    def matrice_adjacence(self):
        return self.adj

    def nb_arcs(self):
        return sum(sum(ligne) for ligne in self.adj) // 2

    def nb_aretes(self):
        return self.nb_arcs()

    def supprimer_arc(self, s1, s2):
        self.adj[s1][s2] = 0
        self.adj[s2][s1] = 0

    def supprimer_arete(self, s1, s2):
        self.supprimer_arc(s1, s2)

    def est_connexe(self):
        if not self.sommets():
            return True

        sommet_depart = self.sommets()[0]
        vus = parcours_profondeur(self, sommet_depart)
        return all(vus)


def parcours_profondeur(graphe, sommet):
    """Parcours en profondeur depuis le sommet"""
    vus = []

    def parcours_rec(graphe, sommet):
        """Utilisation d’une fonction récursive"""
        if sommet not in vus:
            vus.append(sommet)  # préfixe
            for v in graphe.voisins(sommet):
                parcours_rec(graphe, v)

    parcours_rec(graphe, sommet)
    return vus


"""

Exercice 10:

[0, 1, 2, 3]
[1, 0, 3, 2]
[2, 3, 1, 0]
[3, 1, 0, 2]

Exercice 11:

1. True

2. False

3. mystere(g, u, v) permet de vérifier si le sommet v est atteignable
 à partir du sommet u dans le graphe g en utilisant un parcours en profondeur.
"""


# Exercice 13


def parcours_chemin(graphe, vus, org, sommet):
    """Parcours depuis le sommet, en venant de org"""
    if sommet not in vus:
        vus[sommet] = org
    for v in graphe.voisins(sommet):
        parcours_chemin(graphe, vus, sommet, v)


def chemin(graphe, u, v):
    """Un chemin de u à v, le cas échéant, None sinon"""
    vus = {}
    parcours_chemin(graphe, vus, None, u)
    # S’il n’existe pas de chemin
    if v not in vus:
        return None
    # Sinon on construit le chemin
    ch = []
    s = v
    while s != u:
        ch.append(s)
        s = vus[s]
    ch.reverse()
    return ch


# Exercice 14

def parcours_cycle(graphe, couleur, s):
    """Parcours en profondeur depuis le sommet"""
    if couleur[s] == 'gris':
        return True
    if couleur[s] == 'noir':
        return False
    couleur[s] = 'gris'
    for v in graphe.voisins(s):
        if parcours_cycle(graphe, couleur, v):
            return True
    couleur[s] = 'noir'
    return False


def existe_cycle(graphe):
    """Détermine la présence d’un cycle dans le graphe"""
    couleur = {}
    for s in graphe.sommets():
        couleur[s] = 'blanc'
    for s in graphe.sommets():
        if parcours_cycle(graphe, couleur, s):
            return True
    return False


# Exercice 16

class Noeud:
    """Un nœud d’un arbre binaire"""

    def __init__(self, v, g, d):
        self.valeur = v
        self.gauche = g
        self.droit = d
        self.suivante = None


class File:
    """Structure de file"""

    def __init__(self):
        self.tete = None
        self.queue = None

    def est_vide(self):
        return self.tete is None

    def ajouter(self, c):
        if self.est_vide():
            self.tete = c
        else:
            self.queue.suivante = c
        self.queue = c

    def retirer(self):
        if self.est_vide():
            raise IndexError('retirer sur une file vide')
        else:
            v = self.tete
            self.tete = self.tete.suivante
            if self.tete is None:
                self.queue = None
            return v

    def consulter(self):
        if self.est_vide():
            raise IndexError
        else:
            return self.tete


def parcours_largeur(arbre):
    vus = []
    file = File()
    file.ajouter(arbre)
    while not file.est_vide():
        u = file.retirer()
        if u is not None:
            vus.append(u.valeur)
            if u.gauche:
                file.ajouter(u.gauche)
            if u.droit:
                file.ajouter(u.droit)
    return vus


# Exercice 16

def parcours_largeur_ch(arbre, s):
    vus = {}
    vus[s] = None
    file = File()
    file.ajouter(arbre)
    while not file.est_vide():
        u = file.consulter()
        for v in arbre.voisins(u):
            if v not in vus:
                vus[arbre] = u
                file.ajouter(v)
        file.retirer()
    return vus


def chemin2(graphe, u, v):
    """Un chemin de u à v, le cas échéant, None sinon"""
    vus = parcours_largeur_ch(graphe, u)
    if v not in vus:
        return None

    ch = []
    s = v
    while s != u:
        ch.append(s)
        s = vus[s]
    ch.reverse()
    return ch


# Exercice 18

def parcours_distance(graphe, sommet):
    """Dictionnaire des distances entre le sommet et les autres sommets
    accessibles"""
    dist = {sommet: 0}
    file = File()
    file.ajouter(sommet)
    while not file.est_vide():
        u = file.consulter()
        for v in graphe.voisins(u):
            if v not in dist:
                dist[v] = dist[u] + 1
                file.ajouter(v)
        file.retirer()
    return dist


def distance(graphe, u, v):
    """Distance de u à v et None si pas de chemin"""
    dist = parcours_distance(graphe, u)
    if v not in dist:
        return None
    else:
        return dist[v]
