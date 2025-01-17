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
    '1126934135224009636'  # 可以根據需求添加其他用戶
]

@app.route("/")
def hello():
    return "Hello, this is your bot!"

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

    # 回應用戶說的內容
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='您說的是: ' + user_message)
    )

    if user_message == "序號兌換":
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
        response_text = "兌換結果: "
        for code in codelist:
            for user in user_list:
                result = exchange.fetch(user, code).filter()
                response_text += f"{code} - {result} / "  # 结果连在一起，以 / 分隔
                time.sleep(0.5)  # 延遲以避免伺服器過載

        # 移除最後的 " / "
        response_text = response_text.rstrip(" / ")

        # 回應用戶兌換結果
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=response_text)
        )

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
