from Messenger import MyMessenger
from MovieTheater import *
from WebScrap import  *
import time
from threading import Thread as thread
movietheater = MovieTheater()
movieInfo = WebScrap()

class ClientHandler:
    def __init__(self):
        self.client={}
        self.lastClient=''
        t1 = thread(target=self.timeoutChecker)
        t1.start()

    def timeoutChecker(self):
        timer = 60
        while True:
            sleep(timer)
            kill=[]
            for ele in self.client:
                if time.time()-self.client[ele].getStartTime()>300:
                    kill.append(ele)
                    print(str(ele)+' is timeout!!!')
            for ele in kill:
                del self.client[ele]

    def newClient(self,uid):
        return Client(uid)
    def printAllClienr(self):
        print(self.client)
    def setMessage(self,uid='',msg=''):
        if uid=='' and self.lastClient!='':
            uid=self.lastClient
        elif uid=='' and self.lastClient=='':
            print('Please setup uid!!!')
            return
        if uid not in self.client:
            self.client[uid]=self.newClient(uid)
        self.client[uid].setMsg(msg)
        self.lastClient=uid

    def setLocation(self,uid='',loc=[0,0]):
        if uid=='' and self.lastClient!='':
            uid=self.lastClient
        elif uid=='' and self.lastClient=='':
            print('Please setup uid!!!')
            return
        if uid not in self.client:
            self.client[uid]=self.newClient(uid)
        self.client[uid].setLocation(loc)

    def ClientRun(self,uid=''):
        if uid=='' and self.lastClient!='':
            uid=self.lastClient
        elif uid=='' and self.lastClient=='':
            print('Please setup uid!!!')
            return
        if uid in self.client:
            self.client[uid].run()
        else:
            print('Can not find user!!!')

class Client:
    def __init__(self,uid):
        self.status=0
        self.uid=uid
        self.nowMsg=''
        self.location=[0,0]
        self.Messenger = MyMessenger(uid)
        self.movieName=""
        self.TheaterName=''
        self.near=[]
        self.place=[0,0,0]
        self.tmp={}
        self.lastStatus=0
        self.timstamp=time.time()
    def getStartTime(self):
        return self.timstamp
    def setMsg(self,msg):
        print('run setMsg, ori=',self.nowMsg,' To=',msg)
        self.timstamp = time.time()
        self.nowMsg=msg

    def setLocation(self,loc):
        self.timstamp = time.time()
        self.location=loc

    def status0(self):
        self.Messenger.setText('Hello!!!\n請問有甚麼需要幫忙的嗎?')
        self.Messenger.addPostback('推薦電影','推薦電影')
        self.Messenger.addPostback('查最近的電影院','查最近的電影院')
        self.Messenger.send()
    def status1(self):
        self.movieName=""
        msg='我推薦你以下五部電影:\n'
        data = movieInfo.getRank(1,5)
        for i in range(1,6,1):
            msg+= str(i)+'.'+str(data[i-1])+'\n'
        msg+='請輸入影片編號'
        self.Messenger.setText(msg)
        self.Messenger.addPostback('換一組')
        self.Messenger.send()

    def status2(self):
        msg='我推薦你以下五部電影:\n'
        data = movieInfo.getRank(6,10)
        for i in range(6,11,1):
            msg+= str(i)+'.'+str(data[i-6])+'\n'
        msg+='請輸入影片編號'
        self.Messenger.setText(msg)
        self.Messenger.addPostback('換一組')
        self.Messenger.send()

    def status3(self):
        msg='我推薦你以下五部電影:\n'
        data = movieInfo.getRank(11,15)
        for i in range(11,16,1):
            msg+= str(i)+'.'+str(data[i-11])+'\n'
        msg+='請輸入影片編號'
        self.Messenger.setText(msg)
        self.Messenger.addPostback('換一組')
        self.Messenger.send()
    def status6(self):
        if self.TheaterName=="":
            name=movieInfo.getRank(int(self.nowMsg),int(self.nowMsg))[0]
        else:
            name = self.tmp['rank'][int(self.nowMsg)-1]
        info = movieInfo.getMovieInfo(name)
        data=[]
        while len(info)>640:
            data.append(info[:600])
            info=info[600:]
        self.movieName=name
        msg='您所選擇的電影是:'+name+'\n以下為該電影的簡介'
        self.Messenger.setText(msg)
        self.Messenger.send()
        for ele in data:
            self.Messenger.setText(ele)
            self.Messenger.send()
        self.Messenger.setText(info)
        self.Messenger.addPostback('我想看')
        self.Messenger.addPostback('換一部')
        self.Messenger.send()

    def status10(self):
        self.Messenger.setText('請傳送您的位置給我唷!')
        self.Messenger.send()

    def status11(self):
        self.Messenger.setText('查詢中請稍後...')
        self.Messenger.send()
        self.near = movietheater.findWhoIsNearToMe(self.location[0],self.location[1])
        if len(self.near)==0:
            self.Messenger.setText('抱歉!\n我在附近找不到電影院...')
            self.Messenger.send()
            self.Messenger.setText('請重新傳送一個位置給我吧')
            self.Messenger.send()
        else:
            self.place=[0,0,0]
            for ele in self.near:
                if ele[1]=='賓':
                    self.place[1]+=1
                elif ele[2]=='新':
                    self.place[2]+=1
                else:
                    self.place[0]+=1
            txt="我在附近找到"+str(len(self.near))+"間電影院\n你想去哪一家呢?"
            print(self.near)
            self.Messenger.setText(txt)
            if self.place[0]:
                self.Messenger.addPostback('華納威秀')
            if self.place[1]:
                self.Messenger.addPostback('國賓影城')
            if self.place[2]:
                self.Messenger.addPostback('新光影城')
            self.Messenger.send()

    def status12(self):
        ans=self.findNearByTheaterType(self.nowMsg)
        txt = "我在附近找到" + str(len(ans)) + "間"+self.nowMsg+"\n你想去哪一家呢?"
        self.Messenger.setText(txt)
        for ele in ans:
            self.Messenger.addPostback(ele)
        self.Messenger.send()

    def status16(self):
        if self.movieName=="":
            self.status=20
            self.run()
        else:
            self.Messenger.setText("場次查詢中...")
            self.Messenger.send()
            #self.TheaterName=self.nowMsg
            movies = movietheater.getMovies(self.TheaterName)
            if self.movieName in movies:
                timetable = movietheater.getTimeTable(self.TheaterName,self.movieName)
                msg='我幫你找到'+str(len(timetable))+'個時段:\n'
                for i in range(1,len(timetable)+1,1):
                    msg+=str(i)+'. '+str(timetable[i-1])+'\n'
                msg+='請問這樣可以嗎?'
                self.Messenger.addPostback('OK')
                self.Messenger.addPostback('換一部電影')
                self.Messenger.addPostback('換一個影城')
                self.Messenger.setText(msg)
                self.Messenger.send()
            else:
                msg="這部電影在這個影城沒有上映欸...\n您要換一部電影嗎?"
                self.Messenger.setText(msg)
                self.Messenger.addPostback('換一部電影')
                self.Messenger.addPostback('換一個影城')
                self.Messenger.send()
    def status17(self):
        msg='感謝您使用此chatbot\n因避免隱私問題故不代訂電影票\n請自行前往官網訂票唷!\n'
        self.Messenger.setText(msg)
        self.Messenger.send()
        info = movietheater.getTheaterInformation(self.TheaterName)
        msg='以下為'+self.TheaterName+'的資訊\n'
        msg+='電話: '+info['phone']+'\n'
        msg+='地址: '+info['addr']+'\n'
        msg+='官網: '+info['url']+'\n'
        self.Messenger.setText(msg)
        self.Messenger.addPostback('重新開始','reset')
        self.Messenger.send()

    def status20(self):
        self.Messenger.setText('電影資訊查詢中...')
        self.Messenger.send()
        if 'rank' not in self.tmp:
            data=movietheater.getMovies(self.TheaterName)
            rank=movieInfo.getRank()
            newRank=[]
            for ele in rank:
                if ele in data:
                    newRank.append(ele)
            self.tmp['rank']=newRank
        if 'rank_index' not in self.tmp:
            self.tmp['rank_index']=0
        msg = '我推薦你以下幾部電影:\n'
        index = self.tmp['rank_index']
        for i in range(self.tmp['rank_index']+1, self.tmp['rank_index']+6, 1):
            if index >=len(self.tmp['rank']):
                index = 0
                break
            msg += str(i) + '.' + str(self.tmp['rank'][index]) + '\n'
            index+=1
        self.tmp['rank_index']=index
        msg += '請輸入影片編號'
        self.Messenger.setText(msg)
        self.Messenger.addPostback('換一組')
        self.Messenger.send()


    def findStatus(self):
        self.lastStatus =self.status
        if self.nowMsg=='reset':
            self.status=0
            self.movieName=""
            self.TheaterName=""
            self.nowMsg=""
            self.tmp={}
            self.location=[0,0]
            self.near=[]
            self.place=[0,0,0]
        elif self.nowMsg=='推薦電影':
            self.status=1
        elif self.status==1 and self.nowMsg.isdigit():
            if 1<=int(self.nowMsg)<=5:
                self.status=6
        elif self.status==1:
            self.status=2
        elif self.status==2 and self.nowMsg.isdigit():
            if 1<=int(self.nowMsg)<=10:
                self.status=6
        elif self.status==2:
            self.status=3
        elif self.status==3 and self.nowMsg.isdigit():
            if 1<=int(self.nowMsg)<=15:
                self.status=6
        elif self.status==3:
            self.status=1
        elif self.status==6:
            if self.nowMsg=='我想看':
                if self.TheaterName!="":
                    self.status=16
                elif self.location==[0,0]:
                    self.status=10
                else:
                    self.status=11
            elif self.nowMsg=='換一部':
                self.status=1
        elif self.nowMsg=='查最近的電影院' and self.location==[0,0]:
            self.status=10
        elif self.nowMsg=='查最近的電影院' and self.location!=[0,0]:
            self.status=11
        elif self.status==11:
            self.tmp={}
            if self.nowMsg=='華納威秀' and self.place[0]==1:
                self.status = 16
                self.nowMsg=self.findNearByTheaterType('華納威秀')[0]
            elif self.nowMsg=='新光影城' and self.place[2]==1:
                self.status = 16
                self.nowMsg = self.findNearByTheaterType('新光影城')[0]
            elif  self.nowMsg=='國賓影城' and self.place[1]==1:
                self.status=16
                self.nowMsg = self.findNearByTheaterType('國賓影城')[0]
            elif self.nowMsg=='華納威秀' and self.place[0]>1:
                self.status =12
            elif self.nowMsg=='新光影城' and self.place[2]>1:
                self.status = 12
            elif  self.nowMsg=='國賓影城' and self.place[1]>1:
                self.status=12
            if self.status==16 and self.movieName=='':
                self.TheaterName=self.nowMsg
                self.status=20
            elif self.status==16:
                self.TheaterName=self.nowMsg
        elif (self.status==12 and self.nowMsg in self.near) :
            self.TheaterName = self.nowMsg
            self.status=16
        elif self.status==16:
            if self.nowMsg=='換一部電影':
                self.status=20
            elif self.nowMsg=='換一個影城':
                self.status=11
            elif self.nowMsg=='OK':
                self.status=17
            else:
                pass
        elif self.status==20:
            if self.nowMsg=='換一組':
                pass
            elif self.nowMsg.isdigit():
                self.status=6

    def findNearByTheaterType(self,TheaterType):
        ans=[]
        if TheaterType=='華納威秀':
            for ele in self.near:
                if ele[1]!='賓' and ele[2]!='新':
                    ans.append(ele)
        elif TheaterType=='國賓影城':
            for ele in self.near:
                if ele[1]=='賓' :
                    ans.append(ele)
        else:
            for ele in self.near:
                if ele[2]=='新':
                    ans.append(ele)
        return ans

    def printUserStatus(self):
        print('user',self.uid,':status=',self.status,'nowMsg=',self.nowMsg,'loc=',self.location)

    def run(self):
        self.findStatus()
        self.printUserStatus()
        if self.status==0:
            self.status0()
        elif self.status==1:
            self.status1()
        elif self.status==2:
            self.status2()
        elif self.status==3:
            self.status3()
        elif self.status==6:
            self.status6()
        elif self.status==10:
            self.status10()
        elif self.status==11:
            self.status11()
        elif self.status==12:
            self.status12()
        elif self.status==16:
            if self.lastStatus==self.status:
                pass
            else:
                self.status16()
        elif self.status==17:
            self.status17()
        elif self.status==20:
            self.status20()