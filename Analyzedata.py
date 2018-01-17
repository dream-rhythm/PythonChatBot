from time import sleep
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
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
        LinkMoreLook.append(Look['href'])
        #print(LinkMoreLook)
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
#Good = []
Bad = []
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
            Good = comment.find_all('div',{'class':'user_star _c'})
            for context in Context:
                if context.getText() != '':
                    Comment.append(context.getText())
####Chinese sentimentDict

degree_dict={}

stentiment_df = pd.read_csv('SentimentDict.csv')
positives_set = set(stentiment_df['positive'])
negatives_set = set(stentiment_df['negative'])
not_set = set(stentiment_df['not'])

def SetDgree(s,d):
    for word in stentiment_df[s]:
        degree_dict[word] = d

def OpenSentimentDict():

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

def sentiment_analysis(sum):
    if sum > 0:
        return 1
    elif sum == 0:
        return 0
    else:
        return -1

for link in linkings:
    MobvieTitle(link)
    sleep(1)


for linkMoreLook in LinkMoreLook:
    inputUserCommentLink(linkMoreLook)


for MaxLink in MaxCommentLink:
    UserComment(MaxLink,j)
    j += 1




GoodComment = []
BadComment = []
Normal = []
for x in range(0, len(MovieTitle)):
    One = 0
    Zero = 0
    Negative = 0
    index = Comment.index(MovieTitle[x])+1
    if x == len(MovieTitle)-1:
        while index < len(Comment):
            Score = analyze(Comment[index])
            Score = sentiment_analysis(Score)
            if Score == 1:
                One += 1
            elif Score == 0:
                Zero += 1
            else:
                Negative += 1

            index +=1
    else:
        while index < Comment.index(MovieTitle[x+1]):
            Score = analyze(Comment[index])
            Score = sentiment_analysis(Score)
            if Score == 1:
                One += 1
            elif Score == 0:
                Zero += 1
            else:
                Negative += 1
            index +=1
    GoodComment.append(One)
    BadComment.append(Negative)
    Normal.append(Zero)

df =pd.DataFrame({"Chinese Title":MovieTitle,"English Title":MovieEngTitle,"Satisfaction":Satisfaction
    ,"Expection":Expect,"Good":GoodComment,"Bad":BadComment,"Normal":Normal})

writer = pd.ExcelWriter("YahooMovie.xlsx",engine="xlsxwriter")
df.to_excel(writer,index=False,sheet_name='sheet1')
writer.save()


