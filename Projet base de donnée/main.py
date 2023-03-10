import datetime
import sqlite3

import prettytable


def login():
    """
    Procédure de connexion avec l'identifiant du numéro de l'élève
    """
    print("\n---------\nConnexion\n---------")
    while True:  # Tant que l'utilisateur n'a pas fait de choix
        print("\n----\nMenu\n----\n(e) se connecter en élève\n(a) se connecter en admin")
        choix = input("\nQue souhaitez vous faire ? ")

        while True:  # Tant que l'utilisateur n'est pas connecté

            num_etu = input("Saisissez votre numéro d'étudiant (copier-coller : 745611421242) : ")

            try:
                # Recherche du numéro d'étudiant
                nom, prenom = requete("SELECT nom, prenom FROM Eleve WHERE num_etu = ?", [num_etu])[0]
                print("\nBienvenue dans le centre de documentation et d'information", nom, prenom, "!")

                # Attente de l'utilisateur avant d'accéder au menu
                input("Accéder au menu (entrée) >")

                # Arrêter la boucle et continuer sur le menu
                return menu(num_etu)

            except IndexError:  # Si le numéro d'étudiant n'a pas été trouvé (erreur d'index car [0] sur une liste vide)
                print("\nNuméro d'étudiant introuvable, veuillez réessayez.")


def menu(num_etu):
    """
    Navigation dans les options possibles via un menu
    """
    while True:  # Tant que l'utilisateur n'a pas fait de choix

        print(
            "\n----\nMenu\n----\n(d) rechercher un livre\n(e) emprunter\n(r) rendre\n(a) ajouter\n(s) supprimer\n(p) rechercher un prêt\n(q) quitter")
        choix = input("\nQue souhaitez vous faire ? ")

        match choix:
            case "d":
                rechercher_livre()  # Procédure de recherche de livre
            case "e":
                emprunter(num_etu)  # Procédure d'emprunt
            case "r":
                rendre(num_etu)  # Procédure de rendu de livre
            case "a":
                while True:  # Tant que l'utilisateur n'a pas choisi une des deux options
                    print("\n(a) ajouter un auteur\n(l) ajouter un livre")
                    choix = input("\nQue souhaitez vous faire ? ")

                    if choix == "a":
                        ajouter_auteur()  # Procédure d'ajout d'auteur
                    elif choix == "l":
                        ajouter_livre()  # Procédure d'ajout de livre
                    else:
                        print("Choix inconnu, veuillez réessayez.")
                        continue
                    break
            case "s":
                supprimer()  # Procédure de suppression de livre
            case "p":
                rechercher_emprunt(num_etu)  # Procédure de recherche d'emprunt
            case "q":
                break  # Quitter la boucle (et donc fermer le programme)
            case _:  # Si le choix ne correspond à aucune des propositions
                print("Choix inconnu, veuillez réessayez.")

        input("Retourner au menu (entrée) >")  # Attente de l'utilisateur avant de retourner au menu

    print("\nSortie du programme. Au revoir !")


def rechercher_livre():
    """
    Procédure de recherche de livre et d'affichage de ses informations
    """
    print("\n------------------\nRechercher un livre\n------------------")

    # Recherche de livre (via l'ISBN, ou le titre, l'auteur et l'année), et potentiel choix s'il y a plusieurs résultats
    titre, auteur, annee, isbn = recherche_livre()

    # Récupération de la date de retour de l'emprunt (s'il y en a un)
    emprunt = requete("SELECT date_ret FROM Emprunt WHERE isbn = ?", [isbn])

    print(
        f"\nLe livre intitulé '{titre}' de {auteur}, qui a été publié en {annee} sous l'ISBN {isbn} a été découvert dans le centre de documentation et d'information.")
    print(
        f"Il est actuellement emprunté jusqu'au {emprunt[0][0]}." if emprunt else "Il n'est actuellement pas emprunté.")


def emprunter(num_etu):
    """
    Procédure d'emprunt d'un livre
    """
    print("\n-------\nEmprunter un livre\n-------")

    # Recherche de livre (via l'ISBN, ou le titre, l'auteur et l'année), et potentiel choix s'il y a plusieurs résultats
    titre, auteur, annee, isbn = recherche_livre()

    try:
        # Obtenir la date en format DATETIME du jour actuel + 3 semaines (durée de l'emprunt)
        date_retour = (datetime.date.today() + datetime.timedelta(weeks=3)).strftime('%Y-%m-%d')

        # Ajoute d'un emprunt avec le numéro de l'étudiant
        requete("INSERT INTO Emprunt VALUES (?, ?, ?)", [isbn, num_etu, date_retour])

        print(f"\nVous avez correctement emprunté le livre intitulé '{titre}' de {auteur} jusqu'au {date_retour}")

    except sqlite3.Error:  # Si la requête INSERT a échoué
        print(f"\nCe livre est déjà emprunté.")


def rendre(num_etu):
    """
    Procédure de rendu d'un livre
    """
    print("\n--------------\nRendre un livre\n--------------")

    # Récupération des emprunts de l'élève (s'il y en a)
    emprunts = requete("SELECT titre, nom, annee, isbn, date_ret FROM Emprunt "
                       "JOIN Livre USING (isbn)"
                       "JOIN Ecrire USING(isbn) "
                       "JOIN Auteur USING (a_id)"
                       "WHERE num_etu = ?", [num_etu])

    if emprunts:  # Si l'élève à des emprunts en cours
        # Recherche d'emprunt (via l'ISBN, ou le titre, l'auteur et l'année), et potentiel choix s'il y a plusieurs résultats
        titre, auteur, annee, isbn, date_ret = choix_livre(emprunts,
                                                           ["Titre", "Auteur.e", "Année", "ISBN", "Date retour"])

        # Suppression de l'emprunt à partir du numéro d'étudiant
        requete("DELETE FROM Emprunt WHERE isbn = ?", [isbn])

        print(f"\nLe livre {titre} de {auteur} à correctement été rendu.")

    else:  # Si aucun emprunt n'a été trouvé
        print("\nVous n'avez actuellement aucun emprunt de livre.")


def ajouter_auteur():
    """
    Procédure d'ajout d'un auteur
    """
    print("\n----------------\nAjouter un auteur\n----------------")

    while True:  # Tant que l'auteur n'a pas été saisi
        nom = input("Saisissez le nom de l'auteur : ")
        if nom:
            break
        print("\nVeuillez saisir le nom de l'auteur.")

    # Rechercher l'id de l'auteur avec le nom saisi (en ignorant les minuscules)
    a_id = requete("SELECT a_id FROM Auteur WHERE UPPER(nom) = UPPER(?)", [nom])

    if a_id:  # Si le nom de l'auteur saisi a été trouvé
        print(f"\nL'auteur {nom} existe déjà dans la base de donnée du CDI.")

    else:  # Si le nom de l'auteur saisi n'a pas été trouvé

        # Obtenir un nouvel id pour le nouvel auteur (en ajoutant 1 à l'id maximal de la table)
        a_id = int(requete("SELECT MAX(a_id) FROM Auteur")[0][0]) + 1

        # Ajouter l'auteur avec son id et son nom
        requete("INSERT INTO Auteur VALUES (?, ?)", [a_id, nom])

        print(f"\nL'auteur {nom} à correctement été ajouté à la base de donnée du CDI.")


def ajouter_livre():
    """
    Procédure d'ajout de livre
    """
    print("\n-------------\nAjouter un livre\n-------------")

    while True:  # Tant que l'ISBN n'a pas été saisi correctement
        isbn = input("Saisissez l'ISBN du livre : ")
        if not isbn:
            print("\nVeuillez saisir un ISBN.")
        elif requete("SELECT isbn FROM Livre WHERE isbn = ?", [isbn]):
            print(f"\nL'ISBN {isbn} est déjà présent dans la base de donnée.")
        else:
            break

    while True:  # Tant que le siret n'a pas été saisi
        siret = input("Saisissez le siret du livre : ")
        if siret:
            break
        print("\nVeuillez saisir un siret.")

    while True:  # Tant que le titre n'a pas été saisi
        titre = input("Saisissez le titre du livre : ")
        if titre:
            break
        print("\nVeuillez saisir un titre.")

    while True:  # Tant que l'année n'a pas été saisie correctement
        annee = input("Saisissez l'année de publication du livre : ")
        if not annee:
            print("\nVeuillez saisir une année.")
        elif not annee.isdigit():
            print("\nVeuillez saisir une année correcte.")
        else:
            break

    while True:  # Tant que l'auteur n'a pas été saisi
        auteur = input("Saisissez l'auteur du livre : ")
        if auteur:
            break
        print("\nVeuillez saisir l'auteur du livre.")

    # Ajouter le livre avec son ISBN, siret, titre et son année de publication.
    requete("INSERT INTO Livre VALUES (?, ?, ?, ?)", [isbn, siret, titre, annee])

    # Rechercher l'id de l'auteur avec le nom saisi (en ignorant les minuscules)
    a_id = requete("SELECT a_id FROM Auteur WHERE UPPER(nom) = UPPER(?)", [auteur])

    if not auteur:  # Si le nom de l'auteur saisi n'a pas été trouvé

        # Obtenir un nouvel id pour le nouvel auteur (en ajoutant 1 à l'id maximal de la table)
        a_id = int(requete("SELECT MAX(a_id) FROM Auteur")[0][0]) + 1

        # Ajouter l'auteur avec son id et son nom
        requete("INSERT INTO Auteur VALUES (?, ?)", [a_id, auteur])

        # Ajouter la relation Ecrire avec l'id de l'auteur et l'isbn du livre
        requete("INSERT INTO Ecrire VALUES (?, ?)", [a_id, isbn])

        print(
            f"\nLe livre {titre} a correctement été ajouté à la base de donnée du CDI, avec un nouvel auteur : {auteur}.")

    else:  # Si le nom de l'auteur saisi a été trouvé

        # Ajouter la relation Ecrire avec l'id de l'auteur existant et l'isbn du livre
        requete("INSERT INTO Ecrire VALUES (?, ?)", [a_id[0][0], isbn])

        print(f"\nLe livre {titre} a correctement été ajouté à la base de donnée du CDI.")


def supprimer():
    """
    Procédure de suppression de livre
    """
    print("\n----------------\nSupprimer un livre\n----------------")

    # Recherche de livre (via l'ISBN, ou le titre, l'auteur et l'année), et potentiel choix s'il y a plusieurs résultats
    titre, auteur, annee, isbn = recherche_livre()

    # Suppression du livre via l'ISBN
    requete("DELETE FROM Livre WHERE isbn = ?", [isbn])

    # Rechercher l'id de l'auteur avec le nom saisi (en ignorant les minuscules)
    a_id = int(requete("SELECT a_id FROM Auteur WHERE UPPER(nom) = UPPER(?)", [auteur])[0][0])

    # Supprimer la relation Ecrire avec l'id de l'auteur et l'isbn du livre
    requete("DELETE FROM Ecrire WHERE isbn = ? AND a_id = ?", [isbn, a_id])

    # Obtenir tous les livres de l'auteur
    livres_auteur = requete("SELECT COUNT(*) FROM Ecrire WHERE a_id = ?", [a_id])[0][0]

    if livres_auteur == 0:  # Si l'auteur n'a écrit plus aucun livre

        while True:  # Tant que l'utilisateur n'a pas fait de choix
            print(
                f"\nLe livre que vous avez supprimé était le dernier livre écrit par {auteur} dans la base de donnée.",
                "\nVoulez vous supprimer l'auteur de la base de donnée ?", "\n(o) oui, le supprimer",
                "\n(n) non, le garder")
            choix = input("\nVotre choix : ")
            match choix:
                case "o":
                    # Suppression de l'auteur via son id
                    requete("DELETE FROM Auteur WHERE a_id = ?", [a_id])
                    print(f"Le livre {titre} à correctement été supprimé.",
                          f"L'auteur {auteur} a également été supprimé de la base de donnée.")
                    break
                case "n":
                    print(f"Le livre {titre} à correctement été supprimé.",
                          f"L'auteur {auteur} a été conservé dans la base de donnée.")
                    break
                case _:
                    print("Je n'ai pas compris...")

    else:  # S'il reste des livres écrits par l'auteur
        print(f"Le livre {titre} de {auteur} à été supprimé de la base de donnée.")


def rechercher_emprunt(num_etu):
    """
    Procédure de recherche d'emprunt
    """
    print("\n---------------------\nRechercher un emprunt\n---------------------")

    # Récupération des emprunts de l'élève (s'il y en a)
    emprunts = requete("SELECT titre, nom, annee, isbn, date_ret FROM Emprunt "
                       "JOIN Livre USING (isbn)"
                       "JOIN Ecrire USING(isbn) "
                       "JOIN Auteur USING (a_id)"
                       "WHERE num_etu = ?", [num_etu])

    if emprunts:  # S'il existe des emprunts

        # Création d'une table avec la librairie prettytable qui contient les emprunts
        table = prettytable.PrettyTable()
        table.field_names = ["Titre", "Auteur.e", "Année", "ISBN", "Date retour"]
        table.add_rows(emprunts)
        print(table)
    else:
        print("Vous n'avez pas d'emprunt actuellement.")


def recherche_livre():
    """
    Fonction qui permet de trouver un livre (puis de choisir s'il y a plusieurs résultats) soit grâce à l'ISBN, soit avec le titre, l'auteur et l'année.
    """
    while True:  # Tant qu'aucun livre n'a été trouvé
        isbn = input("ISBN (laisser vide pour rechercher avec le titre, l'auteur et l'année) : ")

        # Formatage des champs pour la requête SQL
        titre, auteur, annee = "%%", "%%", "%%"
        if not isbn:  # Si l'ISBN n'a pas été saisi
            titre = "%" + input("Titre : ") + "%"
            auteur = "%" + input("Auteur.e : ") + "%"
            annee = "%" + input("Année : ") + "%"
            isbn = "%%"

        # Recherche des livres trouvés avec les paramètres saisis.
        resultats = requete("SELECT titre, nom, annee, isbn FROM Livre "
                            "JOIN Ecrire USING(isbn)"
                            "JOIN Auteur USING(a_id)"
                            "WHERE titre LIKE ? AND nom LIKE ? AND annee LIKE ? AND isbn LIKE ?",
                            [titre, auteur, annee, isbn])

        if resultats:  # Si un ou plusieurs livres ont été trouvés
            return choix_livre(resultats, ["Titre", "Auteur.e", "Année", "ISBN"])

        print("\nAucun livre n'a été trouvé avec vos paramètres de recherche, veuillez réessayer.")


def choix_livre(resultats, noms_champs):
    """
    Permet de créer un tableau avec les résultats fournis en arguments et laisser l'utilisateur choisir le choix final.
    """
    nbr_resultats = len(resultats)
    if nbr_resultats == 1:
        return resultats[0]

    # Création d'une table avec la librairie prettytable
    table = prettytable.PrettyTable()
    table.field_names = ["#"] + noms_champs
    table.add_rows([[i, *rows] for i, rows in enumerate(resultats, start=1)])

    print("\n", table, "\nPlusieurs livres ont étés trouvés avec vos paramètres de recherche.")

    while True:  # Tant que le numéro n'a pas été saisi correctement
        choix = input("Préciser le livre recherché avec son numéro indiqué dans la liste : ")
        try:
            nombre = int(choix)
            if 0 <= nombre <= nbr_resultats:  # Vérifier si le numéro est compris entre 0 et le numéro maximal des résultats

                # Renvoyer le résultat (-1 car l'utilisateur saisi 1 au lieu de 0)
                return resultats[nombre - 1]

            print("\nVeuillez saisir un numéro compris entre 1 et", str(nbr_resultats))
        except ValueError:
            print("\nVeuillez saisir un numéro correct.")


def requete(sql, arguments=None):
    """
    Execute la requête SQL fournie en ajoutant les arguments fournis et renvoie éventuellement le résultat s'il y en a un
    """
    with sqlite3.connect('cdi.db') as connexion:  # Connexion à la base de donnée
        curseur = connexion.cursor()

        if arguments:
            # Exécuter la requête avec les arguments fournis en paramètres
            curseur.execute(sql, arguments)
        else:
            # Exécuter la requête sans arguments
            curseur.execute(sql)

        # Récupérer le résultat (si la requête était un SELECT, COUNT, etc ...)
        resultat = curseur.fetchall()

        # Effectuer les changements dans la base de donnée (pour les INSERT, DELETE, etc ...)
        connexion.commit()

        # Renvoyer le résultat
        return resultat


# Lancement du programme avec la connexion de l'utilisateur
login()
