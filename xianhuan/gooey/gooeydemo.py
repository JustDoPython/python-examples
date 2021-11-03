#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: 闲欢
"""
from gooey import Gooey, GooeyParser


@Gooey(
    richtext_controls=True,                 # 打开终端对颜色支持
    program_name="MQTT连接订阅小工具",        # 程序名称
    encoding="utf-8",                       # 设置编码格式，打包的时候遇到问题
    progress_regex=r"^progress: (\d+)%$"    # 正则，用于模式化运行时进度信息
)
def main():
    settings_msg = 'MQTT device activation information subscription'
    parser = GooeyParser(description=settings_msg)

    subs = parser.add_subparsers(help='commands', dest='command')

    my_parser = subs.add_parser('MQTT消息订阅')
    my_parser.add_argument("connect", metavar='运行环境',help="请选择开发环境",choices=['dev环境','staging环境'], default='dev环境')
    my_parser.add_argument("device_type",metavar='设备类型',help="请选择设备类型",choices=['H1','H3'],default='H1')
    my_parser.add_argument("serialNumber", metavar='设备SN号',default='LKVC19060047',help='多个请用逗号或空格隔开')

    siege_parser = subs.add_parser('进度条控制')
    siege_parser.add_argument('num',help='请输入数字',default=100)

    args = parser.parse_args()
    print(args, flush=True)    # flush=True在打包的时候会用到


if __name__ == '__main__':
    main()
