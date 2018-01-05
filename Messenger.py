import json
import requests
from Config import PAGE_ACCESS_TOKEN

class MyMessenger:
    def __init__(self):
        self.type='null'
        self.txt=''
        self.button=[]
    def setText(self,text):
        if self.type=='null':
            self.type='text'
        self.txt=text
    def addURL(self,title,url):
        self.type='button'
        self.button.append({
            "type":"web_url",
            "url":url,
            "title":title,
            "webview_height_ratio": "full",
            "messenger_extensions": True,
            "fallback_url": "https://petersfancyapparel.com/fallback"
        })
    def addPostback(self,title,payload):
        self.type='button'
        self.button.append({
            "type": "postback",
            "title": title,
            "payload": payload
        })
    def addPhone(self,title,phone):
        self.type='button'
        self.button.append({
            "type":"phone_number",
            "title":title,
            "payload":phone
         })
    def clear(self):
        self.txt=""
        self.type='null'
        self.button=[]
    def makeMessage(self):
        if self.type=='text':
            return {'text':self.txt}
        elif self.type=='button':
            return {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "button",
                        "text": self.txt,
                        "buttons": self.button
                    }
                }
            }

    def send(self,uid):
        print("sending message to {recipient}: {text}".format(recipient=uid, text=self.txt))
        params = {
            "access_token": PAGE_ACCESS_TOKEN
        }
        headers = {
            "Content-Type": "application/json"
        }
        data = json.dumps({
            "recipient": {
                "id": uid
            },
            "message":self.makeMessage()
        })
        r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
        if r.status_code != 200:
            print(r.status_code)
            print(r.text)
        self.clear()

