import httpx
import mail
import datetime
from bs4 import BeautifulSoup as bs4
import re
import config as conf
import os

class BjBusClock():
    def __init__(self, logger, config=None, ):
        self.logger = logger
        import json
        if config is None:
            with open(r"C:\config.json", "r", encoding='UTF-8') as config_file:
                config = json.load(config_file)
        if config is None:
            raise "没有提供配置且没找到配置文件"

        self.config = conf.Config(config)  # 整体配置
        
        if self.config.mailConfig is None:
            raise "没有发送通知的邮箱配置"
        self.config.alertMail = config.get("alertMail", None)
        if self.config.alertMail is None:
            raise "没有接收通知的邮箱地址"
        self.mailClient = mail.MailSent(self.config.mailConfig)
        self.logger.info("BusClock 初始化完毕")


    def run(self):
        self.logger.info("BusClock 执行运算")
        for line in self.config.lines:
            self.logger.info("BusClock 执行线路:" + "@" + line['line'])
            if self.onTime(line['begin'], line['end']):
                self.logger.info("BusClock 达到提示时间 " + "@" + line['line'])
                if line.get('needSentMail', True):
                    self.logger.info("BusClock 需要发提醒 " + "@" + line['line'])
                    bustime = self.getBusTime(line)
                    if  bustime is None:
                        self.logger.info("BusClock 尚未发车: " + "@" + line['line'])
                    else:
                        self.logger.info("BusClock 得到车辆时间: " + bustime + "@" + line['line'])
                        if int(bustime) <= int(line.get('latestLeaveMinute', self.config.latestLeaveMinute)):
                            self.logger.info("BusClock 可以发邮件提醒了" + "@" + line['line'])
                            self.mailClient.send_mail(self.config.alertMail, '班车提醒: '+line['line'], '车辆即将到站，现在出发正当时')
                            self.logger.info("BusClock 邮件提醒已发送" + "@" + line['line'])
                            line['needSentMail'] = False  # 发送通知后，不必再发了
                        else:
                            self.logger.info("BusClock 没到发邮件的时候" + "@" + line['line'])
                else:
                    self.logger.info("BusClock 已经发过邮件了" + "@" + line['line'])
            else:
                line['needSentMail'] = True
                self.logger.info("BusClock 未到时间窗口" + "@" + line['line'])


    def onTime(self, begin, end):
        d_time = datetime.datetime.strptime(
            str(datetime.datetime.now().date())+begin, '%Y-%m-%d%H:%M')
        d_time1 = datetime.datetime.strptime(
            str(datetime.datetime.now().date())+end, '%Y-%m-%d%H:%M')
        n_time = datetime.datetime.now()
        if n_time > d_time and n_time < d_time1:
            return True
        else:
            return False

    def getBusTime(self, line):
        url = 'http://www.bjbus.com/home/ajax_rtbus_data.php?act=busTime&selBLine=%(line)s&selBDir=%(dir)s&selBStop=%(stop)s' % line
        result = None
        try:
            r = httpx.get(url).json()
            b = bs4(r.get('html'), 'html.parser')
            info = b.find('article')
            i = info.find_all('p')[1]
            ret = re.search(r'\d+(?=\s分钟)', i.text)
            result = None
            if ret:
                result = ret.group()
        except BaseException:
            pass

        return result


if __name__ == "__main__":
    import logging
    logging.basicConfig(filename=r'D:\busclock.log', level=logging.INFO)
    bus = BjBusClock(logging, {
        "loopWaitSeconds": 60,
        "spurtWaitSeconds": 10,
        "latestLeaveMinute": 5,
        "mailConfig": {
            "FROM": "tom@example.com",
            "HOST": "smtp.example.com",
            "PORT": "465",
            "USER": "tom",
            "PASS": "password",
            "SSL": True
         },
        "alertMail": "lily@example.com",
        "lines": [{
            "line": "835快",
            "dir": "5066222788346588777",
            "stop": "13",
            "begin": "08:00",
            "end": "08:30"
        }, {
            "line": "835快",
            "dir": "4997908670784162973",
            "stop": "3",
            "begin": "19:00",
            "end": "20:30"
        }]
    })
    print(bus.onTime("12:00", "13:00"))
    print(bus.getBusTime(bus.config.lines[0]))
    print(bus.run())
