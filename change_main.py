import time
from findcode import Findcode
from exchange import Exchange
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# 使用者帳號
user_list = [
    '1126934135224009636',
    '1126934187638915729',
    '1126934135108928409',
    '1126934114860796869'
]

def run_exchange():
    findcode = Findcode()
    exchange = Exchange()

    # 抓取序號
    codelist = findcode.fetch().filter()
    if not codelist:
        logging.info("無法獲取任何序號")
        return "無法獲取任何序號"

    result_str = "兌換結果:\n"
    # 開始兌換序號
    for user in user_list:
        result_str += f"\n{user}\n"
        for code in codelist:
            # 獲取兌換結果
            result = exchange.fetch(user, code).filter()
            result_str += f"{code} - {result} / "

        result_str += "\n"  # 進行換行處理

    return result_str
