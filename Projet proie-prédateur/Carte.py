from tkinter import *

from PIL import Image, ImageTk


class Carte(Canvas):

    def __init__(self, parent, params, **kwargs):
        """Initialise le terrain (de type Canvas) en le plaçant dans la fenêtre"""
        Canvas.__init__(self, parent, width=params.largeur_pixels, height=params.hauteur_pixels,
                        bg="white", bd=0, **kwargs)

        self.params = params

        self.icons = {}
        # Conservation en mémoire des images représentant les animaux
        # Dictionnaire dont les clés sont les classes des animaux
        # et les valeurs sont les images

        self.herbe = []
        # Tableau à deux dimensions de la taille du terrain
        # contenant des listes de la forme [hauteur d’herbe, représentation]

        self.animal = {}
        # Dictionnaire dont les clés sont les couples (x,y)
        # et les valeurs sont les couples (animal,représentation)

        self.pack()

    def reinit(self):
        """Réinitialise le terrain. À exécuter quand on veut recommencer
        et après avoir modifié la largeur dans les paramètres"""
        self.delete('all')

        t_icone = self.params.taille_case - 2 * self.params.border
        wolf = ImageTk.PhotoImage(Image.open('wolf_38.png').resize((t_icone, t_icone)))
        rabbit = ImageTk.PhotoImage(Image.open('rabbit_38.png').resize((t_icone, t_icone)))
        self.icons = {"loup": wolf, "lapin": rabbit}
        # Conservation en mémoire des images représentant les animaux
        # Dictionnaire dont les clés sont les classes des animaux
        # et les valeurs sont les images

        c, b = self.params.taille_case, self.params.border
        h, l = self.params.hauteur, self.params.largeur

        self.herbe = [[[self.params.niveau_herbe,
                        self.create_rectangle(x * c + b, y * c + b, (x + 1) * c + b, (y + 1) * c + b,
                                              fill=self.couleur(self.params.niveau_herbe),
                                              width=b, outline='gray')]
                       for y in range(h)] for x in range(l)]
        # Tableau à deux dimensions de la taille du terrain
        # contenant des listes de la forme [hauteur d’herbe, représentation]

        self.animal = {}
        # Dictionnaire dont les clés sont les couples (x,y)
        # et les valeurs sont les couples (animal,représentation)

    def couleur(self, value):
        """Retourne la couleur associée à une hauteur d’herbe"""
        return '#60' + hex(round(value * 1.1) + 70)[2:] + '00'

    def faire_pousser_herbe(self):
        """Fait pousser toute l’herbe du terrain"""
        for x in range(self.params.largeur):
            for y in range(self.params.hauteur):
                if self.herbe[x][y][0] < 100:
                    self.herbe[x][y][0] += 1
                    self.itemconfig(self.herbe[x][y][1], fill=self.couleur(self.herbe[x][y][0]))

    def place_animal(self, animal, x, y):
        """Place un animal donné aux coordonnées (x,y) données"""
        assert not (x, y) in self.animal.keys()
        self.animal[(x, y)] = animal, self.create_image(self.coord_to_center(x), self.coord_to_center(y),
                                                        image=self.icons[animal.classe])

    def bouge_animal(self, x0, y0, x, y):
        """Déplace un animal donné par ses coordonnées (x0,y0) aux coordonnées (x,y)"""
        assert not (x, y) in self.animal.keys()
        self.animal[(x, y)] = self.animal.pop((x0, y0))
        self.coords(self.animal[(x, y)][1],
                    self.coord_to_center(x), self.coord_to_center(y))

    def elimine_animal(self, x, y):
        """Supprime un animal du terrain"""
        _, rep = self.animal.pop((x, y))
        self.delete(rep)

    def coupe_herbe(self, x, y):
        """Coupe l’herbe aux coordonnées données et retourne la quantité de nourriture"""
        UN = self.herbe[x][y][0]
        self.herbe[x][y][0] = 0
        self.itemconfig(self.herbe[x][y][1], fill=self.couleur(0))
        return UN

    def coord_to_center(self, x):
        return (2 * x + 1) * self.params.taille_case // 2 + self.params.border
