import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from .config import Password, Sender, Smtpserver
import random


def get_code():
    """
    生成随机的六个数，用来当作验证码
    :return:
    """
    code = random.randint(100000, 999999)
    return code


def mail(receive_email, msg):
    """
    发送邮件的接口
    发送成功返回的是OK
    发送失败返回的是ERROR
    现在配置里面有两个邮件配置
    具体使用方法
    1.
        form xxx import sendemail
    2.
        res = sendemail.mail("382552192@qq.com")
    :param receive_email: 需要发送的地址
    :return:
    """
    try:
        """随机选用邮件发送的配置"""

        sender = Sender
        password = Password
        smtpserver = Smtpserver

        msg = MIMEText('亲爱的%s用户您好 \n 欢迎您的到来　请您在5分钟内点击以下链接进行激活账号：%s \n   ' % (receive_email, msg), 'plain', 'utf-8')
        msg['From'] = formataddr(["[化骨龙]", sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr(["收件人昵称", receive_email])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = "[验证码]"  # 邮件的主题，也可以说是标题

        server = smtplib.SMTP_SSL(smtpserver, 465)  # 发件人邮箱中的SMTP服务器，端口是465
        server.login(sender, password)  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(sender, [receive_email, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
        return "OK"
    except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
        return "ERROR"
