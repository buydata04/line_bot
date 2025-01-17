import os
import time
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from findcode import Findcode
from exchange import Exchange
import logging

# 設定日志顯示級別
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

app = Flask(__name__)

# 必須設置為你的Channel Access Token 和 Channel Secret
LINE_CHANNEL_ACCESS_TOKEN = "yKpXw7OFwbqJxxFADaOPb4Kdii9JIcvlzXGJnmwFttMUfVF5+2GAkSiu9mANnchPy5KbBGPEJdNfQbkBiT5j5Q/Jq1GPLoK9iIx1n20CU9uG3Rqlk9nez71k5lIi1zLkjYOG8ZJcsCZoEvrVZWq3FQdB04t89/1O/w1cDnyilFU="
LINE_CHANNEL_SECRET = "2a5ea71857e45cc5dcb325641cf0a6a9"

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# 使用者帳號
user_list = [
    '1126934135224009636',
    '1126934187638915729',
    '1126934135108928409',
    '1126934114860796869'
]

@app.route("/")
def hello():
    return "嗨, 我是機器人唷!"

@app.route("/callback", methods=['POST'])
def callback():
    # 取得 LINE 傳來的簽名和請求體
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        # 處理請求
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

# 設定訊息回應邏輯
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 獲取用戶的訊息
    user_message = event.message.text.strip()

    if user_message.lower() == "兌換序號":
        # 抓取序號
        findcode = Findcode()
        codelist = findcode.fetch().filter()
        if not codelist:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="無法獲取任何序號")
            )
            return

        # 開始兌換序號
        exchange = Exchange()
        response_text = ""
        for code in codelist:
            for user in user_list:
                result = exchange.fetch(user, code).filter()
                response_text += f"序號: {code} - 兌換結果: {result}\n"
                time.sleep(0.5)  # 延遲以避免伺服器過載

        # 回應用戶兌換結果
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=response_text)
        )
    else:
        # 如果用戶發送的訊息不是 "兌換序號"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="請輸入 '兌換序號' 以開始兌換")
        )

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
