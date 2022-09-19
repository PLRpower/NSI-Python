# Exercice 1
from tkinter import *
from PIL import Image
import requests


# Ouverture des images
default_image = Image.open('data/in/tiger.jpg')
r, g, b = default_image.split()
image1 = default_image.rotate(180)
image2 = Image.merge("RGB", (g, r, b))
image1.save('data/out/image1.jpg')
image2.save('data/out/image2.jpg')
image1.close()
image2.close()


# Exercice 2
fenetre = Tk()
fenetre.title("Petite fenêtre !")
fenetre.geometry("400x400")
fenetre.resizable(False, False)
button = Button(text="Fermer la page", command=fenetre.destroy)
button.pack()
fenetre.mainloop()


# Exercice 3
data_people = requests.get("http://api.open-notify.org/astros.json").json()
number = data_people['number']
print("Nombre de personnes dans l'iss : " + str(number))
for i in range(number):
    print(data_people['people'][i]['name'] + "se trouve dans : " + data_people['people'][i]['craft'])
data_position = requests.get("http://api.open-notify.org/iss-now.json").json()
print("Longitude de l'iss : " + data_position['iss_position']['longitude'])
print("Latitude de l'iss : " + data_position['iss_position']['latitude'])


# Exercice 4
def population(nom):
    data_commune = requests.get("https://geo.api.gouv.fr/communes?nom=" + str(nom) + "&fields=population").json()
    nombre_hab = data_commune[0]['population']
    print("Nombre d'habitants à " + str(nom) + " : " + str(nombre_hab))


population("Strasbourg")
