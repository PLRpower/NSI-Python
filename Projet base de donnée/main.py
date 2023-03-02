import datetime
import sqlite3

from prettytable import PrettyTable


def connexion():
    # Connexion avec l'identifiant d'un étudiant
    print("\n---------\nConnexion\n---------")
    while True:
        num_etu = input("Saisissez votre numéro d'étudiant (copier-coller : 745611421242) : ")
        etudiant = requete("SELECT nom, prenom FROM Eleve WHERE num_etu LIKE ?", [num_etu])
        if etudiant:
            nom, prenom = etudiant[0]
            print("\nBienvenue dans le centre de documentation et d'information", nom, prenom, "!")
            input("Accéder au menu (entrée) >")
            return menu(num_etu)
        print("\nNuméro d'étudiant introuvable, veuillez réessayez.")


def menu(num_etu):
    # Menu
    while True:
        print("\n----", "Menu", "----", "(d) rechercher un livre", "(e) emprunter", "(r) rendre", "(a) ajouter",
              "(s) supprimer", "(p) rechercher un prêt", "(q) quitter", sep="\n")
        choix = input("\nQue souhaitez vous faire ? ")
        match choix:
            case "d":
                rechercher()
            case "e":
                emprunter(num_etu)
            case "r":
                rendre(num_etu)
            case "a":
                ajouter()
            case "s":
                supprimer()
            case "p":
                pass
            case "q":
                break
            case _:
                print("Je n'ai pas compris...")
        input("Retourner au menu (entrée) >")  # Attente de l'utilisateur avant de retourner au menu
    print("\nSortie du programme. Au revoir !")


def rechercher():
    print("\n------------------\nRecherche de livre\n------------------")

    # Procédure de recherche du livre dans la base de données
    titre, auteur, annee, isbn = choix_livre(recherche_livre(), ["Titre", "Auteur.e", "Année", "ISBN"])

    # Récupération de la date de retour de l'emprunt (s'il y en a un)
    emprunt = requete("SELECT date_ret FROM Emprunt WHERE isbn LIKE ?", [isbn])

    # Affichage des informations sur le livre et l'emprunt en cours
    print(
        f"\nLe livre intitulé '{titre}' de {auteur}, qui a été publié en {annee} sous l'ISBN {isbn} a été découvert dans le centre de documentation et d'information.")
    print(
        f"Il est actuellement emprunté jusqu'au {emprunt[0][0]}." if emprunt else "Il n'est actuellement pas emprunté.")


def emprunter(num_etu):
    print("\n-------\nEmprunt\n-------")

    # Procédure de recherche du livre dans la base de données
    titre, auteur, annee, isbn = choix_livre(recherche_livre(), ["Titre", "Auteur.e", "Année", "ISBN"])

    # Récupération de la date de retour de l'emprunt (s'il y en a un)
    emprunt = requete("SELECT date_ret FROM Emprunt WHERE isbn LIKE ?", [isbn])

    if emprunt:  # Si le livre est déjà emprunté
        print(f"\nCe livre est déjà emprunté (jusqu'au {emprunt[0][0]}).")
        return
    date_retour = (datetime.date.today() + datetime.timedelta(weeks=3)).strftime('%Y-%m-%d')
    requete("INSERT INTO Emprunt VALUES (?, ?, ?)", [isbn, num_etu, date_retour])
    print(f"\nVous avez correctement emprunté le livre intitulé '{titre}' de {auteur} jusqu'au {date_retour}")


def rendre(num_etu):
    print("\n--------------\nRendre un livre\n--------------")

    # Récupération des emprunts de l'élève (s'il y en a)
    emprunts = requete("SELECT titre, nom, annee, isbn, date_ret FROM Emprunt "
                       "JOIN Livre USING (isbn)"
                       "JOIN Ecrire USING(isbn) "
                       "JOIN Auteur USING (a_id)"
                       "WHERE num_etu LIKE ?", [num_etu])

    if emprunts:
        # Procédure de recherche du livre emprunté souhaité
        titre, auteur, annee, isbn, date_ret = choix_livre(emprunts,
                                                           ["Titre", "Auteur.e", "Année", "ISBN", "Date retour"])
        requete("DELETE FROM Emprunt WHERE isbn LIKE ?", [isbn])
        print(f"\nLe livre {titre} de {auteur} à correctement été rendu.")
        return
    print("\nCet.te élève.e n'a actuellement aucun emprunt de livre.")


def ajouter():
    print("\n--------\nAjouter\n--------")

    while True:
        print("(a) ajouter un auteur\n(l) ajouter un livre")
        choix = input("\nQue souhaitez vous faire ? ")
        match choix:
            case "a":
                while True:
                    nom = input("\nSaisissez le nom de l'auteur : ")
                    if not nom:
                        print("\nVeuillez saisir le nom de l'auteur.")
                        continue
                    break
                auteur = requete("SELECT nom FROM Auteur WHERE UPPER(nom) = UPPER(?)", [nom])
                if auteur:
                    print(f"\nL'auteur {nom} existe déjà dans la base de donnée du CDI.")
                else:
                    a_id = int(requete("SELECT MAX(a_id) FROM Auteur")[0][0]) + 1
                    requete("INSERT INTO Auteur VALUES (?, ?)", [a_id, nom])
                    print(f"\nL'auteur {nom} à correctement été ajouté à la base de donnée du CDI.")
                break
            case "l":
                while True:
                    isbn = input("Saisissez l'ISBN du livre : ")
                    if not isbn:
                        print("\nVeuillez saisir un ISBN.")
                        continue
                    elif requete("SELECT isbn FROM Livre WHERE isbn = ?", [isbn]):
                        print(f"\nL'ISBN {isbn} est déjà présent dans la base de donnée.")
                        continue
                    break

                while True:
                    siret = input("Saisissez le siret du livre : ")
                    if not siret:
                        print("\nVeuillez saisir un siret.")
                        continue
                    break

                while True:
                    titre = input("Saisissez le titre du livre : ")
                    if not titre:
                        print("\nVeuillez saisir un titre.")
                        continue
                    break

                while True:
                    annee = input("Saisissez l'année de publication du livre : ")
                    if not annee:
                        print("\nVeuillez saisir une année.")
                        continue
                    elif not annee.isdigit():
                        print("\nVeuillez saisir une année correcte.")
                        continue
                    break

                while True:
                    auteur = input("Saisissez l'auteur du livre : ")
                    if not auteur:
                        print("\nVeuillez saisir l'auteur du livre.")
                        continue
                    break

                requete("INSERT INTO Livre VALUES (?, ?, ?, ?)", [isbn, siret, titre, annee])
                a_id = requete("SELECT a_id FROM Auteur WHERE UPPER(nom) = UPPER(?)", [auteur])
                if not a_id:
                    a_id = int(requete("SELECT MAX(a_id) FROM Auteur")[0][0]) + 1
                    requete("INSERT INTO Auteur VALUES (?, ?)", [a_id, auteur])
                    requete("INSERT INTO Ecrire VALUES (?, ?)", [a_id, isbn])
                else:
                    requete("INSERT INTO Ecrire VALUES (?, ?)", [a_id[0][0], isbn])
                print(f"\nLe livre {titre} a correctement été ajouté à la base de donnée du CDI.")
                break
            case _:
                print("Je n'ai pas compris...")


def supprimer():
    print("\n------------\nSupprimer un livre\n------------")
    titre, auteur, annee, isbn = choix_livre(recherche_livre(), ["Titre", "Auteur.e", "Année", "ISBN"])

    requete("DELETE FROM Livre WHERE isbn = ?", [isbn])
    a_id = int(requete("SELECT a_id FROM Auteur")[0][0]) + 1
    requete("DELETE FROM Ecrire WHERE isbn = ? AND a_id = ?", [isbn, a_id])
    livres_auteur = requete("SELECT COUNT(*) FROM Ecrire WHERE isbn = ? AND a_id = ?", [isbn, a_id])[0][0]
    if livres_auteur == 0:
        while True:
            print(
                f"\nLe livre que vous avez supprimé était le dernier livre écrit par {auteur} dans la base de donnée.",
                "\nVoulez vous supprimer l'auteur de la base de donnée ?", "\n(o) oui, le supprimer",
                "\n(n) non, le garder")
            choix = input("\nVotre choix : ")
            match choix:
                case "o":
                    requete("DELETE FROM Auteur WHERE a_id = ?", [a_id])
                    print(f"Le livre {titre}, de {auteur} à correctement été supprimé de la base de donnée.",
                          "Son auteur à également été supprimé de la base de donnée.")
                    break
                case "n":
                    print(f"Le livre {titre} à correctement été supprimé de la base de donnée.")
                    break
                case _:
                    print("Je n'ai pas compris...")


def recherche_livre():
    """
    Procédure de recherche d'un livre (avec le titre, l'auteur, l'année et l'ISBN).
    """
    isbn = input("ISBN (laisser vide pour rechercher avec le titre, l'auteur et l'année) : ")
    titre, auteur, annee = "%%", "%%", "%%"
    if not isbn:
        titre = "%" + input("Titre : ") + "%"
        auteur = "%" + input("Auteur.e : ") + "%"
        annee = "%" + input("Année : ") + "%"
        isbn = "%%"

    resultats = requete("SELECT titre, nom, annee, isbn FROM Livre "
                        "JOIN Ecrire USING(isbn)"
                        "JOIN Auteur USING(a_id)"
                        "WHERE titre LIKE ? AND nom LIKE ? AND annee LIKE ? AND isbn LIKE ?",
                        [titre, auteur, annee, isbn])

    if resultats:
        return resultats
    print("\nAucun livre n'a été trouvé avec vos paramètres de recherche, veuillez réessayer.")
    return recherche_livre()


def choix_livre(resultats, noms_champs):
    """
    Permet de créer un tableau avec les différents résultats trouvés et laisser l'utilisateur choisir le choix final.
    """
    nombre_resultats = len(resultats)
    if nombre_resultats == 1:
        return resultats[0]
    table = PrettyTable()
    table.field_names = ["#"] + noms_champs
    table.add_rows([[i, *rows] for i, rows in enumerate(resultats, start=1)])
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


def requete(sql, arguments=None):
    """
    Execute la requête SQL fournie en ajoutant les arguments fournis et renvoie éventuellement le résultat
    """
    with sqlite3.connect('cdi.db') as connexion:  # Connexion à la base de donnée
        curseur = connexion.cursor()
        if arguments:
            curseur.execute(sql, arguments)  # Exécuter la requête
        else:
            curseur.execute(sql)  # Exécuter la requête
        resultat = curseur.fetchall()  # Récupérer le résultat (si la requête était un SELECT)
        connexion.commit()  # Sauvegarder les changements (pour les INSERT, DELETE, etc ...)
        return resultat  # Renvoyer le résultat (par exemple pour les requêtes SELECT)


connexion()
