from time import sleep
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import re
import pandas
import jieba

html = urlopen("https://movies.yahoo.com.tw/chart.html")
soup = BeautifulSoup(html,'lxml')

session = requests.Session()
headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit 537.36 (KHTML, like Gecko) Chrome","Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"}


#### Top20's linking
linkings = []
i=0
links = soup.find_all('div',{'class':'td'})
for link in links:
    linking = link.find('a')
    if linking != None:
        if i % 2 ==0:
            linkings.append(linking['href'])

        i+=1

###Moive web's information
MovieTitle = []
MovieEngTitle = []
Expect = []
Satisfaction = []
LinkMoreLook = []

def MobvieTitle(Moviehtml):
    req = session.get(Moviehtml, headers=headers)
    soup = BeautifulSoup(req.text,'lxml')
    Movies = soup.find_all('div',{'class':'movie_intro_info _c'})
    for Movie in Movies:
        Title = Movie.find('h1')
        EngTitle = Movie.find('h3')
        expection = Movie.find('div',{'class':"num"})
        satisfaction = Movie.find('div',{'class':'score_num count'})

        MovieTitle.append(Title.getText())
        MovieEngTitle.append(EngTitle.getText())
        Expect.append(expection.getText())
        Satisfaction.append(satisfaction.getText())

    linkMoreLooks = soup.find_all('div',{'class':'btn_plus_more usercom_more gabtn'})
    for linkMoreLook in linkMoreLooks:
        Look = linkMoreLook.find('a')

    LinkMoreLook .append(Look['href'])
    return

###Moive users' comment link
MaxCommentLink = []
def inputUserCommentLink(MovieComment):
    req = session.get(MovieComment,headers = headers)
    soup  = BeautifulSoup(req.text,'lxml')
    comments = soup.find_all('div', {'class': 'page_numbox'})
    if bool(comments):
        for comment in comments:
            links = comment.find_all('a')
            MaxCommentLink.append(links[len(links)-2]['href'])
    else:
        MaxCommentLink.append(MovieComment)


###Movie users's comment
Comment = []
j=0;
def UserComment(s,j):

    if len(s) == 63:
        Movies = 'https://movies.yahoo.com.tw/'+s[:-1]
        max = int(s[-1])
    elif len(s) == 64:
        Movies = 'https://movies.yahoo.com.tw/' + s[:-2]
        max = int(s[-2:])
    else:
        Movies = s +"?sort=update_ts&order=desc&page="
        max = 1
    Comment.append(MovieTitle[j])
    for i in range(0,max):
        Movie = Movies + str(i+1)
        req = session.get(Movie, headers=headers)
        soup = BeautifulSoup(req.text, 'lxml')
        comments = soup.find_all('div',{'class':'usercom_inner _c'})
        for comment in comments:
            Context = comment.find_all('span')
            for context in Context:
                if context.getText() != '':
                    Comment.append(context.getText())

####Chinese sentimentDict
positives_set = {}
negatives_set = {}
not_set = {}
degree_dict={}

stentiment_df = pandas.read_csv('SentimentDict.csv')

def SetDgree(s,d):
    for word in stentiment_df[s]:
        degree_dict[word] = d

def OpenSentimentDict():

    positives_set = set(stentiment_df['positive'])
    negatives_set = set(stentiment_df['negatives'])
    not_set = set(stentiment_df['not'])
    SetDgree('degree-1', 2.2)
    SetDgree('degree-2', 2.0)
    SetDgree('degree-3', 1.8)
    SetDgree('degree-4', 1.6)
    SetDgree('degree-5', 1.4)
    SetDgree('degree-6', 1.2)
    return

# return true if have opposite word
def hasOpposite(wordlist):
    for word in wordlist:
        if word in not_set:
            return True

# return degree if have degree word else return 1.0
def getDegree(wordlist):
    value = 1.0
    for word in wordlist:
        if word in degree_dict:
            value = degree_dict[word]
            return value
    return value


segment = jieba.load_userdict('dict.txt')


def analyze(text):
    tokens = list(jieba.cut(text))
    sum = 0
    for word in tokens:
        if word.lower() in positives_set:
            sum += 1
        elif word.lower() in negatives_set:
            sum -= 1

    if hasOpposite(tokens) == True:
        sum = -sum
    sum = sum * getDegree(tokens)

    return sum

for link in linkings:
    MobvieTitle(link)
    sleep(1)


for linkMoreLook in LinkMoreLook:
    inputUserCommentLink(linkMoreLook)

print(MaxCommentLink)
for MaxLink in MaxCommentLink:
    UserComment(MaxLink,j)
    j += 1

MovieScore = {}
SumScore = 0
LenMovieComment = 0
index = 0

for x in range(0, len(MovieTitle)):
    print(Comment.index(MovieTitle[x]))
    #for i in range(Comment.index(MovieTitle[x])+1,):
        #SumScore = analyze(Comment[i])
        #LenMovieComment += 1

#print(MovieScore)
