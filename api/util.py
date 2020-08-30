from django.core.files.storage import default_storage
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
import json
import csv
import os
import re 

def getStuff(url):
    stuff = []
    try:
        soup = BeautifulSoup(urlopen(url), 'html.parser')
    except:
        return ["error", "error", "error"]
    try:
        stuff.append(soup.find(attrs={"class": re.compile(".author")}).text)
    except:
        stuff.append("no author")
    stuff.append(soup.find("head").find("title").text)
    """try:
        stuff.append(soup.find('article').text)
    except:
        try:
            stuff.append(soup.find(attrs={"class": re.compile(".story")}).text)
        except:
            try:
                stuff.append(soup.find(attrs={"class": re.compile(".body")}).text)
            except:"""
    #placeholders, dont want to backspace that many times
    if 1:
        if 1:
            if 1:
                try:
                    
                    paragraphs = soup.find_all(["p", "div"])
                    textList = []
                    for p in paragraphs:
                        textList.append(p.text)
                    stuff.append(" ".join(textList))
                except:
                    stuff.append("error")
    return stuff


"""
getBiasIndex(url)
input:  url: a url link, must be a string. 
Output: an integer represents its bias index. 
"""
def getBiasIndex(url):
    # Use getStuff() function to extract the content of the url. 
    text = getStuff(url)

    author = text[0]
    headline = text[1]
    content = removeNoice(text[2])

    # calculating the score of each category. 
    headlineKeywordsScore = getKeywordsIndex(headline)
    contentKeywordsScore = getKeywordsIndex(content)
    
    keywordsScore = headlineKeywordsScore * 0.1 + contentKeywordsScore * 0.9
    authorScore = getAuthorAuthority(author, keywordsScore)

    biasIndex = headlineKeywordsScore * 0.2 + contentKeywordsScore * 0.6 + authorScore * 0.2

    # return the keyword score. 
    return biasIndex


"""
getKeywordsIndex(text)
Input:  text: a string. 
Output: an integer that shows the bias score of the text. 
"""
def getKeywordsIndex(text):
    score = 0

    test = nltk.word_tokenize(text)
    
    result = nltk.pos_tag(test)

    #print(result)

    total = 0
    count = 0
    num = 0

    for i in result:
        #print(i)

        # if the word is '?' or '!', it is likely to come from a single person's narrative. 
        if (i[0] == '!' or i[1] == '?'):
            count += 3
            continue

        total += 1

        # We count numarical values. 
        if (i[1] == "CD"):
            num += 1
            continue
        
        # Count the numbers of words that appear to be coming from a person's narrative. 
        word = i[0].lower()
        if (word == "so" or word == "us" or word == "i" or word == "we" or word == 'me'):
            count += 1
            continue
        if (i[1] == "JJ" or i[1] == "ADJ"): 
            count += 1
            continue

    print("count = ", count, ". num = ", num, ". length = ", total)

    score = 100 - ((count - num) * 3 / total) * 100
    return score


"""
getAuthorAuthority(name, keywordsIndex)
Input:  name: a string that contains the name of the author
        keywordsIndex: a float that contains keywordIndex of an article. 
Output: a float that represent the author authority. 
"""
def getAuthorAuthority(name, keywordsIndex):
    if (name == "no author"):
        return 50
    
    author = name.split()

    userhome = os.path.expanduser('~')
    filePath = userhome + r'/Desktop/hackathon/'
    fileName = 'Names.csv'

    reader = openCSV(filePath + fileName) #open the CSV file
    author_list = []

    for line in reader:
        author_list.append(line)

    for line in author_list:
        # if we found the author
        if (line["FirstName"] == author[0] and line["LastName"] == author[1]):
            # calculate the new author authority
            line["Authority"] = keywordsIndex * 0.3 + float(line["Authority"]) * 0.7
            # save the author authority
            saveCSV(filePath + fileName, author_list) 
            #return the author authority
            return line["Authority"]

    # if we didn't find the author
    new_author = {'FirstName': author[0], 'LastName': author[1], 'Authority': keywordsIndex}
    author_list.append(new_author)
    saveCSV(filePath + fileName, author_list) 
    return keywordsIndex 


"""
openCSV(path)
Input:  the directory of a csv file. 
Output: the list of dictionaries stored in the file. 
"""
def openCSV(path):
    try:
        return csv.DictReader(open(path, 'r'))
    except: 
        return []


"""
saveCSV(path, author_list)
Input:  path: a directory. 
        author_list: a list of dictionaries that contains informations of many authors.
Output: none.
"""
def saveCSV(path, author_list):
    field_names = ['FirstName', 'LastName', 'Authority'] 
    try: 
        with open(path, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames = field_names)
            writer.writeheader()
            for author in author_list:
                writer.writerow(author)
    except:
        return ''
        

"""
removeNoice(text)
Input:  text: a string
Output: a string where invalid characters are removed. 
"""
def removeNoice(text):
    # remove all the useless characters. 
    #print(text)

    text = text.rstrip()
    text = re.sub(r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''', " ", text)
    text = re.sub(r"[^a-zA-Z0-9\!\?]+", ' ', text)
    #text = text.replace('<', '').replace('>', '').replace('/', '').replace('+', '').replace('=', '').replace('-', '').replace('_', '').replace('@', '').replace('%', '').replace('^', '').replace('\'', '').replace(';', '').replace(':', '').replace('(', '').replace(')', '')
    #print(text)

    return text
