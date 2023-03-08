# -*- coding:utf-8 -*-

import optparse,os,json
from subprocess import *

class DomainHandler(object):
    def __init__(self):
        pass

    def exec_cmd(self,cmd):
        res = Popen(cmd, shell=True, stdout=PIPE)
        ret = res.communicate()[0].decode('utf-8')
        return ret.strip()

    def domain_info(self):
        cmd = 'curl -s https://dnsapi.cn/Domain.List -d "login_token=391845,92f408bb5343e&format=json"'
        data = json.loads(self.exec_cmd(cmd))
        print(data)
        for item in data['domains']:
            print('%s:%s' % (item['name'], item['id']))

    def add_Arecord(self,domain_id,sub_domain,record_type,address):
        print(domain_id,sub_domain,record_type,address)
        cmd2 = "curl -s -X POST https://dnsapi.cn/Record.Create -d 'login_token=391845,92f408bb5343e&format=json&domain_id={0}&sub_domain={1}&record_type={2}&record_line_id=0&value={3}'".format(
            domain_id, sub_domain, record_type, address)
        r = json.loads(self.exec_cmd(cmd2))
        print(r['status']['message'])

    def add(self):
        self.domain_info()
        while tag:
            self.domain_id = input('\033[1;42m输入域名ID:\033[0m').strip()
            if self.domain_id == 'q':
                break
            if not self.domain_id or not self.domain_id.isdigit():
                print('\033[31merror id\033[0m')
                continue
            self.sub_domain = input('\033[1;42m子域名[@或*等]:\033[0m').strip()
            self.record_type = input('\033[1;42m类型[A或CNAME]:\033[0m').strip()
            self.address = input('\033[1;42m记录值(ip或域名):\033[0m').strip()

            if not self.sub_domain or not self.record_type or not self.address:
                print('\033[31m参数不能为空\033[0m')
                continue
            self.add_Arecord(self.domain_id,self.sub_domain,self.record_type,self.address)
            if self.domain_id == 'q' or self.record_type == 'q' or self.address == 'q':
                self.tag = False
            break

    def get_records(self):
        self.domain_info()
        flag = True
        while tag:
            if not flag:
                break
            self.domain_id = input('\033[1;42m输入域名ID:\033[0m').strip()
            if self.domain_id == 'q':
                break
            if not self.domain_id or not self.domain_id.isdigit():
                print('\033[31merror id\033[0m')
                continue
            self.sub_domain = input('\033[1;42m子域名[@或*等]:\033[0m').strip()
            self.record_type = input('\033[1;42m类型[A或CNAME]:\033[0m').strip()
            cmd3 = "curl -s -X POST https://dnsapi.cn/Record.List -d 'login_token=391845,92f408bb5343e&format=json&domain_id={0}&sub_domain={1}&record_type={2}&offset=0&length=3'".format(
                self.domain_id, self.sub_domain, self.record_type)
            records = json.loads(self.exec_cmd(cmd3))
            try:
                print('\033[33m共%s条%s记录\033[0m' % (len(records['records']), self.record_type))
            except Exception as e:
                print('\033[31m查无此记录\033[0m')
                continue
            for record in records['records']:
                print('\033[35mID{0}: {1}{split}{2}{split}{3}\033[0m'.format(record['id'], record['name'], record['type'],record['value'], split=' ' * 10))
            return records

    def mod(self):
        records = self.get_records()
        while tag:
            record_id = input('\033[1;42m输入record ID:\033[0m').strip()
            if record_id == 'q':
                break
            value = input("\033[1;42m输入新的record value:\033[0m").strip()
            if value == 'q':
                break
            cmd4 = "curl -s -X POST https://dnsapi.cn/Record.Modify -d 'login_token=391845,92f408bb5343e&format=json&domain_id={0}&record_id={1}&sub_domain={2}&value={3}&record_type={4}&record_line_id=0'".format(self.domain_id,record_id,self.sub_domain,value,self.record_type)
            r = json.loads(self.exec_cmd(cmd4))
            print(r['status']['message'])
            flag = False
            break
    def delete(self):
        records = self.get_records()
        while tag:
            record_id = input('\033[1;42m输入record ID:\033[0m').strip()
            if record_id == 'q':
                break
            cmd5 = "curl -s -X POST https://dnsapi.cn/Record.Remove -d 'login_token=391845,92f408bb5343e&format=json&domain_id={0}&record_id={1}'".format(self.domain_id,record_id)
            r = json.loads(self.exec_cmd(cmd5))
            print(r['status']['message'])
            flag = False
            break

dic = {
    '1':DomainHandler().add,
    '2':DomainHandler().mod,
    '3':DomainHandler().delete
}

tag = True
while tag:
    print('''
    1.增加
    2.修改
    3.删除
    q.退出
    ''')
    choice = input('\033[1;42m输入选项:\033[0m').strip()
    if not choice:
        continue
    if choice == 'q':
        break
    if choice in dic:
        dic[choice]()

    else:
        print('\033[31m选项不存在\033[0m')