# Inserire come path per visualizzare il contenuto dei file: ../../passwords

f = open("../passwords.txt", "r").read()

flag = f.split("flag1:")[1].strip()
print(bytes.fromhex(flag).decode())