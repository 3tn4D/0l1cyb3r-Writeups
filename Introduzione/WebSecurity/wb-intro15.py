import requests
from bs4 import BeautifulSoup

url = "http://web-15.challs.olicyber.it/"

r = requests.get(url)
soup = BeautifulSoup(r.text, "html.parser")

links = []

for link in soup.find_all(True):
    if link.get("href"):
        links.append(link.get("href"))
    if link.get("src"):
        links.append(link.get("src"))

for link in links:
    tmp_r = requests.get(url+link)
    if tmp_r.text.find("flag") != -1:
        print(tmp_r.text)
