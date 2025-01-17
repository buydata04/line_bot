import requests
import re
import json


class Exchange:
    def __init__(self):
        self.body = ''
        self.session = requests.Session()

    def fetch(self, card_user: str, card_code: str):
        """向伺服器提交序號兌換請求"""
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
        }
        params = {
            'appkey': '1533634455460',
            'card_user': card_user,
            'card_channel': '0123456789',
            'card_server': '2001',
            'card_role': card_user,
            'card_code': card_code,
        }
        url = 'https://activity.game-beans.com/activity/cmn/card/csmweb.do?pd_acti_cb=jsonpcard_1234'

        try:
            response = self.session.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            self.body = response.text
        except requests.RequestException as e:
            print(f"兌換失敗: {e}")
        return self

    def filter(self):
        """解析兌換結果並直接輸出"""
        # 去除 JSONP 包裹，提取內部 JSON
        match = re.search(r'jsonpcard_1234\((.*)\);', self.body)
        if not match:
            return "兌換失敗（無法解析返回資料）"

        try:
            json_data = json.loads(match.group(1))  # 解析為字典
            info = json_data.get("info", -1)  # 提取 "info" 值
            if info == 111:
                return "重複領取"
            elif info == 115:
                return "領取成功"
            elif info == 108:
                return "無效序號"
            else:
                return "兌換失敗"
        except json.JSONDecodeError:
            return "兌換失敗（JSON 解析錯誤）"
