import googlemaps
import csv
from selenium import webdriver
from time import sleep
from urllib.request import urlopen   #for load web page
from bs4 import BeautifulSoup        #for analysis web page


gmaps = googlemaps.Client(key='AIzaSyCvmftDhP4yEN-as8P7pYiT-fwwIjpRhpI')


class MovieTheater:
    def __init__(self):
        f = open('movietheater.csv', 'r')
        csvreader = csv.reader(f)
        self.allData=[]
        self.timetable={}
        for row in csvreader:
            self.allData.append(row)
        f.close()
    def getTheaterInformation(self,theatername):
        ans={}
        for i in range(len(self.allData)):
            if self.allData[i][0]==theatername:
                ans['addr']=self.allData[i][1]
                ans['phone']=self.allData[i][2]
                if i<=12:
                    ans['url']='https://www.vscinemas.com.tw/'
                elif 12<i<=24:
                    ans['url']='http://www.ambassador.com.tw/'
                else:
                    ans['url']='http://www.skcinemas.com/'
                break
        return  ans
    def firstrun(self):
        self.vieshow={"台北信義威秀影城":{"addr":"台北市信義區松壽路20號","phone":"(02) 8780-5566"},
                      "台北京站威秀影城":{"addr":"台北市大同區市民大道一段209號5樓","phone":"(02) 2552-5511"},
                      "台北日新威秀影城":{"addr":"台北市萬華區武昌街二段87號","phone":"(02) 2331-5256"},
                      "板橋大遠百威秀影城":{"addr":"新北市板橋區新站路28號10樓","phone":"(02) 7738-6608"},
                      "林口MITSUI OUTLET PARK威秀影城":{"addr":"新北市林口區文化三路一段356號3樓","phone":"(02) 2606-8099"},
                      "新竹大遠百威秀影城":{"addr":"新竹市西大路323號8樓","phone":"(03) 524-1166"},
                      "新竹巨城威秀影城":{"addr":"新竹市民權路176號4樓之3","phone":"(03) 534-6999"},
                      "頭份尚順威秀影城":{"addr":"苗栗縣頭份鎮中央路105號7樓","phone":"(037) 686-866"},
                      "台中大遠百威秀影城":{"addr":"台中市西屯區台灣大道三段251號13樓","phone":"(04) 2258-8511"},
                      "台中TIGER CITY威秀影城":{"addr":"台中市西屯區河南路三段120-1號4樓","phone":"(04) 3606-5566"},
                      "台南大遠百威秀影城":{"addr":"台南市公園路60號5樓","phone":"(06) 600-5566"},
                      "台南南紡威秀影城":{"addr":"台南市東區中華東路一段366號5樓","phone":"(06) 237-2255"},
                      "高雄大遠百威秀影城":{"addr":"高雄市苓雅區三多四路21號13樓 ","phone":"(07) 334-5566"}}
        self.ambassador={
            "國賓大戲院":{"addr":"台北市成都路88號","phone":" 02-2361-1223"},
            "國賓影城＠台北微風廣場":{"addr":"台北市復興南路一段39號7樓","phone":"02-8772-1234"},
            "國賓影城＠台北長春廣場": {"addr": "台北市中山區長春路176號", "phone": " 02-2515-5757"},
            "國賓影城@中和環球購物中心": {"addr": "新北市中和區中山路三段122號4樓", "phone": "02-2226-8088"},
            "國賓影城@新莊晶冠廣場": {"addr": "新北市新莊區五工路66號3、4F", "phone": "02-8521-6517"},
            "國賓影城@林口昕境廣場": {"addr": " 新北市林口區文化三路一段402巷2號4F", "phone": "02-2608-0011"},
            "國賓影城@八德廣豐新天地": {"addr": "桃園市八德區介壽路一段728號3F", "phone": " 03-218-2898"},
            "國賓影城@台南國賓廣場": {"addr": "台南市中華東路一段66號", "phone": "06-234-7166"},
            "國賓影城@高雄義大世界": {"addr": "高雄市大樹區學城路一段12號3F", "phone": "07-656-8368"},
            "國賓影城@高雄大魯閣草衙道": {"addr": "高雄市前鎮區中山四路100號3樓", "phone": "07-793-3611"},
            "國賓影城@屏東環球購物中心": {"addr": "屏東縣屏東市仁愛路90號6樓", "phone": "08-766-2128"},
            "國賓影城@金門昇恆昌金湖廣場": {"addr": "金門縣金湖鎮太湖路二段198號6樓", "phone": "082-330-287"}
        }
        self.ShinKong={
            "台北新光影城": {"addr": "台北市萬華區西寧南路36號4樓", "phone": "(02)2314-6668"},
            "台中新光影城": {"addr": "台中市西屯區台灣大道三段301號", "phone": " 	(04)2258-9911"},
            "台南新光影城": {"addr": "台南市中西區西門路一段658號", "phone": "(06)303-1260 "}
        }
        for ele in self.vieshow:
            self.vieshow[ele]["loc"]=self.getLoc(self.vieshow[ele]["addr"])
        for ele in self.ambassador:
            self.ambassador[ele]["loc"]=self.getLoc(self.ambassador[ele]["addr"])
        for ele in self.ShinKong:
            self.ShinKong[ele]["loc"]=self.getLoc(self.ShinKong[ele]["addr"])

        with open('movietheater.csv', 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            for name in self.vieshow:
                data=[name,self.vieshow[name]["addr"],self.vieshow[name]["phone"],self.vieshow[name]["loc"][0],self.vieshow[name]["loc"][1]]
                csv_writer.writerow(data)
            for name in self.ambassador:
                data=[name,self.ambassador[name]["addr"],self.ambassador[name]["phone"],self.ambassador[name]["loc"][0],self.ambassador[name]["loc"][1]]
                csv_writer.writerow(data)
            for name in self.ShinKong:
                data=[name,self.ShinKong[name]["addr"],self.ShinKong[name]["phone"],self.ShinKong[name]["loc"][0],self.ShinKong[name]["loc"][1]]
                csv_writer.writerow(data)
        csv_file.close()

    def getLoc(self,addr):
        global gmaps
        loc = gmaps.geocode(addr)[0]["geometry"]["location"]
        loc = [loc['lat'],loc['lng']]
        return loc
    def get_length(self,x1,y1,x2,y2):
        x1=float(x1)
        x2=float(x2)
        y1=float(y1)
        y2=float(y2)
        return ((x1-x2)**2+(y1-y2)**2)**(1/2)*111.1
    def findWhoIsNearToMe(self,lat,lng):
        ans=[]
        for ele in self.allData:
            if self.get_length(lat,lng,ele[3],ele[4])<=10:
                ans.append(ele[0])
        return ans

    def getMovies(self,TheaterName):
        if TheaterName[1]=='賓':#國賓
            table = self.getAmbassador(TheaterName)
        elif TheaterName[2]=='新':#新光
            table = self.getSkcinems(TheaterName)
        else:
            table = self.getViewshow(TheaterName)
        self.timetable[TheaterName]=table
        arr = []
        for ele in table:
            arr.append(ele)
        return arr
        #吃一個電影院的名稱(上面定義的那些)
        #以陣列回傳該影城現正上映的電影
        #因網頁使用ajex動態獲取資料
        #故須使用webdriver呼叫Firefox出來用

    def getTimeTable(self,TheaterName, Movie):
        if TheaterName not in self.timetable:
            self.getMovies(TheaterName)
        return self.timetable[TheaterName][Movie]

    def Ambassador_paser(self,arr):
        movie={}
        status=0
        name=""
        for ele in arr:
            if status==0:#get chinese name
                name=ele
                movie[name] = []
                status=1
            elif status==1:#get eng name
                status=2
            elif status==2:#get actor
                status=3
            elif status==3:#get on air time
                status=4
            elif status==4:#get theater type
                status=5
            elif status==5:#get theater inffo
                status=6
            elif status==6:
                movie[name].extend(ele.split('|')[1:])
                status=7
            elif status==7:
                if ele[0]=='(':
                    status=5
                else:
                    name=ele
                    movie[ele]=[]
                    status=1
        return  movie
    def getAmbassador(self,theatername):
        theaterID={
            "國賓大戲院":"84b87b82-b936-4a39-b91f-e88328d33b4e",
            "國賓影城@台北微風廣場":"5c2d4697-7f54-4955-800c-7b3ad782582c",
            "國賓影城@台北長春廣場":"453b2966-f7c2-44a9-b2eb-687493855d0e",
            "國賓影城@中和環球購物中心":"357633f4-36a4-428d-8ac8-dee3428a5919",
            "國賓影城@林口昕境廣場":"9383c5fa-b4f3-4ba8-ba7a-c25c7df95fd0",
            "國賓影城@新莊晶冠廣場":"3301d822-b385-4aa8-a9eb-aa59d58e95c9",
            "國賓影城@八德廣豐新天地":"8fda9934-73d4-4c14-b1c4-386c2b81045c",
            "國賓影城@台南國賓廣場":"ace1fe19-3d7d-4b7c-8fbe-04897cbed08c",
            "國賓影城@高雄義大世界":"ec07626b-b382-474e-be39-ad45eac5cd1c",
            "國賓影城@高雄大魯閣草衙道":"f760950a-94b6-4e04-9573-831ed7283c5c",
            "國賓影城@屏東環球購物中心":"41aae717-4464-49f4-ac26-fec2d16acbd6",
            "國賓影城@金門昇恆昌金湖廣場":"65db51ce-3ad5-48d8-8e32-7e872e56aa4a"
        }
        driver = webdriver.Firefox()
        driver.get("http://www.ambassador.com.tw/showtime_list.html?theaterid=" + theaterID[theatername])
        sleep(1)
        data = driver.find_element_by_xpath('//*[@id="mt-main-movie-list-view"]')
        info = data.text.split('\n')
        driver.close()
        return self.Ambassador_paser(info)

    def Viewshow_timeCheaker(self,str):
        str=str.split(':')
        if len(str)!=2:
            return False
        if str[1][-4:]=='(隔日)':
            str[1]=str[1][:-4]
        if str[0].isdigit()==False or str[1].isdigit()==False:
            return False
        if int(str[0]) in range(24) and int(str[1]) in range(60):
            return True
        return False
    def Viewshow_paser(self,arr):
        movie = {}
        status=0
        name=""
        for ele in arr:
            if status==0:#get chinese name
                movie[ele]=[]
                name=ele
                status=1
            elif status==1:#get eng name
                status=2
            elif status==2:#get type
                if ele in ['IMAX 3D','數位']:
                    pass
                elif self.Viewshow_timeCheaker(ele):
                    movie[name].append(ele)
                else:
                    name=ele
                    movie[name]=[]
                    status=1
        return movie
    def getViewshow(self,theatername):
        theaterID={"台北信義威秀影城":"1",
                   "台北京站威秀影城":"2",
                   "台北日新威秀影城":"3",
                   "板橋大遠百威秀影城":"4",
                   "林口MITSUI OUTLET PARK威秀影城":"5",
                   "新竹大遠百威秀影城":"7",
                   "新竹巨城威秀影城":"9",
                   "頭份尚順威秀影城":"10",
                   "台中大遠百威秀影城":"11",
                   "台中TIGER CITY威秀影城":"12",
                   "台南大遠百威秀影城":"15",
                   "台南南紡威秀影城":"16",
                   "高雄大遠百威秀影城":"18"}
        driver = webdriver.Firefox()
        driver.get("https://www.vscinemas.com.tw/theater/detail.aspx?id="+theaterID[theatername])
        sleep(1)
        data = driver.find_element_by_xpath('//html/body/div[17]')
        info = data.text.split('\n')[1:]
        driver.close()
        return self.Viewshow_paser(info)

    def getSkcinems(self,theatername):
        driver = webdriver.Firefox()
        driver.get('http://www.skcinemas.com/MovieList.aspx')
        if theatername=='台北新光影城':
            but = driver.find_element_by_xpath('//*[@id="ctl00_ASPxMenu1_DXI2_I"]')
            but.click()
        elif theatername=='台南新光影城':
            but = driver.find_element_by_xpath('//*[@id="ctl00_ASPxMenu1_DXI1_I"]')
            but.click()
        bsobj = BeautifulSoup(driver.page_source, "lxml")
        blocks = bsobj.find_all('td',{'class':'dxdvItem'})
        if theatername=='台中新光影城':
            but=driver.find_element_by_xpath('/html/body/form/div[3]/div/div/div[2]/table/tbody/tr[1]/td[2]/table/tbody/tr/td/table/tbody/tr[3]/td/div/a')
            but.click()
            bsobj = BeautifulSoup(driver.page_source, "lxml")
            blocks.extend(bsobj.find_all('td', {'class': 'dxdvItem'}))
        movies ={}
        for ele in blocks:
            href=ele.find_all('a')[0].get('href')
            driver.get('http://www.skcinemas.com/'+href)
            times = driver.find_element_by_xpath('/html/body/form/div[3]/div/div/div[2]/div[3]/div/table/tbody/tr[2]').text
            name = driver.find_element_by_xpath('/html/body/form/div[3]/div/div/div[1]/div[1]/div[3]/table/tbody/tr[1]/td/span').text
            movies[name]=times.split(' ')
        driver.close()
        return movies

if __name__ =='__main__':
    a = MovieTheater()
    #a.getSkcinems('台北新光影城')
    print(a.getMovies('台中新光影城'))
    print(a.getTimeTable('台中新光影城','血觀音'))
    #print(a.getAmbassador('國賓大戲院'))