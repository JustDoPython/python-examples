from appium import webdriver

desired_capabilities = {
    "platformName": "Android", # 操作系统
    "deviceName": "emulator-5554", # 设备 ID
    "platformVersion": "6.0.1", # 设备版本号
    "appPackage": "com.tencent.mm", # app 包名
    "appActivity": "com.tencent.mm.ui.LauncherUI", # app 启动时主 Activity
    'noReset': True # 是否保留 session 信息 可以避免重新登录
}

driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_capabilities)
print('链接到安卓模拟器')
time.sleep(5)

driver.find_element_by_id('com.tencent.mm:id/f8y').click()
print('查找搜索按钮')
time.sleep(3)

driver.find_element_by_id('com.tencent.mm:id/bhn').send_keys('Python 技术')
print('查找搜索输入框 & 写入搜索关键字')
time.sleep(3)

driver.find_element_by_id('com.tencent.mm:id/tm').click()
print('点击 icon 图标')
time.sleep(3)

driver.find_element_by_id('com.tencent.mm:id/cj').click()
print('点击右上角头像')
time.sleep(3)

driver.find_element_by_id('com.tencent.mm:id/a1u').click()
print('点击第一篇文章')