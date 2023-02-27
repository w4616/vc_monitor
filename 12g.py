''' 因为我觉得没必要所以未经测试！！！'''
'''连续监测库存的脚本'''
'''如果有库存变动则发送通知'''
import requests
from bs4 import BeautifulSoup
import re
import time
import schedule
import datetime
import pytz
import config
import imp

# 创建时区对象
tz = pytz.timezone('Asia/Shanghai')





# 定义Telegram Bot API参数
BOT_TOKEN = config.bot_token
CHAT_ID = config.chat_id

# 定义Cookies和Headers

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Referer': 'https://free.vps.vc/vps-info',
    'Alt-Used': 'free.vps.vc',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
}


previous_value = None

def check_html():
    imp.reload(config)
    cookies = {
    'PHPSESSID': config.ck,
}
    global previous_value
    response = requests.get('https://free.vps.vc/create-vps', cookies=cookies, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    location_select = soup.find('select', {'name': 'location', 'class': 'form-control', 'id': 'datacenter', 'required': ''})
    pattern = re.compile(r'<option value="">-select-</option>')
    location_select = str(location_select)
    html1 = re.sub(pattern, '', location_select)
    print(location_select)

    if html1 != previous_value:
        beijing_time = datetime.datetime.now(tz)
        text = f"库存发生变化：{html1}\n当前时间:{beijing_time}"
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={text}"
        requests.get(url)
        previous_value = html1


# 使用schedule模块定时执行check_a函数
schedule.every(1).seconds.do(check_html)

# 持续运行程序
while True:
    schedule.run_pending()
    time.sleep(1)
