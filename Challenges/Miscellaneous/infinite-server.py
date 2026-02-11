import re
import requests
from bs4 import BeautifulSoup

url = "http://infinite.challs.olicyber.it/"

s = requests.Session()
r = s.get(url)
soup = BeautifulSoup(r.text, "html.parser")

i = 0

while True:
    test = soup.find("h2").text.strip()

    if test == "MATH TEST": 
        domanda = soup.find("p").text.strip()
        nums = [int(n) for n in re.findall(r"-?\d+", domanda)] # Trova tutti i numeri
        result = sum(nums)

        data = {"sum": str(result)}
        res = s.post(url, data=data)

        print(i)
        i += 1

        soup = BeautifulSoup(res.text, "html.parser") 
        continue

    elif test == "ART TEST":
        domanda = soup.find("p").text.strip()
        color = domanda.split("colore")[1].strip(" ?")

        data = {color: ""}
        res = s.post(url, data=data)
        
        print(i)
        i += 1

        soup = BeautifulSoup(res.text, "html.parser") 
        continue

    elif test == "GRAMMAR TEST":
        domanda = soup.find("p").text.strip()
        parole = re.findall(r'"(.*?)"', domanda)

        num = parole[1].count(parole[0])

        data = {"letter": str(num)}
        res = s.post(url, data=data)

        print(i)
        i += 1

        soup = BeautifulSoup(res.text, "html.parser") 
        continue

    else:
        print(test)
        print(soup.find("p").text.strip())
        break