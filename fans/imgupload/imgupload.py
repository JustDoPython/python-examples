import time
import pyautogui

def auto_upload(x,y,file_path):
    # 点击”选择文件“按钮
    pyautogui.click(307, 227)
    time.sleep(2.5)

    # 弹出对话框后，点击路径那一栏，目的是为下一步粘贴路径
    pyautogui.click(993, 332)
    time.sleep(1.5)

    # 键入图片路径
    pyautogui.typewrite(file_path)
    # 按回车键
    pyautogui.hotkey('enter')
    time.sleep(1)

    # 双击图片
    pyautogui.doubleClick(x,y)
    # 等文件出现
    time.sleep(6)

    # 点击“上传”按钮
    pyautogui.click(304, 278)
    #等几秒传完
    if x == 847:
        #847是第一张图片的x坐标，因为我上传的第一张是gif动图，文件大，上传多等几秒
        time.sleep(11)
    else:
        time.sleep(2.5)

    # 点击“copy”按钮
    pyautogui.click(297, 545)
    time.sleep(1)

    # 点击浏览器的地址栏
    pyautogui.click(410, 66)

    # 模拟键盘点击ctrl+v，然后按回车键
    pyautogui.hotkey('ctrl','v')
    time.sleep(0.5)
    pyautogui.hotkey('enter')

    #欣赏美女3秒
    time.sleep(3)

    # 点击浏览器的返回按钮
    pyautogui.click(32, 67)
    time.sleep(2)

#文件的x,y坐标
file_list = [(847, 489),(965, 490),(1136, 493),(1271, 504),(1391, 498)]
[ auto_upload(f[0],f[1],'C:/Users/0717/Pictures/blog/upload') for f in file_list]