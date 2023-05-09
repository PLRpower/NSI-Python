# Un exemple de table de transition (celle de l’exercice 2) :
tableEx2 = {"E1": {0: (1, ">", "E1"),
                   1: (0, ">", "E1"),
                   None: (None, "<", "E2")},
            "E2": {0: (1, "<", "E3"),
                   1: (0, "<", "E2"),
                   None: (None, ">", "F")},
            "E3": {0: (0, "<", "E3"),
                   1: (1, "<", "E3"),
                   None: (None, ">", "F")}}


def affiche_ruban(ruban):
    print("|", end="")
    for v in ruban:
        if v is None:
            print("   |", end="")
        else:
            print(" " + str(v) + " |", end="")
    print()


def affiche_tete(tete, ruban):
    print(" ", end="")
    i, e = tete
    for j, v in enumerate(ruban):
        if j == i:
            lt = 4 if v is None else 3 + len(str(v))
            s1 = (lt - len(e)) // 2
            print(s1 * " ", e, sep="")
            break
        else:
            lt = 4 if v is None else 3 + len(str(v))
            print(lt * " ", end="")


def affiche_machine(tete, ruban):
    '''affiche la machine, c’est à dire le ruban et la tête'''
    affiche_ruban(ruban)
    affiche_tete(tete, ruban)


def ecrit(ruban, i, w):
    '''écrit sur le ruban la valeur w à l’indice i'''
    ruban[i] = w


def deplace(i, m, ruban):
    '''retourne le nouvel indice de la tête
       et le ruban éventuellement rallongé'''
    if m == ">":  # déplacement à droite
        if i == len(ruban) - 1:
            return i + 1, ruban + [None]
        else:
            return i + 1, ruban
    elif m == "<":  # déplacement à gauche
        if i == 0:
            return i, [None] + ruban
        else:
            return i - 1, ruban
    else:  # aucun déplacement
        return i, ruban


def execute(ruban, tete, etatsFinaux, table):
    '''ruban est une liste non vide
       tete est un couple (indice,état)
       etatsFinaux est une liste d’états finaux
       table est un dictionnaire de dictionnaires de triplets
       dont un exemple est donné plus haut.
       Cette fonction exécute la machine selon les règles
       données dans la table.
       Après chaque étape elle fait afficher l’état de la machine'''
    print("état initial :")
    affiche_machine(tete, ruban)
    while tete[1] not in etatsFinaux:
        i, e = tete
        lu = ruban[i]  # récupère la valeur lue par la tête sur le ruban
        w, m, s = table[e][lu]  # récupère l’action à effectuer selon la table
        ecrit(ruban, i, w)
        i, ruban = deplace(i, m, ruban)
        tete = (i, s)  # nouvelle situation de la tête
        affiche_machine(tete, ruban)


execute([None, None, None, 1, 0, 0, 1, 1, None, None], (3, "E1"), ["F"], tableEx2)
execute([None, None, None, 0, 0, 0, 0, 0, None, None], (3, "E1"), ["F"], tableEx2)
# On peut aussi éxécuter cela :
# execute([1,0,0,1,1],(0,"E1"),["F"],tableEx2)
# execute([0,0,0,0,0],(0,"E1"),["F"],tableEx2)
