from urllib.request import urlopen
from urllib.request import urlretrieve
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from selenium import webdriver

# 이 방법은 최대 400개까지 이미지 크롤링을 하는 방법이다.

search = input('which picture do you want? ')

url = f'https://www.google.com/search?q={quote_plus(search)}&source=lnms&tbm=isch&sa=X&ved=\
2ahUKEwjG-Jept4vpAhUPvZQKHfx-AIEQ_AUoAXoECBYQAw&biw=1920&bih=969'
# 각 컴퓨터 크롬에 들어가서 dog라 검색하고 이미지 들어가서 주소를 더블 클릭한다. 그 주소를 복사하여
# 위의 코드에 붙인다

driver = webdriver.Chrome('D:/lab_document/pycharm_data/chromedriver_win32/chromedriver.exe')
# 크롬의 버젼을 확인하고 그에 맞는 웹 드라이버를 다운 한 다음 주소를 복사한다.
driver.get(url)
for i in range(500):
    driver.execute_script("window.scrollBy(0, 10000)")

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
    urlretrieve(i, './crawlingImages/cat/' + search + str(n) + '.jpg')  # 크롤링할 폴더의 디렉토리를 입력한다.
    n += 1
    print(imgurl)
    if n == 120:  # 만약 120개에서 멈추고 싶다면.
        break
driver.close()
