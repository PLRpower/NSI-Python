def multiple(num):
    """ Obtenir le multiple de 26 dans lequel le nombre num est contenu """
    return 26 * ((num - 65) // 26)


def chiffre_cesar(msg, cle):
    msg_crypte = ""
    for lettre in msg:
        if lettre == " ":  # Si la lettre est un espace
            msg_crypte += " "

        else:
            chiffre = ord(lettre) + cle  # Obtenir la lettre décalée de "clé"

            msg_crypte += chr(chiffre - multiple(chiffre))

    return msg_crypte


def trouve_cesar(msg):
    freq = {}
    for char in msg:
        if char.isalpha() and char.upper() not in freq:
            freq[char.upper()] = 1
        elif char.isalpha():
            freq[char.upper()] += 1

    # Trouve la lettre la plus fréquente dans le message
    lettre_max = max(freq, key=freq.get)
    decalage = ord(lettre_max) - ord('E')

    # Déchiffre le message en utilisant le décalage trouvé
    return chiffre_cesar(msg, -decalage)


print(trouve_cesar('QNAF Y NEVGUZRGVDHR QR Y NZBHE HA CYHF HA RTNYR GBHG RG QRHK ZBVAF HA RTNYR EVRA'))
