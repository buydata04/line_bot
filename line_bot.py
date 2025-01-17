import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

# 必須設置為你的Channel Access Token 和 Channel Secret
LINE_CHANNEL_ACCESS_TOKEN = "yKpXw7OFwbqJxxFADaOPb4Kdii9JIcvlzXGJnmwFttMUfVF5+2GAkSiu9mANnchPy5KbBGPEJdNfQbkBiT5j5Q/Jq1GPLoK9iIx1n20CU9uG3Rqlk9nez71k5lIi1zLkjYOG8ZJcsCZoEvrVZWq3FQdB04t89/1O/w1cDnyilFU="
LINE_CHANNEL_SECRET = "2a5ea71857e45cc5dcb325641cf0a6a9"

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
    # 確保請求的簽名是有效的
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

# 定義當用戶傳送文字訊息時，機器人的回應
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='你說了: ' + text)
    )

if __name__ == "__main__":
    # 使用 Heroku 提供的 $PORT 來綁定服務
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
