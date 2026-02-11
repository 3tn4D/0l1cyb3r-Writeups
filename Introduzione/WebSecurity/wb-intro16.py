from bs4 import BeautifulSoup
import requests

l = {}
p = [""]

url = "http://web-16.challs.olicyber.it"

#Cerca link nella pagina, li memorizza e li apre
while True:
    for pos in p: 
        r = requests.get(url + pos)
        print(url+pos)
        soup = BeautifulSoup(r.text, "html.parser")

        if "flag" in r.text:
            print(soup.find('h1'))
            exit(0)

        print(soup.find('h1'))
        
        for i in soup.find_all("a", href=True):
            if i['href'] not in l:
                l[i['href']] = True
                p.append(i['href'])
                r.close()