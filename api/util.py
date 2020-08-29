from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

def getStuff(url):
    stuff = []
    #url = input("Please enter a valid URL: ")
    soup = BeautifulSoup(urlopen(url))

    
    try:
        stuff.append(soup.find(attrs={"class": re.compile(".author")}).text)
    except:
        stuff.append("no author")
    stuff.append(soup.find("head").find("title").text)
    try:
        stuff.append(soup.find('article').text)
    except:
        try:
            stuff.append(soup.find(attrs={"class": re.compile(".story")}).text)
        except:
            try:
                stuff.append(soup.find(attrs={"class": re.compile(".body")}).text)
            except:
                try:
                    stuff.append("boo\n")
                    paragraphs = soup.find_all("p")
                    textList = []
                    for p in paragraphs:
                        textList.append(p.text)
                    stuff.append(" ".join(textList))
                except:
                    stuff.append("error")
    return stuff
