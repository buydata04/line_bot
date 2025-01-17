import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, Heroku! The app is up and running!'

if __name__ == "__main__":
    # 使用 Heroku 提供的 $PORT 來綁定服務
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

