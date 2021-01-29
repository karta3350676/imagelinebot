from flask import Flask, request, abort
import os
import random
from ChromeClawer import catchWeb
from Clawer import exchangeRate,getUrl,getPhoto,getpttPhoto

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('Hs8MmV7m+a0YGKZCul6XWPiVw8sd6romkklhWU9QusrEEJlzyP/aqSkawlH0fHHSPN3sJTreY92Q4g+1BmE5bIpdS9EkbUxeauxn5zabRuyb83EVHYOn952hktzkJ/Y48+cNDLqajahJH7VxLCdirAdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('48bcb06ed85d64357a5b50ed6a55a490')

# 監聽所有來自 /callback 的 Post Request
@app.route("/", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print('on Call' + event.message.text)
    word = event.message.text
    word = word.lower()   #將使用者字串全轉成小寫 防止大小寫問題

    if word == 'help':
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='輸入:\n妹子\nPtt\n匯率'))

    elif event.message.text == '匯率':
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='輸入:\n日幣\n美金\n人民幣\n歐元\n英鎊'))

    if word == 'ptt':
        keyword = str(random.randrange(0, 3600, 1))
        ptturl = 'https://www.ptt.cc/bbs/Beauty/index' + keyword + '.html'
        pttimg = getpttPhoto(ptturl)
        print(pttimg)
        if pttimg != '':
            message = ImageSendMessage(
                original_content_url=pttimg,
                preview_image_url=pttimg
            )
            textMessage = TextSendMessage(text=pttimg)
            listMessage = [message, textMessage]
            line_bot_api.reply_message(
                event.reply_token,
                listMessage)

    elif '妹子' in event.message.text:
        imageBase = getUrl('https://ck101.com/beauty/')
        imageUrl = getPhoto(imageBase)
        print('imageUrl' + imageUrl)
        if imageUrl != '':
            message = ImageSendMessage(
                original_content_url=imageUrl,
                preview_image_url=imageUrl
            )
            textMessage = TextSendMessage(text=imageBase)
            listMessage = [message,textMessage]

            line_bot_api.reply_message(
                event.reply_token,
                listMessage)

    else:
        # 返回純文字Message
        outInfo = ''

        # if '日幣' in event.message.text:
        #     outInfo += exchangeRate("JPY")

        if event.message.text == '日幣':
            outInfo += exchangeRate("JPY")

        # if '美金' in event.message.text:
        #     outInfo += exchangeRate("USD")

        if event.message.text == '美金':
            outInfo += exchangeRate("USD")

        # if '人民幣' in event.message.text:
        #     outInfo += exchangeRate("CNY")

        if event.message.text == '人民幣':
            outInfo += exchangeRate("CNY")

        # if '歐元' in event.message.text:
        #     outInfo += exchangeRate("EUR")

        if event.message.text == '歐元':
            outInfo += exchangeRate("EUR")

        # if '英鎊' in event.message.text:
        #     outInfo += exchangeRate("GBP")

        if event.message.text == '英鎊':
            outInfo += exchangeRate("GBP")

        if 'test' in event.message.text:
            result = catchWeb()
            print('main:' + result)
            outInfo += result

        print('outInfo:' + outInfo)

        if outInfo != '':
            message = TextSendMessage(text=outInfo)
            line_bot_api.reply_message(
                event.reply_token,
                message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
