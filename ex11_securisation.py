import time


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

    lettre_max = max(freq, key=freq.get)
    decalage = ord(lettre_max) - ord('E')
    return chiffre_cesar(msg, -decalage)


def chiffre_xor(msg, cle):
    msgc = []
    long_cle = len(cle)

    for i, x in enumerate(msg):
        indice = i % long_cle
        msgc.append(x ^ cle[indice])

    return bytes(msgc)


message = "L'informatique c'est super!".encode()
clé = "NSI".encode()
msgc = chiffre_xor(message, clé)


def decrypte_xor(msgc):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    temps_depart = time.time()
    for x in alphabet:
        for y in alphabet:
            for z in alphabet:
                try:
                    cle = x + y + z
                    msg = chiffre_xor(msgc, cle.encode()).decode()
                    if msg[-4:] == "nse!":
                        print("Message décrypté avec la clé " + str(cle) + " : " + msg)
                except UnicodeDecodeError:
                    continue
    temps_total = round(time.time() - temps_depart, 2)
    print("Temps total ≈ " + str(temps_total) + "s")


def factorisation(n):
    temps_depart = time.time()
    for i in range(2, n):
        if n % i == 0:
            return i, n // i, time.time() - temps_depart
    return 1, n, time.time() - temps_depart


def log_discret(gu, g, p):
    temps_depart = time.time()
    u = 1
    while not pow(g, u, p) == gu:
        u += 1
    temps_total = round(time.time() - temps_depart, 2)
    print('Résultat : ' + str(u) + ' Temps total ≈ ' + str(temps_total) + 's')


log_discret(273213231, 7, 934741963)
log_discret(360223736, 7, 934741963)
