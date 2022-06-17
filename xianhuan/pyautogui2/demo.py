import pyautogui

# 图像识别（一个）
oneLocation = pyautogui.locateOnScreen('1.png')
print(oneLocation)  
# 图像识别（多个）
allLocation = pyautogui.locateAllOnScreen('1.png')
print(allLocation)
print(list(allLocation))
for left,top,width,height in pyautogui.locateAllOnScreen('1.png'):
    print(1)
    print(left)