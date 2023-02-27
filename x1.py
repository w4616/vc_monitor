'''获取系统的脚本，以前主要用于检测ck是否失效现在加了判断没啥用了'''
import requests
from bs4 import BeautifulSoup
import re
import config

#填自己的账号ck
PHPSESSID1 = config.ck

cookies = {
    'PHPSESSID': PHPSESSID1,
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

#请求获取网页数据
response = requests.get('https://free.vps.vc/create-vps', cookies=cookies, headers=headers)

#格式化数据
soup = BeautifulSoup(response.text, 'html.parser')



#打印结果，可选
#print(html1)


#此代码为测试代码，因为选择系统选项与库存相似，可以当作测试代码(ck失效也会打印无)
#删除以下代码前#即为启用
os_select = soup.find('select', {'name': 'os', 'class': 'form-control', 'id': 'os', 'required': ''})
pattern = re.compile(r'<option value="">-select-</option>')
os_select = str(os_select)
html1 = re.sub(pattern, '', os_select)
#测试代码结束

#整理数据
pattern = r'<option value="(\d+)">([^<]+)</option>'
matches = re.findall(pattern, html1)

#如果有库存则打印，无库存则打印"无"
#暂时没有加ck失效判断，如果能写出来会加
if matches:
    for match in matches:
        print(f"{match[0]}:{match[1]}")
else:
    print("ck失效")