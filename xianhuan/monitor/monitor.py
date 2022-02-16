#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: 闲欢
"""
from pynput import keyboard, mouse
from loguru import logger
from threading import Thread

# 定义日志文件
logger.add('moyu.log')


def on_press(key):
    logger.debug(f'{key} :pushed')


def on_release(key):
    if key == keyboard.Key.esc:
        return False


# 定义键盘监听线程
def press_thread():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as lsn:
        lsn.join()


def on_click(x, y, button, pressed):
    if button == mouse.Button.left:
        logger.debug('left was pressed!')
    elif button == mouse.Button.right:
        logger.debug('right was pressed!')
        return False
    else:
        logger.debug('mid was pressed!')


# 定义鼠标监听线程
def click_thread():
    with mouse.Listener(on_click=on_click) as listener:
        listener.join()


if __name__ == '__main__':
    # 起两个线程分别监控键盘和鼠标
    t1 = Thread(target=press_thread())
    t2 = Thread(target=click_thread())
    t1.start()
    t2.start()
