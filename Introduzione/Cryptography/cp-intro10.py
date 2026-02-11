data = """
x % 75 = 48
x % 44 = 39
x % 41 = 8
x % 83 = 43
x % 13 = 0
"""

congruences = []

for line in data.strip().splitlines():
    line = line.replace(" ", "")
    mod, rest = line.split("%")[1].split("=")
    congruences.append((int(mod), int(rest)))

M = 1
for mod, res in congruences:
    M *= mod

Mi = []
Yi = []
for mod, res in congruences:
    Mi.append(M // mod)
    Yi.append(pow(M // mod, -1, mod))

x = 0

len = len(congruences)
for i in range(len):
    x += congruences[i][1] * Mi[i] * Yi[i]

x %= M

print(x)