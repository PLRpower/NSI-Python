import datetime
import sqlite3

import prettytable


def login():
    """
    Procédure de connexion avec l'identifiant du numéro de l'élève
    """
    print("\n---------\nConnexion\n---------")
    while True:  # Tant que l'utilisateur n'est pas connecté

        # Recherche du numéro d'étudiant dans la base de donnée
        num_etu = input("Saisissez votre numéro d'étudiant (copier-coller : 745611421242) : ")
        etudiant = requete("SELECT nom, prenom FROM Eleve WHERE num_etu = ?", [num_etu])

        if etudiant:  # Si le numéro d'étudiant a été trouvé
            nom, prenom = etudiant[0]
            print("\nBienvenue dans le centre de documentation et d'information", nom, prenom, "!")
            input("Accéder au menu (entrée) >")  # Attente de l'utilisateur avant d'accéder au menu
            return menu(num_etu)  # Arrêter la boucle et continuer sur le menu
        print("\nNuméro d'étudiant introuvable, veuillez réessayez.")


def menu(num_etu):
    """
    Navigation dans les options possibles via un menu
    """
    while True:
        print("\n----", "Menu", "----", "(d) rechercher un livre", "(e) emprunter", "(r) rendre", "(a) ajouter",
              "(s) supprimer", "(p) rechercher un prêt", "(q) quitter", sep="\n")
        choix = input("\nQue souhaitez vous faire ? ")
        match choix:
            case "d":
                rechercher_livre()
            case "e":
                emprunter(num_etu)
            case "r":
                rendre(num_etu)
            case "a":
                ajouter()
            case "s":
                supprimer()
            case "p":
                rechercher_pret(num_etu)
            case "q":
                break
            case _:
                print("Je n'ai pas compris...")
        input("Retourner au menu (entrée) >")  # Attente de l'utilisateur avant de retourner au menu
    print("\nSortie du programme. Au revoir !")


def rechercher_livre():
    """
    Procédure de recherche de livre et d'affichage de ses informations
    """
    print("\n------------------\nRecherche de livre\n------------------")

    # Procédure de recherche du livre dans la base de données
    titre, auteur, annee, isbn = choix_livre(recherche(), ["Titre", "Auteur.e", "Année", "ISBN"])

    # Récupération de la date de retour de l'emprunt (s'il y en a un)
    emprunt = requete("SELECT date_ret FROM Emprunt WHERE isbn = ?", [isbn])

    # Affichage des informations sur le livre et l'emprunt en cours
    print(
        f"\nLe livre intitulé '{titre}' de {auteur}, qui a été publié en {annee} sous l'ISBN {isbn} a été découvert dans le centre de documentation et d'information.")
    print(
        f"Il est actuellement emprunté jusqu'au {emprunt[0][0]}." if emprunt else "Il n'est actuellement pas emprunté.")


def emprunter(num_etu):
    """
    Procédure d'emprunt d'un livre
    """
    print("\n-------\nEmprunt\n-------")

    # Procédure de recherche du livre dans la base de données
    titre, auteur, annee, isbn = choix_livre(recherche(), ["Titre", "Auteur.e", "Année", "ISBN"])

    try:
        # Obtenir la date en format DATETIME du jour actuel + 3 semaines (durée de l'emprunt)
        date_retour = (datetime.date.today() + datetime.timedelta(weeks=3)).strftime('%Y-%m-%d')

        # Ajouter dans la base de donnée un emprunt avec le numéro de l'étudiant
        requete("INSERT INTO Emprunt VALUES (?, ?, ?)", [isbn, num_etu, date_retour])

        print(f"\nVous avez correctement emprunté le livre intitulé '{titre}' de {auteur} jusqu'au {date_retour}")
    except sqlite3.Error:
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

    if emprunts:
        # Procédure de recherche du livre emprunté souhaité
        titre, auteur, annee, isbn, date_ret = choix_livre(emprunts,
                                                           ["Titre", "Auteur.e", "Année", "ISBN", "Date retour"])

        # Suppression de l'emprunt dans la base de donnée à partir du numéro d'étudiant
        requete("DELETE FROM Emprunt WHERE isbn = ?", [isbn])

        print(f"\nLe livre {titre} de {auteur} à correctement été rendu.")
    else:
        print("\nVous n'avez actuellement aucun emprunt de livre.")


def ajouter():
    """
    Procédure d'ajout de livre/auteur
    """
    print("\n--------\nAjouter\n--------")

    while True:  # Tant que l'utilisateur ne choisi pas entre l'auteur et le livre
        print("(a) ajouter un auteur\n(l) ajouter un livre")
        choix = input("\nQue souhaitez vous faire ? ")
        match choix:

            case "a":  # Ajout d'un auteur
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

            case "l":  # Ajout d'un livre
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
                    print(
                        f"\nLe livre {titre} a correctement été ajouté à la base de donnée du CDI, avec un nouvel auteur : {auteur}.")

                else:
                    requete("INSERT INTO Ecrire VALUES (?, ?)", [a_id[0][0], isbn])
                    print(f"\nLe livre {titre} a correctement été ajouté à la base de donnée du CDI.")
                break
            case _:
                print("Je n'ai pas compris...")


def supprimer():
    print("\n----------------\nSupprimer un livre\n----------------")
    titre, auteur, annee, isbn = choix_livre(recherche(), ["Titre", "Auteur.e", "Année", "ISBN"])

    requete("DELETE FROM Livre WHERE isbn = ?", [isbn])
    a_id = int(requete("SELECT a_id FROM Auteur WHERE UPPER(nom) = UPPER(?)", [auteur])[0][0])
    print(a_id)
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


def rechercher_pret(num_etu):
    # Récupération des emprunts de l'élève (s'il y en a)
    emprunts = requete("SELECT titre, nom, annee, isbn, date_ret FROM Emprunt "
                       "JOIN Livre USING (isbn)"
                       "JOIN Ecrire USING(isbn) "
                       "JOIN Auteur USING (a_id)"
                       "WHERE num_etu = ?", [num_etu])

    if emprunts:
        table = prettytable.PrettyTable()
        table.field_names = ["Titre", "Auteur.e", "Année", "ISBN", "Date retour"]
        table.add_rows(emprunts)
        print("\n", table)
    else:
        print("Vous n'avez pas d'emprunt actuellement.")


def recherche():
    """
    Fonction qui permet de trouver un livre soit grâce à l'ISBN, soit avec le titre, l'auteur et l'année.
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
    return recherche()


def choix_livre(resultats, noms_champs):
    """
    Permet de créer un tableau avec les résultats fournis en arguments et laisser l'utilisateur choisir le choix final.
    """
    nombre_resultats = len(resultats)
    if nombre_resultats == 1:
        return resultats[0]
    table = prettytable.PrettyTable()
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


login()
