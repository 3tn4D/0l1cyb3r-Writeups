import requests

s = requests.Session()
s.get("http://web-06.challs.olicyber.it/token")
print(s.cookies)

r = s.get("http://web-06.challs.olicyber.it/flag")

print(r.text)
