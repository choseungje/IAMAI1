from urllib.request import urlretrieve
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from selenium import webdriver
import time

search = input('검색할 단어? ')

# 고급검색 : 얼굴
url = f'https://www.google.co.kr/search?as_st=y&tbm=isch&hl=ko&as_q={quote_plus(search)}&as_epq=&as_oq=&as_eq=&cr=&as_sitesearch=&safe=images&tbs=itp:face'
# 고급검색 없음
# url = f'https://www.google.co.kr/search?as_st=y&tbm=isch&hl=ko&as_q={quote_plus(search)}&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjb5fGhxprpAhXLdd4KHcm1BvAQ_AUoAXoECBcQAw&biw=1920&bih=969'

driver = webdriver.Chrome('C:/Users/syslab/Desktop/chromedriver/chromedriver.exe')
driver.get(url)

for i in range(2):
    last_height = driver.execute_script("return document.body.scrollHeight")
    driver.execute_script('window.scrollBy(0,10000)')
    time.sleep(3)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if last_height == new_height:
        print("wait")
        Advanced_settings = driver.find_element_by_xpath('// *[ @ id = "islmp"] / div / div / div / div / div[5] / input')
        Advanced_settings.click()
        time.sleep(3)
    print(str((i + 1) * 100))


html = driver.page_source
soup = BeautifulSoup(html)

img = soup.select('.rg_i.Q4LuWd.tx8vtf')
n = 1
imgurl = []
for i in img:
    try:
        imgurl.append(i.attrs["src"])
    except KeyError:
        imgurl.append(i.attrs["data-src"])

for i in imgurl:
    urlretrieve(i, './picture/'+ search + str(n) +'.jpg')
    n += 1
    print(i)
driver.close()