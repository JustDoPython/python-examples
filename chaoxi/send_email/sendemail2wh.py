import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

my_sender = 'xxxxx@qq.com'  # 发送方邮箱
my_psw = 'xxxxxxxxxxx'  # 填入发送方邮箱的授权码
my_user = 'xxxx@qq.com'  # 收件人邮箱


def send():
    subject = "解封纪念日"  # 主题
    msg = MIMEMultipart('related')
    content = MIMEText('<html><body><img src="cid:imageid" alt="imageid"></body></html>', 'html', 'utf-8')  # 正文
    # msg = MIMEText(content)
    msg.attach(content)
    msg['From'] = Header("潮汐同学", 'utf-8')
    msg['To'] = Header("武汉人民", 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')

    file = open("./picture.png", "rb")
    img_data = file.read()
    file.close()

    img = MIMEImage(img_data)
    img.add_header('Content-ID', 'imageid')
    msg.attach(img)

    try:
        s = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 邮件服务器及端口号
        s.login(my_sender, my_psw)
        s.sendmail(my_sender, my_user, msg.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException:
        print("Error: 无法发送邮件")

if __name__ == '__main__':
    send()