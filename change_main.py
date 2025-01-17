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

if __name__ == '__main__':
    findcode = Findcode()
    exchange = Exchange()

    # 抓取序號
    codelist = findcode.fetch().filter()
    if not codelist:
        logging.info("無法獲取任何序號")
    else:
        # 開始兌換序號
        for user in user_list:
            logging.info(f"用戶: {user}")
            print(f"用戶: {user}")
            for code in codelist:
                # logging.info(f"序號: {code}")
                # print(f"序號: {code}")

                # 獲取兌換結果
                result = exchange.fetch(user, code).filter()

                # 假設result返回的是 '重複領取' 或 '領取成功'，然後加上序號
                print(f"兌換結果: {result} ({code})")

                time.sleep(0.5)  # 延遲以避免伺服器過載
