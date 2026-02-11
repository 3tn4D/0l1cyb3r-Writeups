import zipfile
import os

wordlist = open("rockyou.txt", "rb")

for i in range(100, 0, -1):
    wordlist.seek(0)

    with zipfile.ZipFile(f"{i}.zip", 'r') as z:
        for pwd in wordlist:
            pwd = pwd.strip()

            try:
                z.extractall(pwd=pwd)
                print(f"{i}.zip  --> [+] Password trovata: {pwd.decode()}")
                break
            except:
                continue

    if i != 0 :
        os.remove(f"{i}.zip")