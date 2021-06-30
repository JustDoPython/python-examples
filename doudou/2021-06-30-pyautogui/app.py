# coding=utf-8

import time
import pyautogui


# 将图片拖入轨道
def drag_img_to_track():
    # 选中图片
    pyautogui.moveTo(170, 270)
    pyautogui.doubleClick()
    # 拖拽图片至轨道
    pyautogui.dragTo(120, 600, 1, button='left')


# 调整视频时长
def drag_img_to_3_min():
    # 选中轨道中的第一张图
    pyautogui.moveTo(125, 600)
    pyautogui.click()
    # 拖拽至第三分钟
    pyautogui.moveTo(135, 600)
    pyautogui.dragTo(700, 600, 1, button='left')


# 删除旧的素材
def delete_top_img():
    # 删除轨道中的第二张图片
    pyautogui.moveTo(300, 160)
    pyautogui.doubleClick()
    pyautogui.press("backspace")

    # enter yes
    pyautogui.moveTo(650, 470)
    time.sleep(0.5)
    pyautogui.click()


# 导出
def export(name):
    pyautogui.moveTo(126, 600)
    pyautogui.click()

    pyautogui.hotkey('command', 'e')
    pyautogui.write(name)
    time.sleep(1)
    pyautogui.moveTo(800, 393)
    pyautogui.click()
    time.sleep(20)
    pyautogui.click()


index = 0
count = 2
while index < count:
    drag_img_to_track()
    drag_img_to_3_min()
    delete_top_img()
    export(str(index))
    time.sleep(2)
    index += 1
    print("end..." + str(index))