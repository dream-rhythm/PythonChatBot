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
                movieData['star']=float(ele.find_all('div',{'class':'leveltext starwithnum'})[0].span.get('data-num'))
                html = urlopen(ele['href'])
                bsobj = BeautifulSoup(html, 'lxml')
                movieData['info']=bsobj.find_all('div', {'class': 'gray_infobox_inner'})[0].span.get_text()
                self.allData.append(movieData)
        print(self.allData)
    def getSk(self):
        html = urlopen('http://www.skcinemas.com/MovieList.aspx')

        bsobj = BeautifulSoup(html, "lxml")

        blocks = bsobj.find_all('td', {"class": "dxdvItem"})
        for ele in blocks:
            a = ''
            movieData={}
            detail = ''
            movieData['name_zh']=self.removeSpace(ele.find('div',style="font-family: 微軟正黑體; font-weight: bold; font-size: 10pt; color: #003b70;width:125px;height:36px;text-align:center;overflow:hidden;vertical-align:top;").get_text())
            movieData['name_eng']=self.removeSpace(ele.find('div',style="font-family: 微軟正黑體; font-weight: bold; font-size: 8pt; color: #003b70;width:125px;text-align:center;height:15px;overflow:hidden;").get_text())
            movieData['movie_date']=self.removeSpace(ele.find('div',style="font-family: 微軟正黑體; font-weight: bold; font-size: 8pt; width:125px;text-align:center;margin-top:10px;color:black;").get_text())
            
            a = ele.find(a,href = True)
            movieData['movie_href']=a['href']
            detail = urlopen("http://www.skcinemas.com/"+a['href'])
            bsobj = BeautifulSoup(detail, "lxml")
            target = bsobj.find('div',style = "border: 2px solid #000000; padding:8px;margin:-4px 0 0 0;")
            movieData['movie_detail']=target.find_all('div',text = True) 
            self.allData.append(movieData)
        print(self.allData)
    def getVs(self):
        html = urlopen('https://www.vscinemas.com.tw/film/index.aspx')

        bsobj = BeautifulSoup(html, "lxml")

        blocks = bsobj.find_all('section',{"class" : "infoArea"})
        detail = bsobj.find_all('figure',style = "height: 279px;")
        for ele in blocks:
            movieData={}
            movieData['name_zh']=self.removeSpace(ele.find('h2',text = True).get_text())
            movieData['name_eng']=self.removeSpace(ele.find('h3',text = True).get_text())
            movieData['movie_date']=self.removeSpace(ele.find('time',text = True).get_text())
            self.allData.append(movieData)
            a = ''
            detail = ''
            a = ele.find(a,href = True)
            movieData['movie_href']=a['href']
            detail = urlopen("https://www.vscinemas.com.tw/film/"+a['href'])
            bsobj = BeautifulSoup(detail, "lxml")
            target = bsobj.find('div',{"class":"bbsArticle"})
            movieData['movie_detail']=target.find_all('p',text = True) 
            self.allData.append(movieData)
        print(self.allData)
if __name__ =='新光':
    obj = WebScrap()
    obj.getSk()
if __name__ =='威秀':
    obj = WebScrap()
    obj.getVs()
if __name__ =='Yahooˇ電影':
    obj = WebScrap()
    obj.getYahoo()