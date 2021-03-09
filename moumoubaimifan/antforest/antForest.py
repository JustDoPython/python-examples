import time

from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from appium.webdriver.common.touch_action import TouchAction

desired_capabilities = {
        'platformName': 'Android',  # 操作系统
        'deviceName': '2a254a02',  # 设备 ID
        'platformVersion': '10.0.10',  # 设备版本号，在手机设置中查看
        'appPackage': 'com.eg.android.AlipayGphone',  # app 包名
        'appActivity': 'AlipayLogin',  # app 启动时主 Activity
        'noReset': True  # 是否保留 session 信息 避免重新登录
    }

# 判断元素是否存在
def is_element_exist_by_xpath(driver, text):
    try:
        driver.find_element_by_xpath(text)
    except Exception as e:
        return False
    else:
        return True

# 收取能量
def collect_energy(driver, width, height):
    # 能量球可能出现的区域坐标
    start_x = 150
    end_x = 900
    start_y = 540
    end_y = 900

    for x in range(start_x, end_x, 50):
        for y in range(start_y, end_y, 50):
            x_scale = int((int(x) / width) * width)
            y_scale = int((int(y) / height) * height)
            # 点击指定坐标
            TouchAction(driver).press(x=x_scale, y=y_scale).release().perform()
    print('能量收取完毕')

def search_energy(driver, width, height):

    x = int((int(1000) / width) * width)
    y = int((int(1550) / height) * height)
    # 点击指定坐标
    TouchAction(driver).press(x=x, y=y).release().perform()
    time.sleep(1)
    is_collected = is_element_exist_by_xpath(driver, '//android.widget.Button[contains(@text, "返回我的森林")]')
    if is_collected:
        print('能量全部收集完毕')
        return

    collect_energy(driver, width, height)
    search_energy(driver, width, height)



if __name__ == '__main__':

    driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_capabilities)
    print('支付宝启动')
    # 设置等待超时时间
    wait = WebDriverWait(driver, 60)

    wait.until(EC.element_to_be_clickable((By.ID, 'com.alipay.android.phone.openplatform:id/more_app_icon'))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, '//android.widget.TextView[contains(@text, "蚂蚁森林")]'))).click()
    time.sleep(3)
    # 获取手机屏幕宽高
    width = int(driver.get_window_size()['width'])
    height = int(driver.get_window_size()['height'])

    collect_energy(driver, width, height)

    search_energy(driver, width, height)
