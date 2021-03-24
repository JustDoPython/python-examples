#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: 闲欢
"""
from loguru import logger

logger.debug('this is a debug message')

logger.add('hello.log')

logger.debug('i am in log file')

id = logger.add('world.log', format="{time} | {level} | {message}", level="INFO")
logger.info('this is a debug message')
logger.remove(id)
logger.info('this is another debug message')
logger.add('runtime.log')
logger.info('this is an debug message')

# 超过200M就新生成一个文件
logger.add("size.log", rotation="200 MB")
# 每天中午12点生成一个新文件
logger.add("time.log", rotation="12:00")
# 一周生成一个新文件
logger.add("size.log", rotation="1 week")

@logger.catch
def a_function(x):
    return 1 / x

a_function(0)



def b_function1(x):
    try:
        return 1 / x
    except ZeroDivisionError:
        logger.exception("exception!!!")

b_function1(0)
