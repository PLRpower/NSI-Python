import sqlite3


def main():
    stop = False
    while not stop:
        print("", "Choix :",
              "rechercher un document (d)",
              "emprunter (e)",
              "rendre (r)",
              "ajouter (a)",
              "supprimer (s)",
              "rechercher un prêt (p)",
              "quitter (q)", sep="\n")
        choix = input("Quel est votre choix ? ")
        match choix:
            case "d":
                rechercher_document()
            case "e":
                pass
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


def rechercher_document():
    print("", "---------", "Rechercher un document (laisser les champs non désirés vide pour "
                           "ne pas les prendre en compte dans la recherche", sep="\n")
    titre = "%" + input("Titre : ") + "%"
    auteur = "%" + input("Auteur.e : ") + "%"
    annee = "%" + input("Année : ") + "%"
    isbn = "%" + input("ISBN : ") + "%"

    conn, cursor = ouvrir_connexion()
    cursor.execute(
        "SELECT Livre.*, Auteur.nom FROM Livre "
        "JOIN Ecrire USING(isbn)"
        "JOIN Auteur USING(a_id)"
        "WHERE titre LIKE ? AND nom LIKE ? AND annee LIKE ? AND isbn LIKE ?",
        (titre, auteur, annee, isbn)
    )
    resultat = cursor.fetchall()
    print(resultat)
    fermer_connexion(conn)


def ouvrir_connexion():
    conn = sqlite3.connect('cdi.db')
    return conn, conn.cursor()


def fermer_connexion(conn):
    conn.close()


main()
