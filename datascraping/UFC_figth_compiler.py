#! python3
# Compiles a list of all UFC fights a figther have participated in

import requests, bs4

UFCStart = 89
UFCEnd = 150

url = 'https://en.wikipedia.org/wiki/UFC_'

for urlNumber in range(UFCStart, UFCEnd):
    # Download the page
    res = requests.get(url + str(urlNumber))
    res.raise_for_status()

    soup = bs4.BeautifulSoup(res.text, 'html.parser')

    if (soup.find("a", string="Jim Miller")) != None:
        print(urlNumber)