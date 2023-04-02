import requests
from bs4 import BeautifulSoup
import datetime
import pytz
import sys
import config
import date
import fileinput

tz = pytz.timezone('Asia/Shanghai')
BOT_TOKEN = '' #bot token
CHAT_ID = '' #对话id
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
runfrequency = int(date.ber)
runfrequencyn = date.ber
previous_value = date.date



runfrequency1 = runfrequency + 1
print(f'第{runfrequency1}次')
for line in fileinput.input('date.py', inplace=True):
        print(line.replace(runfrequencyn, str(runfrequency1)), end='')
cookies = {'PHPSESSID': config.ck,}
response = requests.get('https://free.vps.vc/create-vps', cookies=cookies, headers=headers)
    

soup = BeautifulSoup(response.text, 'html.parser')
sj = soup.find('select', {'name': 'location', 'class': 'form-control', 'id': 'datacenter', 'required': ''})
sj = str(sj)
date1 = sj.replace('\n', '')



            


if date1 != previous_value:
    for line in fileinput.input('date.py', inplace=True):
        print(line.replace(previous_value, date1), end='')
    beijing_time = datetime.datetime.now(tz)
    soup = BeautifulSoup(sj, 'html.parser')
    select_tag = soup.find('select', {'id': 'datacenter'})
    options_tags = select_tag.find_all('option')[1:]
    
    if options_tags:
        a = [option.text.strip() for option in options_tags]
        a = '\n'.join(a)
    else:
        a = "暂无库存"
    text = f"库存发生变化：\n{a}\n当前时间:{beijing_time}\n当前消息为24小时监控"
    print(text)
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={text}"
            
    if 1 == runfrequency1:
        print('首次不发送')
    else:
        requests.get(url)
                

    
    
    
    
    
    
    
    
    
    
    
    
    
    