import datetime
import sqlite3

from prettytable import PrettyTable


def main():
    # Connexion avec l'identifiant d'un étudiant
    print("\n---------\nConnexion\n---------")
    while True:
        num_etu = input("Saisissez votre numéro d'étudiant : ")
        etudiant = requete("SELECT nom, prenom FROM Eleve WHERE num_etu LIKE ?", (num_etu,))
        if etudiant:
            nom, prenom = etudiant[0]
            print("Bienvenue dans le centre de documentation et d'information", nom, prenom, "!")
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
    titre, auteur, annee, isbn = afficher_resultats(recherche_livre(), ["#", "Titre", "Auteur.e", "Année", "ISBN"])

    # Récupération de la date de retour de l'emprunt (s'il y en a un)
    emprunt = requete("SELECT date_ret FROM Emprunt WHERE isbn LIKE ?", (isbn,))

    # Affichage des informations sur le livre et l'emprunt en cours
    message = "\nLe livre intitulé '{0}' de {1}, qui a été publié en {2} sous l'ISBN {3} a été découvert dans le centre de documentation et d'information."
    if emprunt:
        message += "\nIl est actuellement emprunté jusqu'au {4}."
    else:
        message += "\nIl n'est actuellement pas emprunté."
    print(message.format(titre, auteur, annee, isbn, emprunt[0] if emprunt else ""))

    # Attente de l'utilisateur avant de retourner au menu
    input("\nRetourner au menu (entrée) >")


def emprunter(num_etu):
    print("\n-------\nEmprunt\n-------")

    # Procédure de recherche du livre dans la base de données
    titre, auteur, annee, isbn = afficher_resultats(recherche_livre(), ["#", "Titre", "Auteur.e", "Année", "ISBN"])

    # Récupération de la date de retour de l'emprunt (s'il y en a un)
    emprunt = requete("SELECT date_ret FROM Emprunt WHERE isbn LIKE ?", (isbn,))[0]

    if not emprunt:
        date_retour = (datetime.date.today() + datetime.timedelta(weeks=3)).strftime('%Y-%m-%d')
        requete("INSERT INTO Emprunt VALUES (?, ?, ?)", (isbn, num_etu, date_retour))
        print(f"\nVous avez correctement emprunté le livre intitulé '{titre}' de {auteur} jusqu'au {date_retour}")
    else:
        print(f"\nCe livre est déjà emprunté (jusqu'au {emprunt[0]}).", end="")

    # Attente de l'utilisateur avant de retourner au menu
    input("\nRetourner au menu (entrée) >")


def rendre():
    print("\n--------------\nRendre un livre\n--------------")

    # Saisie du numéro d'étudiant de l'élève
    eleve = input("Saisissez votre numéro d'étudiant : ")

    # Récupération des emprunts de l'élève (s'il y en a)
    emprunts = requete("SELECT titre, nom, annee, isbn, date_ret FROM Emprunt "
                       "JOIN Livre USING (isbn)"
                       "JOIN Ecrire USING(isbn) "
                       "JOIN Auteur USING (a_id)"
                       "WHERE num_etu LIKE ?", (eleve,))

    if emprunts:
        # Procédure de recherche du livre emprunté souhaité
        titre, auteur, annee, isbn, date_ret = afficher_resultats(emprunts, ["#", "Titre", "Auteur.e", "Année", "ISBN",
                                                                             "Date retour"])

        requete("DELETE FROM Emprunt WHERE isbn LIKE ?", (isbn,))
    else:
        print("\nCet.te élève.e n'a actuellement aucun emprunt de livre.")

    # Attente de l'utilisateur avant de retourner au menu
    input("\nRetourner au menu (entrée) >")


def recherche_livre():
    titre = "%" + input("Titre : ") + "%"
    auteur = "%" + input("Auteur.e : ") + "%"
    annee = "%" + input("Année : ") + "%"
    isbn = "%" + input("ISBN : ") + "%"

    resultats = requete("SELECT titre, nom, annee, isbn FROM Livre "
                        "JOIN Ecrire USING(isbn)"
                        "JOIN Auteur USING(a_id)"
                        "WHERE titre LIKE ? AND nom LIKE ? AND annee LIKE ? AND isbn LIKE ?",
                        (titre, auteur, annee, isbn))
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


def requete(sql, arguments):
    connexion = sqlite3.connect('cdi.db')
    curseur = connexion.cursor()
    curseur.execute(sql, arguments)
    resultat = curseur.fetchall()
    connexion.commit()
    connexion.close()
    return resultat


main()
