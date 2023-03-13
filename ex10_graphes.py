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

    def __str__(self):
        voisins = [[] for _ in range(self.n)]
        for s in range(self.n):
            for v in self.voisins(s):
                voisins[s].append(str(v))
        resultat = ''
        for s in range(self.n):
            resultat += f"{s} {' '.join(voisins[s])}\n" if voisins[s] else f"{s}\n"
        return resultat

    def est_connexe(self):
        if not self.sommets():
            # Si le graphe est vide, il est connexe par définition
            return True

        # Initialisation du dictionnaire des sommets visités à False
        sommets_visites = {sommet: False for sommet in self.sommets()}

        # On commence par choisir un sommet de départ au hasard
        sommet_depart = self.sommets()[0]

        # On effectue un parcours en profondeur à partir du sommet de départ
        parcours_profondeur(self, sommet_depart, sommets_visites)

        # Si tous les sommets ont été visités, le graphe est connexe
        return all(sommets_visites.values())


def parcours_profondeur(graphe, sommet, sommets_visites):
    sommets_visites[sommet] = True
    for voisin in graphe.voisins(sommet):
        if not sommets_visites[voisin]:
            parcours_profondeur(graphe, voisin, sommets_visites)


# création d'un graphe vide avec 3 sommets
g = Graphe8(3)

# ajout d'un sommet et d'arêtes
g.ajouter_sommet()
g.ajouter_arete(0, 3)
g.ajouter_arete(1, 3)
g.ajouter_arete(2, 3)

# test si une arête existe
assert g.arete(0, 1) == False
assert g.arete(0, 3) == True

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

Exercice 13:

"""


def parcours_chemin(g, vus, org, s):
    """Parcours depuis le sommet s, en venant de org"""
    if s not in vus:
        vus[s] = org
    for v in g.voisins(s):
        if v not in vus:
            parcours_chemin(g, vus, s, v)


def chemin(g, u, v):
    """Un chemin de u a v, le cas échéant, None sinon"""
    vus = {}
    parcours_chemin(g, vus, None, u)
    # s’il n’existe pas de chemin
    if
        return None
    # sinon on construit le chemin
    ch = []
    s = v
    while
        ch.append(s)
    s =
    ch.reverse()
    return ch
