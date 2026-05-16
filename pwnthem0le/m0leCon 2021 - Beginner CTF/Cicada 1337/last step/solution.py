with open("input.txt", "r") as f:
    idx = f.readline().split(" ")
    f.readline()

    testo = f.readlines()

flag = ""
for i in idx:
    curr = i.split(":")
    x = int(curr[0])
    y = int(curr[1])

    flag += testo[x-1][y-1]

print(flag)