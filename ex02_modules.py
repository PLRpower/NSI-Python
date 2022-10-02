# ----- Imports -----
from tkinter import *
import requests
from PIL import Image


# ----- Exercice 1 -----
default_image = Image.open('data/in/tiger.jpg')  # Charger l'image par défaut du tigre

image1 = default_image.rotate(180)
image1.save('data/out/image1.jpg')
image1.close()  # Tourner l'image à 180 degrès, l'enregistrer et la fermer

r, g, b = default_image.split()
image2 = Image.merge("RGB", (g, r, b))
image2.save('data/out/image2.jpg')
image2.close()  # Inverser les valeurs de couleur de l'image, l'enregistrer et la fermer


# ----- Exercice 2 -----
fenetre = Tk()  # Création de la fenêtre
fenetre.title("Ma p'tite fenêtre")  # Définir un titre à la fenêtre
fenetre.geometry("400x400")  # Définir la taille de la fenêtre
fenetre.resizable(False, False)  # Bloquer le redimensionnement de la fenêtre
Button(text="Fermer la page", command=fenetre.destroy).pack()  # Ajout d'un bouton, qui permet de fermer la fenêtre

fenetre.mainloop() # Permet de lancer la fenêtre


# ----- Exercice 3 -----
data_people = requests.get("http://api.open-notify.org/astros.json").json()  # Permet des récupérer les astronautes via l'api externe
number = data_people['number']  # Récupérer le nombre de personnes dans l'iss
print("Nombre de personnes dans l'iss : " + str(number))
for i in range(number):
    print(data_people['people'][i]['name'] + "se trouve dans : " + data_people['people'][i]['craft'])

data_position = requests.get("http://api.open-notify.org/iss-now.json").json()  # Permet de récupérer la position de l'iss via l'api externe
print("Longitude de l'iss : " + data_position['iss_position']['longitude'])
print("Latitude de l'iss : " + data_position['iss_position']['latitude'])


# ----- Exercice 4 -----
def population(nom):
    # Permet de récupérer le nombre d'habitants d'une ville donnée via l'api externe
    data_commune = requests.get("https://geo.api.gouv.fr/communes?nom=" + str(nom) + "&fields=population").json()
    nombre_hab = data_commune[0]['population']
    print("Nombre d'habitants à " + str(nom) + " : " + str(nombre_hab))


population("Strasbourg")
