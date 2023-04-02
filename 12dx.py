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
BOT_TOKEN = '' #bot token
CHAT_ID = '' #对话id

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

time1 = datetime.datetime.now(tz)
t = f'已自动开始12点监测，达到200次将自动退出\n当前时间:{time1}'
requests.get(f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={t}')

d = 0
previous_value = None
kcbp = None
def check_html():
    global d
    global previous_value
    global kcbp
    d += 1
    response = requests.get('https://free.vps.vc/create-vps', cookies=cookies, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    sj = soup.find('select', {'name': 'location', 'class': 'form-control', 'id': 'datacenter', 'required': ''})
    sj = str(sj)
    print(d)
     
    if sj != previous_value:
        previous_value = sj
        beijing_time = datetime.datetime.now(tz)
        soup = BeautifulSoup(sj, 'html.parser')
        select_tag = soup.find('select', {'id': 'datacenter'})
        options_tags = select_tag.find_all('option')[1:]

        if options_tags:
            a = [option.text.strip() for option in options_tags]
            a = '\n'.join(a)
            kc8 = a
        else:
            a = "暂无库存"
            kc8 = None

        set_a = set(kc8.split() if kc8 else [])
        set_b = set(kcbp.split() if kcbp else [])
        duo = f"+{set_a - set_b}"
        shao = f"-{set_b - set_a}"
        kcbp = kc8
        if duo == '+set()':
            duo1 = ''
        else:
            duo1 = f'\n{duo}'
        if shao == '-set()':
            shao1 = ''
        else:
            shao1 = f'\n{shao}'
        
        text = f"库存发生变化：\n{a}\n当前时间:{beijing_time}{duo1}{shao1}"
        print(text)
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={text}"
        requests.get(url)

    
    if d == 200:
        print(d)
        print('退出监控')
        time2 = datetime.datetime.now(tz)
        t2 = f'已自动退出监控程序\n当前时间:{time2}'
        requests.get(f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={t2}')
        sys.exit()



# 使用schedule模块定时执行check_a函数
schedule.every(1).seconds.do(check_html)

# 持续运行程序
while True:
    schedule.run_pending()
    time.sleep(1)