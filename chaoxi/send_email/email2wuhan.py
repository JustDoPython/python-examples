import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header


my_sender = 'xxxxx@qq.com'  # 发送方邮箱
my_psw = 'xxxxxxxxxxx'  # 填入发送方邮箱的授权码
my_user = 'xxxx@qq.com'  # 收件人邮箱


# 创建一个带附件的实例
message = MIMEMultipart()
message['From'] = Header("潮汐同学", 'utf-8')
message['To'] =  Header("武汉人民", 'utf-8')
subject = '荆楚疫情去'
message['Subject'] = Header(subject, 'utf-8')

# 邮件正文内容
message.attach(MIMEText('南山镇守江南之都，且九州一心！月余，疫尽去，举国庆之！', 'plain', 'utf-8'))
# 构造附件1，传送当前目录下的 test.txt 文件
att1 = MIMEText(open('./test.txt', 'rb').read(), 'base64', 'utf-8')
att1["Content-Type"] = 'application/octet-stream'
# 这里的filename可以任意写，写什么名字，邮件中显示什么名字
att1["Content-Disposition"] = 'attachment; filename="test.txt"'
message.attach(att1)

try:
    server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25

    server.login(my_sender, my_psw)  # 发件人邮箱账号、邮箱密码
    server.sendmail(my_sender, my_user, message.as_string())
    server.quit()  # 关闭连接
    print("邮件发送成功")
except smtplib.SMTPException:
    print("Error: 无法发送邮件")

