import time

from appium import webdriver
from selenium.common.exceptions import NoSuchElementException

desired_capabilities = {
    'platformName': 'Android', # 操作系统
    'deviceName': '2a254a02', # 设备 ID
    'platformVersion': '10.0.10', # 设备版本号，在手机设置中查看
    'appPackage': 'com.tencent.mm', # app 包名
    'appActivity': 'com.tencent.mm.ui.LauncherUI', # app 启动时主 Activity
    'noReset': True # 是否保留 session 信息 避免重新登录
}

driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_capabilities)
print('微信启动')



# 所有好友
friends = ['宝贝']
def get_friends():
    # 好友id
    address_list = driver.find_elements_by_id('com.tencent.mm:id/dy5')
    for address in address_list:
        # 昵称
        friend = address.get_attribute('content-desc')
        # 过滤掉自己、微信团队、文件夹传输助手
        if friend != '某某白米饭' and friend != '微信团队' and friend != '文件夹传输助手':
            friends.append(friend)
        # 获取到最后一个好友返回
        if friend == '🔥Jiuki🔥':
            return
    # 向上滚动获取好友，获取好友会重复，最后结果需过滤
    driver.swipe(100, 1000, 100, 500)
    # 递归循环得到所有好友
    get_friends()
    pass

# 判断是否被删
def is_del(f):

    time.sleep(2)
    driver.find_element_by_id('com.tencent.mm:id/cn1').click()
    time.sleep(2)
    # 在搜索框输入搜索信息
    driver.find_element_by_id('com.tencent.mm:id/bhn').send_keys(f)
    time.sleep(2)
    #点击好友
    driver.find_element_by_id('com.tencent.mm:id/tm').click()
    time.sleep(2)
    # 转账操作 + 号
    driver.find_element_by_id('com.tencent.mm:id/aks').click()
    time.sleep(2)
    # 转账按钮
    driver.find_elements_by_id('com.tencent.mm:id/pa')[5].click()
    time.sleep(2)
    # 数字 1
    driver.find_element_by_id('com.tencent.mm:id/cx_').click()
    time.sleep(1)
    # 付款界面转账按钮
    driver.find_element_by_id('com.tencent.mm:id/cxi').click()
    time.sleep(2)

    # 判断是否被删
    is_exist = is_element('com.tencent.mm:id/dos')
    if is_exist:
        # 不能转账就点击确定按钮
        driver.find_element_by_id('com.tencent.mm:id/doz').click()

        time.sleep(2)
    else:
        # 可以转账就后退
        driver.press_keycode(4)

    # 后退到 搜索页面
    driver.press_keycode(4)
    driver.press_keycode(4)
    driver.press_keycode(4)
    driver.press_keycode(4)
    # 清空文本框
    driver.find_element_by_id('com.tencent.mm:id/bhn').send_keys('')

    return is_exist


# 删除好友
def del_friend(friend):
    time.sleep(2)
    driver.find_element_by_id('com.tencent.mm:id/cn1').click()
    time.sleep(2)
    driver.find_element_by_id('com.tencent.mm:id/bhn').send_keys(friend)
    time.sleep(2)
    #点击好友
    driver.find_element_by_id('com.tencent.mm:id/tm').click()
    time.sleep(2)
    # 右上角...
    driver.find_element_by_id('com.tencent.mm:id/cj').click()
    time.sleep(2)
    # 头像
    driver.find_element_by_id('com.tencent.mm:id/f3y').click()
    time.sleep(2)
    # 右上角...
    driver.find_element_by_id('com.tencent.mm:id/cj').click()
    time.sleep(2)
    # 删除按钮
    driver.find_element_by_id('com.tencent.mm:id/g6f').click()
    time.sleep(2)
    # 选中删除
    driver.find_element_by_id('com.tencent.mm:id/doz').click()

def is_element(id):
    flag = None
    try:
        driver.find_element_by_id(id)
        flag = True
    except NoSuchElementException:
        flag = False
    finally:
        return flag

time.sleep(8)
driver.find_elements_by_id('com.tencent.mm:id/cn_')[1].click()

time.sleep(3)
get_friends()
friends = list(set(friends))

del_friends = []
for f in friends:
    is_exist = is_del(f)
    if is_exist:
        del_friends.append(f)

for f in del_friends:
    del_friend(f)