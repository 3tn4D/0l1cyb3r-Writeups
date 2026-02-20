def decrypt(ciphertext):

    # ------ Inverso livello 3 ------ (Inverto)
    plaintext3 = ciphertext[::-1]
    print("LIVELLO 3:\n", plaintext3)

    # ------ Inverso livello 2 ------ ([lunghezza][numero][lunghezza][numero].......)
    plaintext2 = []
    i = 0
    n = len(plaintext3)

    while i < n:
        length = int(plaintext3[i])
        i += 1
        plaintext2.append(int(plaintext3[i:i+length]))
        i += length
    print("\nLIVELLO 2:\n", plaintext2)

    # ------ Inverso livello 1 ------
    plaintext = ""

    for i in plaintext2:
        if i > 99:
            plaintext += chr(i - 100)
        else:
            plaintext += chr(i + 20)
            
    return plaintext


ciphertext = "6423522322238023102381231023652522102341238229023572002300237725721123462522002313213201235725725729023752902340233223302377280232023"
plaintext = decrypt(ciphertext)

print("\nLIVELLO 1:\n", plaintext)
