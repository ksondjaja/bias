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


"""
getBiasIndex(url)
input:  url: a url link
Output: an integer represents its bias index. 
"""
def getBiasIndex(url):
    text = getStuff(url)
    author = text[0]
    headline = text[1]
    content = text[2]

    headlineKeywordsScore = getKeywordsIndex(headline)
    contentKeywordsScore = getKeywordsIndex(content)
    
    keywordsScore = headlineKeywordsScore * 0.1 + contentKeywordsScore * 0.8
    authorScore = getAuthorAuthority(author, keywordsScore)

    biasIndex = headlineKeywordsScore * 0.2 + contentKeywordsScore * 0.6 + authorScore * 0.2

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

    count = 0
    for i in result:
        if i[1] == "JJ":
            count += 1

    score = 100 - (count * 3 / len(result)) * 100
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
    filePath = '/static/api/documents/'
    fileName = 'Names.csv'

    #reader = openCSV(filePath + fileName) #open the CSV file
    reader = openCSV(filePath+fileName)
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
    saveCSV('C:/Users/sondj/OneDrive/Documents/hackathon/bias/api/static/documents/Names.csv', author_list) 
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
getCleanText(text)
Input:  text: a string
Output: a string where invalid characters are removed. 
"""
def getCleanText(text):
    text = text.rstrip("\n")
    return text


# This is the test code. 
def test():

    print("The bias score range from 0 to 100.")
    print("0 means completly biased. 100 means completly unbiased.")

    # Test Code 1 -------------------------------------------------
    text = getStuff("https://www.vox.com/2020-presidential-election/2020/8/25/21400795/rnc-2020-andrew-pollack-parkland-shooting-restorative-justice")
    author = text[0]
    headline = text[1]
    content = text[2]
    BiasScore = getBiasIndex("https://www.vox.com/2020-presidential-election/2020/8/25/21400795/rnc-2020-andrew-pollack-parkland-shooting-restorative-justice")

    # print(content)

    print("The bias Score of", author, "is: ", BiasScore)

    # Test Code 2 -----------------------------------------------
    """
    author = "Soros Wen"
    headline = "How Smart People Deal With People They Don’t Like"
    content = "However, we don’t live in a perfect world. Some people drive us crazy, and we (admittedly) drive a few mad as well. Those we dislike are inconsiderate, rushed, malign our character, question our motives, or just don’t get our jokes at all — but expect us to laugh at all theirs."
    BiasScore = getBiasIndex(headline, content, author)

    print("The bias Score of", author, "is: ", BiasScore)
    """

#if __name__=="__main__":
#    print(default_storage)
