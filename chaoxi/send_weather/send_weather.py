
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import requests
from bs4 import BeautifulSoup
import prettytable as pt

def get_Data(url):
    data_list = []
    response = requests.get(url)
    html_doc = response.text
    soup = BeautifulSoup(html_doc, 'lxml')  # 自动补全html代码，并按html代码格式返回
    wendu = soup.find('div', class_='temperature').get_text()
    tianqi = soup.find('div', class_='weather-icon-wrap').get_text()
    data_list.append("现在的温度：%s\n现在天气情况：%s" % (wendu, tianqi))
    list = soup.find_all('ul', class_='weather-columns')
    for item in list:
        data_list.append(item.get_text())
    print("列表数据：",data_list)
    a = 1
    tb = pt.PrettyTable() #创建PrettyTable对象
    tb.field_names = ["日期","天气","详情"]
    for item in data_list:
        # print(a)
        if a != 1:
            tb.add_row([item.strip().split()[0]+item.strip().split()[1],item.strip().split()[2],item.strip().split()[3]])
        else: print(item.strip())
        a+=1
    print(tb)
    return tb



def send_mail(msg,receiver):
    # 收件人
    receiver = receiver
    mail_title = '小姐姐，请查收今天以及往后15天的天气预报，愿你三冬暖，春不寒'
    mail_body = str(msg)
    # 创建一个实例
    message = MIMEText(mail_body, 'plain', 'utf-8')  # 邮件正文
    # (plain表示mail_body的内容直接显示，也可以用text，则mail_body的内容在正文中以文本的形式显示，需要下载）
    message['From'] = sender  # 邮件的发件人
    message['To'] = receiver  # 邮件的收件人
    message['Subject'] = Header(mail_title, 'utf-8')  # 邮件主题

    smtp = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 创建发送邮件连接
    smtp.connect(smtpserver)  # 连接发送邮件的服务器
    smtp.login(username, password)  # 登录服务器
    smtp.sendmail(sender, receiver, message.as_string())  # 填入邮件的相关信息并发送

    smtp.quit()



if __name__ == '__main__':
    sender = 'xxx@qq.com'
    # 发件人邮箱的SMTP服务器（即sender的SMTP服务器）
    smtpserver = 'smtp.qq.com'
    # 发件人邮箱的用户名和授权码（不是登陆邮箱的密码）
    username = 'xxxxxx'
    # 邮箱授权码
    password = 'xxxxx'
    url1 = 'https://tianqi.so.com/weather/'
    url_list = ['url1','url1']
    receiver_list ='xxx@qq.com'
    tb = get_Data(url1) #获得每一个用户的数据
    send_mail(tb,receiver_list) #发送邮件
#