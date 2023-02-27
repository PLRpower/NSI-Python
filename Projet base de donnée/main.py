import datetime
import sqlite3

from prettytable import PrettyTable


def main():
    num_etu = None
    stop = False
    while not stop:
        print("", "---------", "Connexion", "---------", sep="\n")
        num_etu = input("Saisissez votre numéro d'étudiant : ")
        connexion, curseur = ouvrir_connexion()
        curseur.execute("SELECT nom, prenom FROM Eleve WHERE num_etu LIKE ?", (num_etu,))
        etudiant = curseur.fetchone()
        fermer_connexion(connexion)
        if etudiant is None:
            print("Numéro d'étudiant introuvable, veuillez réessayez.")
        else:
            print("Bienvenue dans le centre de documentation et d'information " + str(etudiant[0]) + " " + str(
                etudiant[1]) + " !")
            stop = True
    stop = False
    while not stop:
        print("", "----", "Menu", "----",
              "(d) rechercher un document",
              "(e) emprunter",
              "(r) rendre",
              "(a) ajouter",
              "(s) supprimer",
              "(p) rechercher un prêt",
              "(q) quitter", sep="\n")
        choix = input("Que souhaitez vous faire ? ")
        match choix:
            case "d":
                print("\n--------------------\nRecherche de livre\n--------------------")
                livre = rechercher_livre()
                connexion, curseur = ouvrir_connexion()
                curseur.execute("SELECT date_ret FROM Emprunt WHERE isbn LIKE ?", (livre[3],))
                emprunt = curseur.fetchone()
                fermer_connexion(connexion)

                print("\nLe livre intitulé '" + str(livre[0]) + "' de " + str(livre[1]) + ", qui a été publié en "
                      + str(livre[2]) + " sous l'ISBN " + str(livre[3]) +
                      " à été découvert dans le centre de documentation et d'information.")
                if emprunt is None:
                    print("Il n'est actuellement pas emprunté.")
                else:
                    print("Il est actuellement emprunté jusqu'au " + emprunt[0])
                input("\nRetourner au menu (entrée) >")
            case "e":
                print("\n-------\nEmprunt\n-------")
                livre = rechercher_livre()
                date = (datetime.date.today() + datetime.timedelta(weeks=3)).strftime('%Y-%m-%d')
                connexion, curseur = ouvrir_connexion()
                curseur.execute("SELECT date_ret FROM Emprunt WHERE isbn LIKE ?", (livre[3],))
                emprunt = curseur.fetchone()
                if emprunt is None:
                    curseur.execute("INSERT INTO Emprunt VALUES (?, ?, ?)", (livre[3], num_etu, date))
                else:
                    print("Ce livre est déjà emprunté (jusqu'au " + emprunt[0] + ").")
                fermer_connexion(connexion)
                input("\nRetourner au menu (entrée) >")
            case "r":
                pass
            case "a":
                pass
            case "s":
                pass
            case "p":
                pass
            case "q":
                stop = True
            case _:
                print("Je n'ai pas compris...")
    print("\nSortie du programme. Au revoir !")


def rechercher_livre():
    titre = "%" + input("Titre : ") + "%"
    auteur = "%" + input("Auteur.e : ") + "%"
    annee = "%" + input("Année : ") + "%"
    isbn = "%" + input("ISBN : ") + "%"

    connexion, curseur = ouvrir_connexion()
    curseur.execute("SELECT titre, nom, annee, isbn FROM Livre "
                    "JOIN Ecrire USING(isbn)"
                    "JOIN Auteur USING(a_id)"
                    "WHERE titre LIKE ? AND nom LIKE ? AND annee LIKE ? AND isbn LIKE ?",
                    (titre, auteur, annee, isbn))
    resultats = curseur.fetchall()
    fermer_connexion(connexion)

    # S'il existe plusieurs livres avec les champs recherchés
    nombre_resultats = len(resultats)
    if nombre_resultats > 1:
        table = PrettyTable()
        table.field_names = ["#", "Titre", "Auteur.e", "Année", "ISBN"]
        for i, rows in enumerate(resultats):
            table.add_rows([[i + 1] + list(rows)])
        print("\n", table, "\nPlusieurs livres ont étés trouvés avec vos paramètres de recherche.")
        stop1 = False
        while not stop1:
            choix = input("Préciser le livre recherché avec son numéro : ")
            try:
                nombre = int(choix)
                if 0 <= nombre <= nombre_resultats:
                    stop1 = True
                    return resultats[nombre - 1]
                print("\nVeuillez saisir un numéro compris entre 1 et " + str(nombre_resultats))
            except ValueError:
                print("\nVeuillez saisir un numéro correct.")
    elif nombre_resultats == 1:
        return resultats[0]
    else:
        print("\nAucun livre n'a été trouvé avec vos paramètres de recherche, veuillez réessayer.")
        return rechercher_livre()


def ouvrir_connexion():
    connexion = sqlite3.connect('cdi.db')
    return connexion, connexion.cursor()


def fermer_connexion(connexion):
    connexion.close()


main()
