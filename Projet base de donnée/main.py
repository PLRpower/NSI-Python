import datetime
import sqlite3

from prettytable import PrettyTable


def main():
    # Connexion avec l'identifiant d'un étudiant
    print("\n---------\nConnexion\n---------")
    while True:
        num_etu = input("Saisissez votre numéro d'étudiant : ")
        connexion, curseur = ouvrir_connexion()
        curseur.execute("SELECT nom, prenom FROM Eleve WHERE num_etu LIKE ?", (num_etu,))
        etudiant = curseur.fetchone()
        connexion.close()
        if etudiant:
            print("Bienvenue dans le centre de documentation et d'information", etudiant[0], etudiant[1], "!")
            break  # Arrêter la boucle While
        print("\nNuméro d'étudiant introuvable, veuillez réessayez.")

    # Menu
    while True:
        print("", "----", "Menu", "----", "(d) rechercher un document", "(e) emprunter", "(r) rendre", "(a) ajouter",
              "(s) supprimer", "(p) rechercher un prêt", "(q) quitter", sep="\n")
        choix = input("Que souhaitez vous faire ? ")
        match choix:
            case "d":
                rechercher()
            case "e":
                emprunter(num_etu)
            case "r":
                rendre()
            case "a":
                pass
            case "s":
                pass
            case "p":
                pass
            case "q":
                break  # Arrêter la boucle While
            case _:
                print("Je n'ai pas compris...")
    print("\nSortie du programme. Au revoir !")


def rechercher():
    print("\n------------------\nRecherche de livre\n------------------")

    # Procédure de recherche du livre dans la base de données
    livre = afficher_resultats(recherche_livre(), ["#", "Titre", "Auteur.e", "Année", "ISBN"])

    # Récupération de la date de retour de l'emprunt (s'il y en a un)
    connexion, curseur = ouvrir_connexion()
    curseur.execute("SELECT date_ret FROM Emprunt WHERE isbn LIKE ?", (livre[3],))
    emprunt = curseur.fetchone()
    connexion.close()

    # Affichage des informations sur le livre et l'emprunt en cours
    message = "\nLe livre intitulé '{0}' de {1}, qui a été publié en {2} sous l'ISBN {3} a été découvert dans le centre de documentation et d'information."
    message += "\nIl n'est actuellement pas emprunté." if not emprunt else "\nIl est actuellement emprunté jusqu'au {4}."
    print(message.format(livre[0], livre[1], livre[2], livre[3], emprunt[0] if emprunt else ""))

    # Attente de l'utilisateur avant de retourner au menu
    input("\nRetourner au menu (entrée) >")


def emprunter(num_etu):
    print("\n-------\nEmprunt\n-------")

    # Procédure de recherche du livre dans la base de données
    livre = afficher_resultats(recherche_livre(), ["#", "Titre", "Auteur.e", "Année", "ISBN"])

    # Récupération de la date de retour de l'emprunt (s'il y en a un)
    connexion, curseur = ouvrir_connexion()
    curseur.execute("SELECT date_ret FROM Emprunt WHERE isbn LIKE ?", (livre[3],))
    emprunt = curseur.fetchone()

    if not emprunt:
        date_retour = (datetime.date.today() + datetime.timedelta(weeks=3)).strftime('%Y-%m-%d')
        curseur.execute("INSERT INTO Emprunt VALUES (?, ?, ?)", (livre[3], num_etu, date_retour))
        connexion.commit()
        print(f"\nVous avez correctement emprunté le livre intitulé '{livre[0]}' de {livre[1]} jusqu'au {date_retour}")
    else:
        print(f"\nCe livre est déjà emprunté (jusqu'au {emprunt[0]}).", end="")
    connexion.close()

    # Attente de l'utilisateur avant de retourner au menu
    input("\nRetourner au menu (entrée) >")


def rendre():
    print("\n--------------\nRendre un livre\n--------------")

    eleve = input("Saisissez votre numéro d'étudiant : ")

    # Récupération des emprunts de l'élève (s'il y en a)
    connexion, curseur = ouvrir_connexion()
    curseur.execute("SELECT titre, nom, annee, isbn, date_ret FROM Emprunt "
                    "JOIN Livre using (isbn)"
                    "JOIN Ecrire using(isbn) "
                    "JOIN Auteur using (a_id)"
                    "WHERE num_etu LIKE ?", (eleve,))
    emprunts = curseur.fetchall()
    connexion.close()

    if emprunts:
        livre = afficher_resultats(emprunts, ["#", "Titre", "Auteur.e", "Année", "ISBN", "Date retour"])
        connexion, curseur = ouvrir_connexion()
        curseur.execute("DELETE FROM Emprunt WHERE isbn LIKE ?", (livre[3],))
        connexion.commit()
        connexion.close()
    else:
        print("\nCet.te élève.e n'a actuellement aucun emprunt de livre.")

    # Attente de l'utilisateur avant de retourner au menu
    input("\nRetourner au menu (entrée) >")


def recherche_livre():
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
    connexion.close()
    if not resultats:
        print("\nAucun livre n'a été trouvé avec vos paramètres de recherche, veuillez réessayer.")
        return recherche_livre()
    return resultats


def afficher_resultats(resultats, noms_champs):
    nombre_resultats = len(resultats)
    if nombre_resultats == 1:
        return resultats[0]
    table = PrettyTable()
    table.field_names = noms_champs
    table.add_rows([[i + 1, *rows] for i, rows in enumerate(resultats)])
    print("\n", table, "\nPlusieurs livres ont étés trouvés avec vos paramètres de recherche.")
    while True:
        choix = input("Préciser le livre recherché avec son numéro indiqué dans la liste : ")
        try:
            nombre = int(choix)
            if 0 <= nombre <= nombre_resultats:
                return resultats[nombre - 1]
            print("\nVeuillez saisir un numéro compris entre 1 et", str(nombre_resultats))
        except ValueError:
            print("\nVeuillez saisir un numéro correct.")


def ouvrir_connexion():
    connexion = sqlite3.connect('cdi.db')
    return connexion, connexion.cursor()


main()
