import requests
import time
import random
import config
from bs4 import BeautifulSoup
import datetime
import pytz
import imp

bot_token = '' #bot token
chat_id = '' #对话id


headers1 = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Referer': 'https://free.vps.vc/login',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
}
headers2 = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Referer': 'https://free.vps.vc/create-vps',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
}
headers3 = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Referer': 'https://free.vps.vc/vps-status',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
}
headers4 = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Referer': 'https://free.vps.vc/vps-control',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
}

# 创建时区对象
tz = pytz.timezone('Asia/Shanghai')


urls = ['https://free.vps.vc/vps-info', 'https://free.vps.vc/vps-status', 'https://free.vps.vc/vps-control', 'https://free.vps.vc/vps-reinstall']
a = 0

while True:
    imp.reload(config)
    cookies = {
    'PHPSESSID': config.ck,
}
    url = random.choice(urls)  # 随机选择一个URL
    if url == 'https://free.vps.vc/vps-info':
        headers = headers1
    elif url == 'https://free.vps.vc/vps-status':
        headers = headers2
    elif url == 'https://free.vps.vc/vps-control':
        headers = headers3
    elif url == 'https://free.vps.vc/vps-reinstall':
        headers = headers4
    response = requests.get(url, cookies=cookies, headers=headers)  # 发送请求
    a += 1
    print(f'{response.status_code} 已运行{a}次')


    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    div = soup.find('div', {'class': 'text-center wow fadeInUp animated'})
    text = div.text
    if 'Login to Free.vps.vc' in text:
        print('ck已失效，请重新设置ck')
        beijing_time = datetime.datetime.now(tz)
        message = f'ck已失效，请联系管理员https://t.me/cjak6重新设置ck\n{beijing_time}\n(本消息仅作为https://t.me/vcfreekc_bot ck通知)\n本频道运行时间请看置顶谢谢'
        # 发送Telegram Bot消息
        requests.get(f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={message}')
        break  # 停止运行


    time.sleep(200) 