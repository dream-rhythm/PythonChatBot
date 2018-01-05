import googlemaps
import csv
from datetime import datetime

gmaps = googlemaps.Client(key='AIzaSyCvmftDhP4yEN-as8P7pYiT-fwwIjpRhpI')

# Geocoding an address
#geocode_result = gmaps.geocode('高雄市苓雅區三多四路21號13樓')[0]["geometry"]["location"]
#for ele in geocode_result:
#    print(ele,"=",geocode_result[ele])

class MovieTheater:
    def __init__(self):
        self.vieshow={"台北信義威秀影城":{"addr":"台北市信義區松壽路20號","phone":"(02) 8780-5566"},
                      "台北京站威秀影城":{"addr":"台北市大同區市民大道一段209號5樓","phone":"(02) 2552-5511"},
                      "台北日新威秀影城":{"addr":"台北市萬華區武昌街二段87號","phone":"(02) 2331-5256"},
                      "板橋大遠百威秀影城":{"addr":"新北市板橋區新站路28號10樓","phone":"(02) 7738-6608"},
                      "林口MITSUI OUTLET PARK威秀影城":{"addr":"新北市林口區文化三路一段356號3樓","phone":"(02) 2606-8099"},
                      "新竹大遠百威秀影城":{"addr":"新竹市西大路323號8樓","phone":"新竹市西大路323號8樓"},
                      "新竹巨城威秀影城":{"addr":"新竹市民權路176號4樓之3","phone":"(03) 534-6999"},
                      "頭份尚順威秀影城":{"addr":"苗栗縣頭份鎮中央路105號7樓","phone":"(037) 686-866"},
                      "台中大遠百威秀影城":{"addr":"台中市西屯區台灣大道三段251號13樓","phone":"(04) 2258-8511"},
                      "台中TIGER CITY威秀影城":{"addr":"台中市西屯區河南路三段120-1號4樓","phone":"(04) 3606-5566"},
                      "台南大遠百威秀影城":{"addr":"台南市公園路60號5樓","phone":"(06) 600-5566"},
                      "台南南紡威秀影城":{"addr":"台南市東區中華東路一段366號5樓","phone":"(06) 237-2255"},
                      "高雄大遠百威秀影城":{"addr":"高雄市苓雅區三多四路21號13樓 ","phone":"(07) 334-5566"}}
        for ele in self.vieshow:
            self.vieshow[ele]["loc"]=self.getLoc(self.vieshow[ele]["addr"])
        with open('movietheater.csv', 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            for name in self.vieshow:
                data=[name,self.vieshow[name]["addr"],self.vieshow[name]["phone"],self.vieshow[name]["loc"]]
                csv_writer.writerow(data)
        csv_file.close()

    def getLoc(self,addr):
        global gmaps
        loc = gmaps.geocode(addr)[0]["geometry"]["location"]
        loc = [loc['lat'],loc['lng']]
        return loc
a = MovieTheater()