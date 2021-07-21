from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time,base64
import chaojiying
from selenium.webdriver import ActionChains

class Ticket(object):

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.login_url = 'https://kyfw.12306.cn/otn/resources/login.html'

    
    def findElement(self, type, id):
        # 查找元素
        return EC.visibility_of_element_located((type, id))

    def login(self):
        self.driver = webdriver.Chrome(executable_path='D:\chromedriver.exe')

        with open('D:\stealth.min.js') as f:
            stealth = f.read()
        self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {"source": stealth})

        self.wait = WebDriverWait(self.driver, 10, 0.1)
        self.driver.get(self.login_url)
        
        self.wait.until(self.findElement(By.LINK_TEXT,'账号登录')).click()

        self.wait.until(self.findElement(By.ID, 'J-userName')).send_keys(self.username)
        
        self.wait.until(self.findElement(By.ID, 'J-password')).send_keys(self.password)

        success_flag = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'lgcode-success'))).get_attribute('style')
        while success_flag == 'display: none;':
            img = self.wait.until(EC.visibility_of_element_located((By.ID, 'J-loginImg')))

            base64Img = img.get_attribute('src')
            base64Img = base64Img.replace('data:image/jpg;base64,', '')
            imgdata=base64.urlsafe_b64decode(base64Img)
            file=open('1.jpg','wb')
            file.write(imgdata)
            file.close()

            cj = chaojiying.Chaojiying_Client('用户名', '密码', '软件ID')
            im = open('1.jpg', 'rb').read()
            cjy_result = cj.PostPic(im, 9004)
            print(cjy_result)											
            x_y = cjy_result['pic_str']
            pic_id = cjy_result['pic_id']

            all_list = []
            for i in x_y.split('|'):
                all_list.append([int(i.split(',')[0]), int(i.split(',')[1])])

            for rangle in all_list:
                ActionChains(self.driver).move_to_element_with_offset(img, rangle[0], rangle[1]).click().perform()

            self.wait.until(self.findElement(By.ID, 'J-login')).click()
            success_flag = self.driver.find_element_by_class_name('lgcode-success').get_attribute('style')

            if success_flag == 'display: none;':
                cj.ReportError(pic_id)

        nc_1_n1z = self.wait.until(self.findElement(By.ID, 'nc_1_n1z'))
        tracks = [6,16,31,52,72,52,62,50]
    
        action = ActionChains(self.driver)
    
        action.click_and_hold(nc_1_n1z).perform()
        for track in tracks:
            action.move_by_offset(track, 0)
        time.sleep(0.5)
        action.release().perform()

if __name__ == '__main__':
    username = 'xxxx'
    password = 'xxxdddxx'

    ticket = Ticket(username, password)
    ticket.login()

