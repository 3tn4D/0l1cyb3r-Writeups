import requests
from bs4 import BeautifulSoup

r = requests.get("http://web-12.challs.olicyber.it/")
soup = BeautifulSoup(r.text, "html.parser")

# Trova tag nella pagina e li stampa (no ripetizioni)
tags = []

for tag in soup.find_all(True):
    tags.append(tag.name)

print(set(tags))

print(soup.find_all("pre"))
