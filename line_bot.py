import os
from flask import Flask, request, abort
from line_bot_sdk import LineBotApi, WebhookHandler
from line_bot_sdk.exceptions import InvalidSignatureError
from line_bot_sdk.models import MessageEvent, TextMessage

app = Flask(__name__)

# 必須設置為你的Channel Access Token 和 Channel Secret
LINE_CHANNEL_ACCESS_TOKEN = "yKpXw7OFwbqJxxFADaOPb4Kdii9JIcvlzXGJnmwFttMUfVF5+2GAkSiu9mANnchPy5KbBGPEJdNfQbkBiT5j5Q/Jq1GPLoK9iIx1n20CU9uG3Rqlk9nez71k5lIi1zLkjYOG8ZJcsCZoEvrVZWq3FQdB04t89/1O/w1cDnyilFU="
LINE_CHANNEL_SECRET = "2a5ea71857e45cc5dcb325641cf0a6a9"

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)


# 設定 webhook 路由
@app.route("/callback", methods=["POST"])
def callback():
    # 取得 LINE 訊息
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)

    # 驗證訊息
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


# 處理文字訊息的回應
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text
    line_bot_api.reply_message(
        event.reply_token,
        TextMessage(text=f"你說了: {text}")  # 回覆用戶發送的文字
    )


if __name__ == "__main__":
    # app.run(debug=True)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
