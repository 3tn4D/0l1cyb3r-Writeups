import string

words = [
    "casa", "albero", "notte", "sole", "montagna", "fiume", "mare", "vento", "nuvola", 
    "pioggia", "strada", "amico", "sorriso", "viaggio", "tempo", "cuore", "stella", 
    "sogno", "giorno", "libro", "porta", "luce", "ombra", "silenzio", "fiore", "luna"
]

flag =""

str = ""
with open("passphrase.txt", "r") as f:
    str = f.read().strip()

passphrase = str.replace("{", "").replace("-}", "").replace("-_","").split("-")

for w in passphrase:
    for c in string.ascii_lowercase:
        if words[ord(c) - ord('a')] == w:
            flag += c
            break

print("flag{" + flag[4:] + "}")