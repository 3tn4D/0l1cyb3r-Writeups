def get_value(item):
    return item[1]

def change_value(text, letter_rep):
    italian_freq = [
        "e","a","i","o","l","n","r","t","s","c","d","u","p","m","v","g",
        "h","b","f","q","z","k","j","w","y","x"
    ]

    mapping = {}
    for i in range(len(letter_rep)):
        cif_letter = letter_rep[i][0]
        plain_letter = italian_freq[i]
        mapping[cif_letter] = plain_letter

    result = ""
    for ch in text:
        if ch in mapping:
            result += mapping[ch]
        else:
            result += ch

    return result


ciphertext = open("ciphertext.txt", "r").read().lower()

mappa = {chr(c): 0 for c in range(ord('a'), ord('z')+1)}

for c in  ciphertext:
    if c in mappa:
        mappa[c] += 1
mappa = sorted(mappa.items(), key=get_value, reverse=True)

plaintext = change_value(ciphertext, mappa)

print(mappa)

open("plaintext.txt", "w").write(plaintext)
