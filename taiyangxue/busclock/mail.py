#!/usr/local/bin/python3
# coding=utf-8

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class MailSent(object):
    default_config = {
        'PORT': '465',
        'SSL': True
    }

    def __init__(self, config):
        self.config = {
            'FROM': config.get('mail_from', self.default_config['FROM']),
            'HOST': config.get('mail_host', self.default_config['HOST']),
            'PORT': config.get('port', self.default_config['PORT']),
            'USER': config.get('user', self.default_config['USER']),
            'PASS': config.get('mail_pass', self.default_config['PASS']),
            'SSL': config.get('ssl', self.default_config['SSL']),
        }

    def send_mail(self, to_mail, title, content):
        ret = True
        FROM_MAIL = self.config['FROM']  # 发件人
        if type(to_mail) == 'list':
            TO_MAIL = to_mail  # 收件人
        else:
            TO_MAIL = [to_mail]

        SMTP_SERVER = self.config['HOST']  # qq邮箱服务器
        SSL_PORT = self.config['PORT']  # 加密端口
        USER_NAME = self.config['USER']  # qq邮箱用户名
        USER_PWD = self.config['PASS']  # qq邮箱授权码
        msg = MIMEMultipart('alternative')  # 实例化email对象
        msg['from'] = FROM_MAIL  # 对应发件人邮箱昵称、发件人邮箱账号
        msg['to'] = ';'.join(TO_MAIL)  # 对应收件人邮箱昵称、收件人邮箱账号
        msg['subject'] = title  # 邮件的主题
        txt = MIMEText(content, 'html')
        msg.attach(txt)
        try:
            # 纯粹的ssl加密方式
            smtp = smtplib.SMTP_SSL(SMTP_SERVER, SSL_PORT)  # 邮件服务器地址和端口
            smtp.ehlo()  # 用户认证
            smtp.login(USER_NAME, USER_PWD)  # 括号中对应的是发件人邮箱账号、邮箱密码
            smtp.sendmail(FROM_MAIL, TO_MAIL, str(msg))  # 收件人邮箱账号、发送邮件
            smtp.quit()  # 等同 smtp.close()  ,关闭连接
            # print('发送成功')
        except Exception:
            ret = False
        return ret
