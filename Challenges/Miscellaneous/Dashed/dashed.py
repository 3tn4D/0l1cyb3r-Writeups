from base64 import b64decode

MORSE_CODE = {
    '.-'    : 'A', '-...'  : 'B',
    '-.-.'  : 'C', '-..'   : 'D',
    '.'     : 'E', '..-.'  : 'F',
    '--.'   : 'G', '....'  : 'H',
    '..'    : 'I', '.---'  : 'J',
    '-.-'   : 'K', '.-..'  : 'L',
    '--'    : 'M', '-.'    : 'N',
    '---'   : 'O', '.--.'  : 'P',
    '--.-'  : 'Q', '.-.'   : 'R',
    '...'   : 'S', '-'     : 'T',
    '..-'   : 'U', '...-'  : 'V',
    '.--'   : 'W', '-..-'  : 'X',
    '-.--'  : 'Y', '--..'  : 'Z',
    '.----' : '1', '..---' : '2',
    '...--' : '3', '....-' : '4',
    '.....' : '5', '-....' : '6',
    '--...' : '7', '---..' : '8',
    '----.' : '9', '-----' : '0',
    '--..--': ', ', '.-.-.-': '.',
    '..--..': '?', '-..-.' : '/',
    '-....-': '-', '-.--.' : '(',
    '-.--.-': ')'
}

flag1 = str(open("dashed.txt", "r").read()).split(" ")
text = ""

# Codice mors
for c in flag1:
    text += MORSE_CODE[c]

text = text.replace("0X", "").replace(",", "").split(" ")

# Esadecimale
flag2 = ""
for c in text:
    flag2 += bytes.fromhex(c).decode("ascii")

# Binario
flag3 = int(flag2, 2).to_bytes((len(flag2) + 7) // 8, "big").decode("ascii")

# Base 64
flag4 = b64decode(flag3).decode()

# Cifrario di Cesare
flag5 = ""
shift = 13
for c in flag4:
    if c.isalpha():
        upper = c.isupper()

        c = c.upper()

        pos = ord(c) + ord('A')
        c_new = (pos + shift) % 26

        if not upper :
            flag5 += chr(c_new + ord('A')).lower()
        else:
            flag5 += chr(c_new + ord('A'))
    else:
        flag5 += c

print(flag5)