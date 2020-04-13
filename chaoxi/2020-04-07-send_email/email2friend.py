import smtplib
from email.mime.text import *
from email.utils import formataddr

my_sender = 'xxxxx@qq.com'  # 发送方邮箱
my_psw = 'xxxxxxxxxxx'  # 填入发送方邮箱的授权码
my_user = 'xxxx@qq.com'  # 收件人邮箱


def send_email():
    ret = True
    try:
        msg = MIMEText('待花开时，邀您一起赏花吃热干面，我们重新拥抱这座城市的热情', 'plain', 'utf-8')

        msg['From'] = formataddr(["知心。。。。", my_sender])  # 发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr(["知心。。。。", my_user])  # 收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = "静待归期！"  # 邮件主题

        server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25

        server.login(my_sender, my_psw)  # 发件人邮箱账号、邮箱密码
        server.sendmail(my_sender, [my_user, ], msg.as_string())  # 发件人邮箱账号、授权码、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
    except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
        ret = False
    return ret

ret = send_email()
if ret:
    print(ret)
    print("邮件发送成功")
else:
    print(ret)
    print("邮件发送失败")

