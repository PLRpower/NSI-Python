def affiche(mot):
    for i in mot:
        print(i)


def longueur(mot):
    count = 0
    for _ in mot:
        count += 1
    return count


assert longueur("abracadabra") == 11


def recherche(caractere, mot):
    count = 0
    for i in mot:
        if i == caractere:
            count += 1
    return count


assert recherche('e', "sciences") == 2
assert recherche('i', "mississippi") == 4
assert recherche('a', "mississippi") == 0


def occurrence_lettres(chaine):
    dictionnaire = {}
    for caractere in chaine:
        if caractere in dictionnaire:
            dictionnaire[caractere] += 1
        else:
            dictionnaire[caractere] = 1
    return dictionnaire


def anagramme(mot1, mot2):
    return occurrence_lettres(mot1) == occurrence_lettres(mot2)


def occurrence_max(chaine):
    if not chaine:
        return None
    else:
        dictionnaire = {chaine[0]: 1}
        caractere_max = chaine[0]
        frequence_max = 1

        for caractere in chaine[1:]:
            if caractere in dictionnaire:
                dictionnaire[caractere] += 1

                if dictionnaire[caractere] > frequence_max:
                    frequence_max = dictionnaire[caractere]
                    caractere_max = caractere
            else:
                dictionnaire[caractere] = 1

        return caractere_max


assert occurrence_max("je suis en terminale et je passe le bac") == 'e'


def inverse_chaine(chaine):
    result = ""
    for caractere in chaine:
        result = caractere + result
    return result


def est_palindrome(chaine):
    inverse = inverse_chaine(chaine)
    return chaine == inverse


assert inverse_chaine('bac') == 'cab'
assert not est_palindrome('NSI')
assert est_palindrome('ISN-NSI')

dico = {chr(ord('A') + i): i + 1 for i in range(26)}


def est_parfait(mot):
    code_a = 0
    code_c = ""
    for c in mot:
        code_a = code_a + int(dico[c])
        code_c = code_c + str(dico[c])
    code_c = int(code_c)
    parfait = code_c % code_a == 0
    return code_a, code_c, parfait


assert est_parfait("PAUL") == (50, 1612112, False)
assert est_parfait("ALAIN") == (37, 1121914, True)


def recherche(gene, seq_adn):
    n = len(seq_adn)
    g = len(gene)
    i = 0
    trouve = False
    while i < n and not trouve:
        j = 0
        while j < g and gene[j] == seq_adn[i + j]:
            j += 1
            if j == g:
                trouve = True
        i += 1
    return trouve


assert recherche("AATC", "GTACAAATCTTGCC")
