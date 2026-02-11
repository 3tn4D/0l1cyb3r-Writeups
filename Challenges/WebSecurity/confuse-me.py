from Cryptodome.Hash import MD5

# Se le due stringhe sono numeriche ("0e1234" == "0e3245678") l'operatore == le converte in numeri
# e se si usa 0e qualunque cosa ci sia dopo diventa 0 il risultato

i = 0

while True:
    input = "0e" + str(i)

    h = MD5.new(input.encode()).hexdigest()

    if h.startswith("0e") and h[2:].isdigit():
        print(f"Found: {input}")
        exit(0)
    
    # print(f"Trying: {input}")

    i += 1