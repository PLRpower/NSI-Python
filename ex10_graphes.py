class Graphe:
    def __init__(self, n):
        self.adj = [[0] * n for _ in range(n)]
        self.n = n

    def ajouter_arc(self, s1, s2):
        self.adj[s1][s2] = 1

    def arc(self, s1, s2):
        return self.adj[s1][s2] == 1

    def ordre(self):
        return self.n

    def sommets(self):
        return list(range(self.n))

    def voisins(self, s):
        return [i for i in range(self.n) if self.adj[s][i]]

    def degre(self, s):
        return sum(self.adj[s])

    def liste_adjacence(self):
        liste_adj = {}
        for i in range(self.n):
            liste_adj[i] = [j for j in range(self.n) if self.arc(i, j)]
        return liste_adj

    def matrice_adjacence(self):
        return self.adj
