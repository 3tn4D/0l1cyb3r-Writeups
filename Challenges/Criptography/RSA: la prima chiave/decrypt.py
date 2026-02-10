import string

file = open("dati.txt", "r")

e = int(file.readline().split()[2])
n = int(file.readline().split()[2])
c = file.readline().split("=")[1].strip().strip("[]").split(",")
c = [x.strip() for x in c]
c = [int(x) for x in c]

for i in c:
    for j in string.printable:
        chiper = pow(ord(j), e, n)

        if chiper == i:
            print(j, end="")

print()