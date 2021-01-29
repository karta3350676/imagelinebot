import os
import re
from bs4 import BeautifulSoup
from urllib import request
import requests
import random
import psycopg2

getOne = ''
def exchangeRate(country):
    rateString = ""
    resp = requests.get('http://www.findrate.tw/'+country+'/')
    resp.encoding = "utf-8"
    soup = BeautifulSoup(resp.text, 'html.parser')
    first_table = soup.find('table')
    index = 0
    main_tr = first_table.find_all('tr')
    for title in main_tr:
        index = index + 1
        if index == 2:
            temp = ""
            tdNum = 0
            main_td = title.find_all("td")
            for td in main_td:
                tdNum = tdNum + 1
                if tdNum != 4:
                    temp = temp + td.text + "|"

            temp = temp + "\n"
            rateString += temp

        if index == 3:
            temp = ""
            tdNum = 0
            main_td = title.find_all("td")
            for td in main_td:
                tdNum = tdNum + 1
                if tdNum != 4:
                    temp = temp + td.text + "|"

            temp = temp + "\n"
            rateString += temp

    rateString += "\n連結:http://www.findrate.tw/"+country+"/"
    return rateString

def getImage(url):
    print(url)
    mheaders = {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}
    req = request.Request(url, headers=mheaders)  # 新增headers避免伺服器拒絕非瀏覽器訪問
    page = request.urlopen(req)
    html = page.read()
    soup = BeautifulSoup(html.decode('utf-8'), 'html.parser')
    body = soup.find(class_='main-image')
    img = body.find('img').get('src')

    return  img

def getUrl(url):
    print("getCk101Url url:" + url)
    # 瀏覽器請求頭（大部分網站沒有這個請求頭可能會報錯）
    index = []
    mheaders = {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}
    req = request.Request(url,headers=mheaders) #新增headers避免伺服器拒絕非瀏覽器訪問
    page = request.urlopen(req)
    html = page.read()
    soup = BeautifulSoup(html.decode('utf-8'), 'html.parser')
    main = soup.find('div','bt-main-cont')
    search_li = main.find_all('li')
    for li in search_li:
        element = li.find('a').get('href')
        if not element is None:
            index.append(element)

    getOne = index[random.randrange(0, len(index)-1)]
    print("getCk101Url back url :" + getOne)
    return getOne

def getPhoto(url):
    print("photo url:"+url)
    index = []
    mheaders = {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}
    req = request.Request(url, headers=mheaders)  # 新增headers避免伺服器拒絕非瀏覽器訪問
    page = request.urlopen(req)
    html = page.read()
    soup = BeautifulSoup(html.decode('utf-8'), 'html.parser')
    main_table = soup.find(id = 'lightboxwrap')
    img_all = main_table.find_all('img')

    for img in img_all:
        element = img.get('file')
        if not element is None:
            index.append(element)

    getOne = index[random.randint(0, len(index)-1)]
    print("photo back url :" + getOne)
    return getOne

def getpttPhoto(url):
    print("photo url:"+url)
    index = []
    header = {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}
    res = requests.get(url, headers=header, cookies={'over18': '1'})  # 新增headers避免伺服器拒絕非瀏覽器訪問
    soup = BeautifulSoup(res.text, 'html.parser')
    titleSoupList = soup.select('div.title a')
    for titleSoup in titleSoupList:
        title = titleSoup.text
        articleUrl = 'https://www.ptt.cc' + titleSoup['href']
        if '[正妹]' in title:
            if '肉特' or '[神人]' not in title:
                            # print(title)
                            resArticle = requests.get(articleUrl, headers=header, cookies={'over18': '1'})
                            soupArticle = BeautifulSoup(resArticle.text, 'html.parser')
                            links = soupArticle.find(id='main-content').find_all('a')
                            try:
                                for link in links:
                                    # 找尋符合的 img 圖片網址
                                    if re.match(r'^https?://(i.)?(m.)?imgur.com', link['href']):
                                        img_url = link['href']
                                        index.append(img_url)
                                            # return index
                                getOne = index[random.randint(0, len(index) - 1)]
                                print("photo back url :" + getOne)
                            except:
                                pass
                            return getOne
if __name__ == '__main__':
    # Test Function
    # IgUrl = "https://www.instagram.com/p/BymVt2NH5OE/?igshid=7jpeb1f596h6"
    # IString = exchangeRate("JPY")
    IArray = getPhoto('https://ck101.com/thread-5017396-1-1.html')
    # IArray = getImage('https://www.mzitu.com/187752/16')
    # SData = randomIgImage()
    print(IArray)
    PTT_URL = 'https://www.ptt.cc'
    keyword = str(random.randrange(0, 3544, 1))
    ptturl = 'https://www.ptt.cc/bbs/Beauty/index' + keyword + '.html'
    pttimg = getpttPhoto(ptturl)
    print(pttimg)