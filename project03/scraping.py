from selenium import webdriver
from bs4 import BeautifulSoup
import time
from selenium.common.exceptions import NoSuchElementException
from pymongo import MongoClient
import requests

# client = MongoClient('13.209.18.100', 27017, username="test", password="test")
client = MongoClient("mongodb://localhost:27017/")
db = client.dbsparta_plus_week3

driver = webdriver.Chrome('./chromedriver')

url = "http://matstar.sbs.co.kr/location.html"

driver.get(url)
time.sleep(5)
#더 보기 버튼의 선택자로 버튼 클릭
# Please use find_element(by=By.CSS_SELECTOR, value=css_selector) instead
for i in range(10):
    try:
        btn_more = driver.find_element_by_css_selector("#foodstar-front-location-curation-more-self > div > button")
        btn_more.click()
        time.sleep(5)
    except NoSuchElementException:
        break

req = driver.page_source
driver.quit()

soup = BeautifulSoup(req, 'html.parser')

# 각 식당에 해당하는 카드 선택
places = soup.select("ul.restaurant_list > div > div > li > div > a")
print(len(places))

# 식당 이름, 주소, 카테고리, 출연 프로그램과 회차 정보
for place in places:
    title = place.select_one("strong.box_module_title").text
    address = place.select_one("div.box_module_cont > div > div > div.mil_inner_spot > span.il_text").text
    category = place.select_one("div.box_module_cont > div > div > div.mil_inner_kind > span.il_text").text
    show, episode = place.select_one("div.box_module_cont > div > div > div.mil_inner_tv > span.il_text").text.rsplit(" ", 1)
    print(title, address, category, show, episode)
    #지오코딩 연결하기
    headers = {
        "X-NCP-APIGW-API-KEY-ID": "98hquhx0x7",
        "X-NCP-APIGW-API-KEY": "gOPbsaUYxHdcFsmFsAQ2IW3cMzPQYM7EX4Rjgp8q"
    }
    r = requests.get(f"https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode?query={address}", headers=headers)
    response = r.json()
    # 결과 출력하기
    if response["status"] == "OK":
        if len(response["addresses"]) > 0:
            x = float(response["addresses"][0]["x"])
            y = float(response["addresses"][0]["y"])
            print(title, address, category, show, episode, x, y)
            #디비에 저장하기
            doc = {
                "title": title,
                "address": address,
                "category": category,
                "show": show,
                "episode": episode,
                "mapx": x,
                "mapy": y}
            db.matjips.insert_one(doc)


        else:
            print(title, "좌표를 찾지 못했습니다")