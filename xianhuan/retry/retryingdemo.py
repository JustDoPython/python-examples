#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: 闲欢
"""
import random
from retrying import retry


@retry
def do_something_unreliable():
    if random.randint(0, 10) > 1:
        print("just have a test")
        raise IOError("raise exception!")
    else:
        return "good job!"


print(do_something_unreliable())


# 最大重试次数
@retry(stop_max_attempt_number=5)
def do_something_limited():
    print("do something several times")
    raise Exception("raise exception")

# do_something_limited()


# 限制最长重试时间（从执行方法开始计算）
@retry(stop_max_delay=5000)
def do_something_in_time():
    print("do something in time")
    raise Exception("raise exception")

# do_something_in_time()


# 设置固定重试时间
@retry(wait_fixed=2000)
def wait_fixed_time():
    print("wait")
    raise Exception("raise exception")

# wait_fixed_time()

# 设置重试时间的随机范围
@retry(wait_random_min=1000,wait_random_max=2000)
def wait_random_time():
    print("wait")
    raise Exception("raise exception")

# wait_random_time()


# 根据异常重试
def retry_if_io_error(exception):
    return isinstance(exception, IOError)

# 设置特定异常类型重试
@retry(retry_on_exception=retry_if_io_error)
def retry_special_error():
    print("retry io error")
    raise IOError("raise exception")

# retry_special_error()


# 通过返回值判断是否重试
def retry_if_result_none(result):
    """Return True if we should retry (in this case when result is None), False otherwise"""
    # return result is None
    if result =="111":
        return True


@retry(retry_on_result=retry_if_result_none)
def might_return_none():
    print("Retry forever ignoring Exceptions with no wait if return value is None")
    return "111"

might_return_none()







