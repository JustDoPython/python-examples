import time

from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.support import expected_conditions as EC

desired_capabilities = {
    'platformName': 'Android', # 操作系统
    'deviceName': '2a254a02', # 设备 ID
    'platformVersion': '10.0.10', # 设备版本号，在手机设置中查看
    'appPackage': 'com.tencent.mm', # app 包名
    'appActivity': 'com.tencent.mm.ui.LauncherUI', # app 启动时主 Activity
    'noReset': True # 是否保留 session 信息 避免重新登录
}

# 判断元素是否存在
def is_element_exist_by_xpath(driver, text):
    try:
        driver.find_element_by_xpath(text)
    except Exception as e:
        return False
    else:
        return True

if __name__ == '__main__':
    driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_capabilities)
    # 设置等待超时时间
    wait = WebDriverWait(driver, 60)

    while True:
        time.sleep(0.5)

        # 进入第一个聊天框
        red_packet_group = driver.find_elements_by_id('com.tencent.mm:id/e3x')[0]
        red_packet_group.click()

        # 检查红包
        reds = driver.find_elements_by_id('com.tencent.mm:id/r2')
        if len(reds) == 0:
            driver.keyevent(4)
        else:
            for red in reds[::-1]:
                red.click()
                # 领取了
                is_open = is_element_exist_by_xpath(driver, '//android.widget.TextView[contains(@text, "已存入零钱")]')
                # 没抢到
                is_grabbed = is_element_exist_by_xpath(driver, '//android.widget.TextView[contains(@text, "手慢了")]')

                if is_open or is_grabbed:
                    driver.keyevent(4)
                else:
                    wait.until(EC.element_to_be_clickable((By.ID, "com.tencent.mm:id/den"))).click()
                    wait.until(EC.element_to_be_clickable((By.ID, "com.tencent.mm:id/dm"))).click()

                TouchAction(driver).long_press(red).perform()
                wait.until(EC.element_to_be_clickable((By.ID, "com.tencent.mm:id/gam"))).click()
                wait.until(EC.element_to_be_clickable((By.ID, "com.tencent.mm:id/doz"))).click()
            driver.keyevent(4)