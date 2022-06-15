import email
import requests
import re
import os
import smtplib
from email.header import Header
from email.mime.text import MIMEText
import time
from email.utils import formataddr
#####
#####
userId = 11067  # edusrc的用户id，在个人主页的url里有
# 设置 SMTP 服务
my_sender = 'xxxxxxxx@qq.com'  # 填写发信人的邮箱账号
my_pass = 'xxxxx'  # 发件人邮箱16位授权码
my_user = 'xxxxxx'  # 收件人邮箱账号


def mail(getrank):
    ret = True
    try:
        msg = MIMEText('大佬，您有个报告过了( •̀ ω •́ )✧  现在的Rank是:'+str(getrank),
                       'plain', 'utf-8')  # 填写邮件内容
        msg['From'] = formataddr(["tracy", my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr(["test", my_user])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = "发送邮件测试"  # 邮件的主题，也可以说是标题

        server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器
        server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱授权码
        # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.sendmail(my_sender, [my_user, ], msg.as_string())
        server.quit()  # 关闭连接
        print("Mail sent")
    except Exception:  # 如果 try 中的语句没有执行，则会执行下面的
        print("Oh！no")


def getRank():
    url = "https://src.sjtu.edu.cn/profile/"+str(userId)
    r = requests.get(url)
    rule = r'Rank： (.*?)\n'
    rank = re.findall(rule, r.text)[0]
    return rank


def writeRank(getrank):
    with open("edurank.txt", mode='w+', encoding='utf-8') as ff:
        ff.write(getrank)


i = 1
while (i == 1):
    getrank = getRank()
    if os.path.exists('edurank.txt'):
        with open("edurank.txt") as f:
            rank = f.read()
        if(getrank != rank and rank != ''):
            mail(getrank)
            writeRank(getrank)
            print('Rank Update:'+str(getrank) +
                  time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime()))
        else:
            print('Not updated!!  ' +
                  time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime()))
            # print(time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime()))
            # mail(getrank)debug用的
            writeRank(getrank)
    else:
        writeRank(getrank)
        print('newfile')
    time.sleep(1800000)  # 这里设置执行的间隔，现在是半小时执行一次
# 放在服务器 可以用nohup python -u edu.py >edu.log 2>&1 &
# 会自动产生一个log日志！ps aux | grep python可以看当前的进程
