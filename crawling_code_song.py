from urllib.request import urlretrieve
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from selenium import webdriver
import time

search = input('검색할 단어? ')

url = f'https://www.google.co.kr/search?as_st=y&tbm=isch&hl=ko&as_q={quote_plus(search)}&as_epq=&as_oq= \
&as_eq=&cr=&as_sitesearch=&safe=images&tbs=itp:face'
# &source=lnms&tbm=isch&sa=X&ved=\ 2ahUKEwjG-Jept4vpAhUPvZQKHfx-AIEQ_AUoAXoECBYQAw&biw=1920&bih=969 -그냥 검색
# &as_epq=&as_oq=&as_eq=&cr=&as_sitesearch=&safe=images&tbs=itp:face                                -세부 검색
driver = webdriver.Chrome('D:/lab_document/pycharm_data/chromedriver_win32/chromedriver.exe')
driver.get(url)

"""
time.sleep(3)
driver.find_element_by_xpath('//*[@id="ow21"]/a/div').click()  # 설정클릭
time.sleep(3)
driver.find_element_by_xpath('//*[@id="lb"]/div/a[3]').click()  # 고급검색 클릭
time.sleep(3)
driver.find_element_by_xpath('//*[@id=":7v"]/div').click()  # 모든 유형 클릭
driver.find_element_by_xpath('//*[@id=":7w"]/div').click()  # 얼굴 선택
driver.find_element_by_xpath('/html/body/div[1]/div[5]/form/div[5]/div[10]/div[2]/input').click()  # 검색 버튼 클릭
time.sleep(3)
"""

for i in range(5):
    last_height = driver.execute_script("return document.body.scrollHeight")
    driver.execute_script('window.scrollBy(0,10000)')
    time.sleep(3)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if last_height == new_height:
        print("wait")
        Advanced_settings = driver.find_element_by_xpath(
            '// *[ @ id = "islmp"] / div / div / div / div / div[5] / input')
        Advanced_settings.click()
        time.sleep(3)
    last_height = new_height
# driver.find_element_by_xpath('//*[@id="islmp"]/div/div/div/div/div[4]/div[2]/div[1]/div')
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
    urlretrieve(i, './picture/토끼상/' + search + str(n) + '.jpg')
    n += 1
    print(imgurl)
    if n == 200:  # 만약 120개에서 멈추고 싶다면.
        break
driver.close()
