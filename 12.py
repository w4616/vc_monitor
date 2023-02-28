'''连续监测库存的脚本'''
'''如果有库存变动则发送通知'''
import requests
from bs4 import BeautifulSoup
import time
import schedule
import datetime
import pytz
import sys
import config

# 创建时区对象
tz = pytz.timezone('Asia/Shanghai')





# 定义Telegram Bot API参数
BOT_TOKEN = config.bot_token
CHAT_ID = config.chat_id

cookies = {
    'PHPSESSID': config.ck,
}
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

d = 0
previous_value = None
def check_html():
    global d
    global previous_value
    d += 1
    response = requests.get('https://free.vps.vc/create-vps', cookies=cookies, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    sj = soup.find('select', {'name': 'location', 'class': 'form-control', 'id': 'datacenter', 'required': ''})
    sj = str(sj)
    print(d)
    if 'None' in sj:
        print('ck已失效，请重新设置ck')
        beijing_time = datetime.datetime.now(tz)
        message = f'ck已失效，请联系管理员重新设置ck\n{beijing_time}'
        # 发送Telegram Bot消息
        requests.get(f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}')
        sys.exit()
        


    if sj != previous_value:
        previous_value = sj
        beijing_time = datetime.datetime.now(tz)
        soup = BeautifulSoup(sj, 'html.parser')
        select_tag = soup.find('select', {'id': 'datacenter'})
        options_tags = select_tag.find_all('option')[1:]

        if options_tags:
            a = [option.text.strip() for option in options_tags]
            a = '\n'.join(a)
        else:
            a = "暂无库存"
        text = f"库存发生变化：\n{a}\n当前时间:{beijing_time}"
        print(text)
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={text}"
        requests.get(url)


# 使用schedule模块定时执行check_a函数
schedule.every(1).seconds.do(check_html)

# 持续运行程序
while True:
    schedule.run_pending()
    time.sleep(1)