# vc_monitor
vc库存bot，监控，ck保活全套，学习python写的一个脚本，算是边学边写的，写的很烂。
### 使用教程
下载并解压

进入解压完的目录

配置config.py和bot.js的值

安装python

```shell
apt-get upgrade -y # CentOS：yum update -y
apt install -y python3 python3-pip # CentOS: yun install -y python3 python3-pip
pip3 install -r requirements.txt
```

安装nodejs

```shell
apt install -y nodejs npm # CentOS：yum install -y nodejs npm
npm install node-telegram-bot-api
```

运行

```shell
node bot.js
```

使用screen持续运行ck.py（监测可选24是1分钟监测一次，12和12g是连续区别自己看）

后续如果ck失效需要重新运行ck.py,更换ck不需要
