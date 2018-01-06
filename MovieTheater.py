import googlemaps
import csv

gmaps = googlemaps.Client(key='AIzaSyCvmftDhP4yEN-as8P7pYiT-fwwIjpRhpI')


class MovieTheater:
    def __init__(self):
        f = open('movietheater.csv', 'r')
        csvreader = csv.reader(f)
        self.allData=[]
        for row in csvreader:
            self.allData.append(row)
        f.close()

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

#a = MovieTheater()
#a.firstrun()