from selenium import webdriver
import urllib.request

driver = webdriver.Chrome()
driver.get('https://weibo.com/')

driver.get('https://s.weibo.com/weibo/%25E5%25A5%25A5%25E8%25BF%2590%25E4%25BC%259A?topnav=1&wvr=6&b=1')

contents = driver.find_elements_by_xpath(r'//p[@class="txt"]')

for i in range(0,3):
    print("==============================")
    print(contents[i].get_attribute('innerHTML'))

contents = driver.find_elements_by_xpath(r'//img[@action-type="fl_pics"]')

print(len(contents))

for i in range(0,20):
    print("==============================")
    print(contents[i].get_attribute('src'))


for i in range(0,20):
    print("==============================")
    image_url=contents[i].get_attribute('src')
    file_name="downloads//p"+str(i)+".jpg"
    print(image_url,file_name)
    urllib.request.urlretrieve(image_url, filename=file_name)