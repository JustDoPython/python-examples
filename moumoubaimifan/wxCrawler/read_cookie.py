# read_cookie.py
import re
import os

class ReadCookie(object):
    """
    启动write_cookie.py 和 解析cookie文件，
    """

    def __init__(self, outfile):
        self.outfile = outfile

    def parse_cookie(self):
        """
        解析cookie
        :return: appmsg_token, biz, cookie_str·
        """
        f = open(self.outfile)
        lines = f.readlines()
        appmsg_token_string = re.findall("appmsg_token.+?&", lines[0])
        biz_string = re.findall('__biz.+?&', lines[0])
        appmsg_token = appmsg_token_string[0].split("=")[1][:-1]
        biz = biz_string[0].split("__biz=")[1][:-1]

        cookie_str = '; '.join(lines[1][15:-2].split('], [')).replace('\'','').replace(', ', '=')
        return appmsg_token, biz, cookie_str

    def write_cookie(self):
        """
        启动 write_cookie。py
        :return:
        """

        #当前文件路径
        path = os.path.split(os.path.realpath(__file__))[0]
        # mitmdump -s 执行脚本 -w 保存到文件 本命令
        command = "mitmdump -s {}/write_cookie.py -w {} mp.weixin.qq.com/mp/getappmsgext".format(
            path, self.outfile)

        os.system(command)


if __name__ == '__main__':
    rc = ReadCookie('cookie.txt')
    rc.write_cookie()
    appmsg_token, biz, cookie_str = rc.parse_cookie()
    print("appmsg_token：" + appmsg_token , "\nbiz：" + biz, "\ncookie："+cookie_str)