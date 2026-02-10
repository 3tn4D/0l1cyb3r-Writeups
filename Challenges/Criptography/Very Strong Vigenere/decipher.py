from itertools import cycle

data = list(open("ct.txt", "r").read())
            
key = list("aoaon")

for c, k in zip(data, cycle(key)):
    if c.isalpha():
        val = ((ord(c) - ord('a')) - (ord(k) - ord('a'))) % 26
        print(chr(val + ord('a')), end="")
    else:
        print(c, end="")

print()

# flag{non_usare_chiavi_piccole}