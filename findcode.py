import requests
import re
import logging

logging.basicConfig(level=logging.WARNING, format="%(asctime)s - %(levelname)s - %(message)s")


class Findcode:
    def __init__(self):
        self.body = ''
        self.session = requests.Session()

    def fetch(self):
        """從指定網址抓取序號"""
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
        }
        url = 'https://www.game-beans.com/actv/45/supply/js/index.js'
        try:
            response = self.session.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            self.body = response.text
            logging.info("序號抓取成功")
        except requests.RequestException as e:
            logging.error(f"序號抓取失敗: {e}")
        return self

    def filter(self):
        """過濾抓取內容，匹配序號"""
        codes = re.findall(r'[A-Z0-9]{9}', self.body)
        logging.debug(f"抓取到的序號: {codes}")
        return codes
