chiper = open("output.txt", "r").read()


cont = 0
curr = ""

for i in chiper:
    if i != curr:
        print(chr(cont), end="")
        cont = 0
        curr = i
    
    cont += 1