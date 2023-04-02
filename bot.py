import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests
from bs4 import BeautifulSoup
import config
import sys
import datetime
import pytz
import time
import imp
import config
import re
import fileinput
valid_ids = [] #管理员id（纯数字，如果需要多个逗号相隔）

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

def start(update, context):
    userid = update.effective_chat.id
    text = '欢迎使用vc库存bot\n发送 /help 查看帮助 \n库存及CK实时频道:https://t.me/vpsvckc\n本程序已开源https://github.com/w4616/vc_bot/'
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)

def vc(update, context):
    imp.reload(config)
    cookies = {
    'PHPSESSID': config.ck,
}
    global headers
    response = requests.get('https://free.vps.vc/create-vps', cookies=cookies, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    sj = soup.find('select', {'name': 'location', 'class': 'form-control', 'id': 'datacenter', 'required': ''})
    sj = str(sj)
    if 'None' in sj:
       a = 'ck已失效'
    else:
        soup = BeautifulSoup(sj, 'html.parser')
        select_tag = soup.find('select', {'id': 'datacenter'})
        options_tags = select_tag.find_all('option')[1:]
        if options_tags:
            b = [option.text.strip() for option in options_tags]
            b = '\n'.join(b)
            a = f'当前可用地区:\n{b}'
        else:
            a = f"暂时无可用机器\n北京时间12点放机\n其他时间以公告为准"
    context.bot.send_message(chat_id=update.effective_chat.id, text=a)

def x(update, context):
    imp.reload(config)
    cookies = {
    'PHPSESSID': config.ck,
}
    global headers
    response = requests.get('https://free.vps.vc/create-vps', cookies=cookies, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    os_select = soup.find('select', {'name': 'os', 'class': 'form-control', 'id': 'os', 'required': ''})
    if os_select == None:
       a = 'ck已失效'
    else:
        #soup = BeautifulSoup(os_select, 'html.parser')
        select_tag = soup.find('select', {'id': 'os'})
        options_tags = select_tag.find_all('option')[1:]
        b = [option.text.strip() for option in options_tags]
        b = '\n'.join(b)
        a = f'{b}'
    context.bot.send_message(chat_id=update.effective_chat.id, text=a)

def ping(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='pong')

def ck(update, context):
    global valid_ids
    userid = update.effective_chat.id
    userdate = update.message.text[4:]
    imp.reload(config)
    ck = config.ck
    if userid in valid_ids:
        for line in fileinput.input('config.py', inplace=True):
            print(line.replace(ck, userdate), end='')
        text = '已将config.py中的ck变量修改为{userdate}'
    else:
        text = '您不是管理员'
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)

def help(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='/vc 库存\n/x 系统 没什么实际作用\n/ping 检测是否存活\n/help 帮助\n/ck 设置ck\n库存及CK实时频道:https://t.me/vpsvckc')

def main():
    updater = Updater(token='6171476381:AAGOV8QIo1MrTE4vaJa0lkZ2p0YdebXFRdQ', use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('vc', vc))
    dispatcher.add_handler(CommandHandler('x', x))
    dispatcher.add_handler(CommandHandler('ck', ck))
    dispatcher.add_handler(CommandHandler('help', help))
    dispatcher.add_handler(CommandHandler('ping', ping))
    updater.start_polling()

if __name__ == '__main__':
    main()