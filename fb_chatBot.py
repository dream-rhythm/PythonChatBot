import requests
from flask import Flask,request
import json
import pandas as pd
#import statsmodels.api as sm
import facebook

PAGE_ACCESS_TOKEN = 'EAAOJbhlLZA3ABADcSKZCSniBR7YYgVThnGZCSEdaZAeXa2FcfuS5qCyeoK8iqTnxN29vj1q58d2dfBqJcrgRWVDR3MZA5fp1739gd0B6oxE1B6r8vA9Bct6PtviLAJRfx34Equli3YbUKZAdyhoyZB4IUOgvautU6dllDwNpseKpM1qU7MhvpYf'
app = Flask(__name__)

@app.route("/")
#def hello():
    #return "Hello World!"



#app = Flask(__name__)

#PAGE_ACCESS_TOKEN = 'XXX'


@app.route("/")
def verify():
   if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
       if not request.args.get("hub.verify_token") == 'hi':
           return "Verification token mismatch", 403
       return request.args["hub.challenge"], 200
   return "Hello world", 200

@app.route('/', methods=['POST'])
def webhook():
   data = request.get_json()
   print(data)
   if data["object"] == "page":
       for entry in data["entry"]:
           for messaging_event in entry["messaging"]:
               if messaging_event.get("message"):
                   message = messaging_event['message']
                   sender_id = messaging_event["sender"]["id"]
                   recipient_id = messaging_event["recipient"]["id"]

                   if 'text' in message:
                       if message['text'] == 'hi':
                           message["text"] = "你好，我可以幫你介紹電影"
                           message_text = message["text"]
                           print(message_text)
                           send_message(sender_id, message_text)
                       else:
                           message_text = message["text"]
                           send_message(sender_id,message_text)
                   elif 'attachments' in message:
                       for attachment in message['attachments']:
                           if attachment['type'] == 'location':
                               print(attachment['payload']['coordinates']['lat'],attachment['payload']['coordinates']['long'])
                               lat = str(attachment['payload']['coordinates']['lat'])
                               long = str(attachment['payload']['coordinates']['long'])
                               foods = recommend_taking_about_food(lat,long,'一中')
                               msg = '我推薦以下商店，因為口碑最好\n'+'\n'.join(foods)
                               send_message(sender_id, msg)

   return "ok", 200


def send_message(recipient_id, message_text):
   print("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

   params = {
       "access_token": PAGE_ACCESS_TOKEN
   }
   headers = {
       "Content-Type": "application/json"
   }
   data = json.dumps({
       "recipient": {
           "id": recipient_id
       },
       "message": {
           "text": message_text
       }
   })
   r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
   if r.status_code != 200:
       print(r.status_code)
       print(r.text)

def get_fb_page(lat,long,keyword):
    token = 'EAACEdEose0cBAD0KjZBayqpoHzrZAZBUVVvYYWPhKhDZBzv7WKXOx4g4WZB8heyOANlK3XiJvIMXvmgyb10VxTl4Efet80Ie4FIrrluvjbv1yilv05VHSbyRZAgeM5gbLhK84V3J3qxztlVzdNBsHD12bnGbSJWaDmcRGJf5TJRmCsGli8M8k8GuiWq1RJbYwSAXZBAFSwOCQZDZD'

    fields = [
        'id',
        'name',
        'about',
        'category',
        'checkins',
        'fan_count',
        'talking_about_count',
        'price_range',
        'is_always_open',
    ]
    fields = ','.join(fields)

    exclude = [
        'Apartment & Condo Building',
        'Home',
        'Hotel',
        'Hotel & Lodging',
        'Inn',
        'Men\'s Clothing Store',
        'Night Market',
        'Parking Garage / Lot',
        'Performance & Event Venue',
        'Real Estate',
        'Region',
        'Shopping & Retail',
        'Tour Agency',
        'Vacation Home Rental',
        'Christian Church',
        'Art',
        'Gym/Physical Fitness Center',
        'Recreation Center',
        'Karaoke',
        'Costume Shop',
        'Hair Salon',
        'Mobile Phone Shop',
        'Beauty Supply Store',
        'Nail Salon',
        'Women\'s Clothing Store',
        'Makeup Artist',
        'Nail Salon',
        'Clothing Store',
        'Shopping District',
        'Beauty Salon',
        'Tour Guide',
    ]

    graph = facebook.GraphAPI(access_token=token, version='2.10')
    fc = graph.search(type='place', q=keyword, center=lat+','+long, distance=1000, fields=fields)

    pagelist = []

    while True:
        if 'data' in fc:
            pagelist.extend(fc['data'])
        else:
            break
        if 'paging' in fc:
            if 'next' in fc['paging']:
                fc = requests.get(fc['paging']['next']).json()
        else:
            break

    pagelist = [page for page in pagelist if page['is_always_open'] != True]
    pagelist = [page for page in pagelist if page['category'] not in exclude]
    pagelist = [page for page in pagelist if page['checkins'] > 500]
    pagelist = [page for page in pagelist if page['fan_count'] > 500]

    fcdata = pd.DataFrame(pagelist)
    return fcdata

def recommend_taking_about_food(lat,long,keyword):
   fb_data = get_fb_page(lat,long, keyword)
   recommend = max(fb_data['checkins'])

   return recommend


#app.run()
