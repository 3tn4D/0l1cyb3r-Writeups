import requests
from bs4 import BeautifulSoup, Comment

def is_comment(tag):
    return isinstance(tag, Comment)

r = requests.get("http://web-14.challs.olicyber.it/")
soup = BeautifulSoup(r.text, "html.parser")
    
for comment in soup.find_all(string=is_comment):
    print(comment)    