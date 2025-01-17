import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from change_main import run_exchange  # 引入執行兌換的函數

app = Flask(__name__)

# 必須設置為你的Channel Access Token 和 Channel Secret
LINE_CHANNEL_ACCESS_TOKEN = "yKpXw7OFwbqJxxFADaOPb4Kdii9JIcvlzXGJnmwFttMUfVF5+2GAkSiu9mANnchPy5KbBGPEJdNfQbkBiT5j5Q/Jq1GPLoK9iIx1n20CU9uG3Rqlk9nez71k5lIi1zLkjYOG8ZJcsCZoEvrVZWq3FQdB04t89/1O/w1cDnyilFU="
LINE_CHANNEL_SECRET = "2a5ea71857e45cc5dcb325641cf0a6a9"

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

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
        abort(400)  # 如果簽名驗證失敗，返回 400

    return 'OK'

# 設定訊息回應邏輯
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    try:
        if event.message.text == "序號兌換":
            # 呼叫 change_main.py 的 run_exchange 函數，取得兌換結果
            result = run_exchange()
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=result)
            )
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='您說的是: ' + event.message.text)
            )
    except Exception as e:
        # 捕捉並處理錯誤，返回一個通用的錯誤訊息
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"出現錯誤: {str(e)}")
        )
        logging.error(f"Error occurred: {str(e)}")

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
