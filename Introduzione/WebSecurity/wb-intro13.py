import requests
from bs4 import BeautifulSoup

r = requests.get("http://web-13.challs.olicyber.it/")
soup = BeautifulSoup(r.text, "html.parser")

print("flag{", end="")

for p in soup.find_all("span"): 
    print(p.get_text(), end="")

print("}")