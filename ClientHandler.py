from Messenger import MyMessenger
class ClientHandler:
    def __init__(self):
        self.client={}
        self.lastClient=''
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
    def setMsg(self,msg):
        print('run setMsg, ori=',self.nowMsg,' To=',msg)
        self.nowMsg=msg
    def setLocation(self,loc):
        self.location=loc
    def status0(self):
        self.Messenger.setText('Hello!!!\n請問有甚麼需要幫忙的嗎?')
        self.Messenger.addPostback('推薦電影','推薦電影')
        self.Messenger.addPostback('查最近的電影院','查最近的電影院')
        self.Messenger.send()
    def status10(self):
        self.Messenger.setText('請傳送您的位置給我唷!')
        self.Messenger.send()
    def status11(self):
        self.Messenger.setText('查詢中請稍後...')
        self.Messenger.send()

    def findStatus(self):
        if self.nowMsg=='推薦電影':
            self.status=1
        elif self.nowMsg=='查最近的電影院' and self.location==[0,0]:
            self.status=10
        elif self.nowMsg=='查最近的電影院' and self.location!=[0,0]:
            self.status=11

    def printUserStatus(self):
        print('user',self.uid,':status=',self.status,'nowMsg=',self.nowMsg,'loc=',self.location)

    def run(self):
        self.findStatus()
        self.printUserStatus()
        if self.status==0:
            self.status0()
        elif self.status==10:
            self.status10()
        elif self.status==11:
            self.status11()
