import datetime
import sqlite3

from prettytable import PrettyTable


def main():
    # Connexion avec l'identifiant d'un étudiant
    print("\n---------\nConnexion\n---------")
    while True:
        num_etu = input("Saisissez votre numéro d'étudiant : ")
        etudiant = requete("SELECT nom, prenom FROM Eleve WHERE num_etu LIKE ?", [num_etu])
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
        input("\nRetourner au menu (entrée) >")  # Attente de l'utilisateur avant de retourner au menu
    print("\nSortie du programme. Au revoir !")


def rechercher():
    print("\n------------------\nRecherche de livre\n------------------")

    # Procédure de recherche du livre dans la base de données
    titre, auteur, annee, isbn = afficher_resultats(recherche_livre(), ["Titre", "Auteur.e", "Année", "ISBN"])

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
    titre, auteur, annee, isbn = afficher_resultats(recherche_livre(), ["Titre", "Auteur.e", "Année", "ISBN"])

    # Récupération de la date de retour de l'emprunt (s'il y en a un)
    emprunt = requete("SELECT date_ret FROM Emprunt WHERE isbn LIKE ?", [isbn])

    if emprunt:  # Si le livre est déjà emprunté
        print(f"\nCe livre est déjà emprunté (jusqu'au {emprunt[0][0]}).", end="")
        return
    date_retour = (datetime.date.today() + datetime.timedelta(weeks=3)).strftime('%Y-%m-%d')
    requete("INSERT INTO Emprunt VALUES (?, ?, ?)", [isbn, num_etu, date_retour])
    print(f"\nVous avez correctement emprunté le livre intitulé '{titre}' de {auteur} jusqu'au {date_retour}")


def rendre():
    print("\n--------------\nRendre un livre\n--------------")

    # Saisie du numéro d'étudiant de l'élève
    eleve = input("Saisissez votre numéro d'étudiant : ")

    # Récupération des emprunts de l'élève (s'il y en a)
    emprunts = requete("SELECT titre, nom, annee, isbn, date_ret FROM Emprunt "
                       "JOIN Livre USING (isbn)"
                       "JOIN Ecrire USING(isbn) "
                       "JOIN Auteur USING (a_id)"
                       "WHERE num_etu LIKE ?", [eleve])

    if emprunts:
        # Procédure de recherche du livre emprunté souhaité
        titre, auteur, annee, isbn, date_ret = afficher_resultats(emprunts,
                                                                  ["Titre", "Auteur.e", "Année", "ISBN", "Date retour"])
        requete("DELETE FROM Emprunt WHERE isbn LIKE ?", [isbn])
        print(f"\nLe livre {titre} de {auteur} à correctement été rendu.")
        return
    print("\nCet.te élève.e n'a actuellement aucun emprunt de livre.")


def ajouter():
    print("\n----------\nAjouter\n----------")


def recherche_livre():
    """
    Procédure de recherche d'un livre (avec le titre, l'auteur, l'année et l'ISBN).
    """
    titre = "%" + input("Titre : ") + "%"
    auteur = "%" + input("Auteur.e : ") + "%"
    annee = "%" + input("Année : ") + "%"
    isbn = "%" + input("ISBN : ") + "%"

    resultats = requete("SELECT titre, nom, annee, isbn FROM Livre "
                        "JOIN Ecrire USING(isbn)"
                        "JOIN Auteur USING(a_id)"
                        "WHERE titre LIKE ? AND nom LIKE ? AND annee LIKE ? AND isbn LIKE ?",
                        [titre, auteur, annee, isbn])

    if resultats:
        return resultats
    print("\nAucun livre n'a été trouvé avec vos paramètres de recherche, veuillez réessayer.")
    return recherche_livre()


def afficher_resultats(resultats, noms_champs):
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


def requete(sql: str, arguments: list):
    """
    Execute la requête SQL fournie en ajoutant les arguments fournis et renvoie éventuellement le résultat
    """
    with sqlite3.connect('cdi.db') as connexion:  # Connexion à la base de donnée
        curseur = connexion.cursor()
        curseur.execute(sql, arguments)  # Exécuter la requête
        resultat = curseur.fetchall()  # Récupérer le résultat (si la requête était un SELECT)
        connexion.commit()  # Sauvegarder les changements (pour les INSERT, DELETE, etc ...)
        return resultat  # Renvoyer le résultat (par exemple pour les requêtes SELECT)


main()
