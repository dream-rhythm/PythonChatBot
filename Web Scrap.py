from urllib.request import urlopen   #for load web page
from bs4 import BeautifulSoup        #for analysis web page
import time                          #for wait
import re                            #for anaysis string

class WebScrap:
    def __init__(self):
        self.allData=[]
    def removeSpace(self,txt):
        return txt.replace(' ','').replace('\n','')
    def getYahoo(self):
        for pageIndex in range(1,7,1):
            html = urlopen('https://movies.yahoo.com.tw/movie_intheaters.html?page='+str(pageIndex))
            bsobj = BeautifulSoup(html, "lxml")
            blocks = bsobj.find_all('div',{"class":"release_info_text"})
            for ele in blocks:
                movieData={}
                movieData['name_zh']=self.removeSpace(ele.a.get_text())
                movieData['name_eng']=self.removeSpace(ele.find_all('a')[1].get_text())
                movieData['href']=ele.a.get('href')
                movieData['want']=ele.find_all('div',{'class':'leveltext'})[0].span.get_text()
                movieData['star']=ele.find_all('div',{'class':'leveltext starwithnum'})[0].span.get('data-num')
                html = urlopen(ele['href'])
                bsobj = BeautifulSoup(html, 'lxml')
                movieData['info']=bsobj.find_all('div', {'class': 'gray_infobox_inner'})[0].span.get_text()
                self.allData.append(movieData)
        print(self.allData)


if __name__ =='__main__':
    obj = WebScrap()
    obj.getYahoo()