import os
from datetime import datetime

from flask import Flask, abort, request

# https://github.com/line/line-bot-sdk-python
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, LocationSendMessage, ImageMessage, ImageSendMessage
import pygsheets
#Open Google Sheets
gc = pygsheets.authorize(service_file='googlesheet.json')
survey_url = 'https://docs.google.com/spreadsheets/d/1GqyfaeKiqDVV8UWpLBh_DwpObIDEFPihG9aX2H7f4fw/'
sh = gc.open_by_url(survey_url)

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ.get("CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.environ.get("CHANNEL_SECRET"))


@app.route("/", methods=["GET", "POST"])
def callback():

    if request.method == "GET":
        return "Hello Heroku"
    if request.method == "POST":
        signature = request.headers["X-Line-Signature"]
        body = request.get_data(as_text=True)

        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            abort(400)

        return "OK"


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    get_message = event.message.text

    if isinstance(event.message, TextMessage):
        if event.message.text == "婚宴資訊":
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text = "婚宴時間: 2021/07/24 （星期六）\n開桌時間: 中午12:00\n進場時間: 上午11:30 \n\n婚禮地點: 台中萊特薇庭宴會廳8F\n\n更詳細的地點位置歡迎點選交通方式喔！")
            )
        elif event.message.text == "交通方式":
            location_message = LocationSendMessage(
                                title='萊特薇庭宴會廳',
                                address='407台中市西屯區龍富路五段396號',
                                latitude=24.160027075487694,
                                longitude=120.62964710009635
            )
            wedding1_img_message = ImageSendMessage(
                original_content_url='https://i.imgur.com/GWob91O.jpg',
                preview_image_url='https://i.imgur.com/GWob91O.jpg'
            )
            wedding2_img_message = ImageSendMessage(
                original_content_url='https://i.imgur.com/hgKOVCN.jpg',
                preview_image_url='https://i.imgur.com/hgKOVCN.jpg'
            )
            line_bot_api.reply_message(
                event.reply_token,
                [location_message, wedding1_img_message, wedding2_img_message]
            )

        else:
            
            finds = sh.find(event.message.text)
            if(len(finds)==0):
                line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text = "抱歉我不懂您的問題，更多婚禮資訊跟功能會在之後推出，如果緊急的話歡迎直接聯絡我們喔！謝謝．")
              )    
            else:
              print(finds[0].row) 
              print(finds[0].col) 

    # # Send To Line
    # reply = TextSendMessage(text=f"我的回話是:{get_message}")
    # line_bot_api.reply_message(event.reply_token, reply)
