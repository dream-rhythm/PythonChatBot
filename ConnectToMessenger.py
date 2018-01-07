from flask import Flask,request
from Config import WEB_HOOK_TOKEN
from ClientHandler import *

app = Flask(__name__)

clientHandler =ClientHandler()

@app.route("/")
def verify():
   if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
       if not request.args.get("hub.verify_token") == WEB_HOOK_TOKEN:
           return "Verification token mismatch", 403
       return request.args["hub.challenge"], 200
   return "Hello world", 200

@app.route("/")
def hello():
    return "Hello World!"

@app.route('/', methods=['POST'])
def webhook():
   global clientHandler
   data = request.get_json()
   print(data)
   if data["object"] == "page":
       for entry in data["entry"]:
           for messaging_event in entry["messaging"]:
               if messaging_event.get("message"):
                   message = messaging_event['message']
                   sender_id = messaging_event["sender"]["id"]
                   if 'text' in message:
                       message_text = message["text"]
                       print(message_text)
                       clientHandler.setMessage(sender_id,message_text)
                       clientHandler.ClientRun(sender_id)
                   elif 'attachments' in message:
                       for attachment in message['attachments']:
                           if attachment['type'] == 'location':
                               print(attachment['payload']['coordinates']['lat'],attachment['payload']['coordinates']['long'])
                               clientHandler.setLocation(sender_id,[attachment['payload']['coordinates']['lat'],attachment['payload']['coordinates']['long']])
                               clientHandler.setMessage(sender_id,'查最近的電影院')
                               clientHandler.ClientRun(sender_id)
               elif messaging_event.get('postback'):
                   message = messaging_event['postback']
                   sender_id = messaging_event["sender"]["id"]
                   print('psotTitle=',message['title'],'payload=',message['payload'])
                   clientHandler.setMessage(sender_id,message['payload'])
                   clientHandler.ClientRun(sender_id)
   return "ok", 200


app.run(host="localhost",port=5000)