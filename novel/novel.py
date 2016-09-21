# coding:utf-8
# author： ou

import urllib.request
from bs4 import BeautifulSoup
from txspider import  txmhrul
import demjson as json
import re
import urllib
import time



urlhome="http://m.sfacg.com"
user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'
headers = { 'User-Agent' : user_agent}



#首页数据
def getNovelHome():

    url =urlhome
    req = urllib.request.Request(url, headers = headers)
    response = urllib.request.urlopen(req)
    the_page = response.read()
    # print('the_page:',the_page)
    soup = BeautifulSoup(the_page, 'html.parser')
    # print('soup:',soup)
    book_Contents=soup.find_all("div",{"class":"book_Content_style"})
    for book_Content in book_Contents:
        book_Content_title=book_Content.find("div",{"class":"book_bk_qs1 book_Content_title"})
        print('\n栏目标题:',book_Content_title.text)
        books=book_Content.find_all("a")
        for book in books:
            title=book.text
            href=book.get("href")
            src=book.find("img").get("src")
            print('\ntitle:',title)
            print('href:',href)
            print('src:',src)

#更新
def getUpdata():
    url =urlhome+"/API/HTML5.ashx?op=latest&index=1&_="+str(int(time.time()))
    print('\nurl:',url)
    req = urllib.request.Request(url, headers = headers)
    response = urllib.request.urlopen(req)
    the_page = response.read()
    print('\nthe_page:',the_page)
    # http://m.sfacg.com/API/HTML5.ashx?op=latest&index=1&_=1474442424293


# http://m.sfacg.com/API/HTML5.ashx?op=jpnovels&index=10&listype=latest&_=1474445188394
# http://m.sfacg.com/API/HTML5.ashx?op=jpnovels&index=2&listype=finish&_=1474445335160
# http://m.sfacg.com/API/HTML5.ashx?op=jpnovels&index=1&listype=hot&_=1474445451544
#日轻中的   latest:最新更新  hot：热门推荐   finish完结
def getRQ(type):
    url =urlhome+"/API/HTML5.ashx?op=jpnovels&index=10&listype="+type+"&_="+str(int(time.time()))
    print('\nurl:',url)
    req = urllib.request.Request(url, headers = headers)
    response = urllib.request.urlopen(req)
    the_page = response.read()
    print('\nthe_page:',the_page)



#排行中的这些栏目类型--original:原创 sale 热销 jp：日轻 new：新书 ticket：月票 bm：收藏
def getRanking(type):

    url =urlhome+"/rank/"+type+".html"
    print('\nurl:',url)
    req = urllib.request.Request(url, headers = headers)
    response = urllib.request.urlopen(req)
    the_page = response.read()
    # print('the_page:',the_page)
    soup = BeautifulSoup(the_page, 'html.parser')
    # print('soup:',soup)

    book_list=soup.find_all("div",{"class":"Content_Frame book_list"})
    # print('##book_list:',book_list)
    for book in book_list:
        bookherf=book.parent.get("href")
        src=book.find("img").get("src")
        title=book.find("span",{"id":"book_title"}).text
        # print('\n##title:',title)
        # print('##bookherf:',bookherf)
        # print('##src:',src)





#文章的章节列表
def getNovelCharpterList(herf):

    # url =urlhome+"/i/50076/"
    url=herf
    if herf.startswith(urlhome)==False:
        url =urlhome+herf

    req = urllib.request.Request(url, headers = headers)
    response = urllib.request.urlopen(req)
    the_page = response.read()
    # print('the_page:',the_page)
    soup = BeautifulSoup(the_page, 'html.parser')
    # print('soup:',soup)

    list_menu_title=soup.find_all("div",{"class":"mulu"})
    # print('list_menu_title:',list_menu_title)
    mulu_list=soup.find_all("ul",{"class":"mulu_list"})
    # print('list_Content:',mulu_list)

    for menu_title in list_menu_title:
        print('text:',menu_title.text)

    for menu in mulu_list:
        charpter=menu.find_all("a")
        for c in charpter:
            href=c.get("href")
            title=c.find("li").text
            print('\nhref:',href)
            print('title:',title)
            getNovelDetail(href)




#文章详情
def getNovelDetail(detailurl):
    print('\n开始下载内容')
    url=detailurl
    if detailurl.startswith(urlhome)==False:
        url =urlhome+detailurl
    # url =urlhome+detailurl
    req = urllib.request.Request(url, headers = headers)
    response = urllib.request.urlopen(req)
    the_page = response.read()
    # print('the_page:',the_page)
    soup = BeautifulSoup(the_page, 'html.parser')
    content=soup.find("div",{"class":"yuedu Content_Frame"})

    texts=content.find_all("p")
    tempText=content.text
    contentList=[]
    for text in texts:
        contentList.append(text.text)
        # print('text:',text.text)

    index=tempText.find(contentList[0])
    textfirst=""
    if index>1:
        textfirst=tempText[0:index]

    contentList.insert(0,textfirst)
    contentAll=""
    for contenttext in contentList:
        contentAll=contentAll+contenttext+"\n"
    try:
        print('\n完整内容：'+contentAll)
    except (UnicodeEncodeError):
            print('\n编码报错')
    except:
           print('\n\n出错了！')
#搜索
def search(key):
    key=urllib.request.quote(key)
    url =urlhome+"/API/HTML5.ashx?op=search&keyword="+key+"&_="+str(int(time.time()))
    print('\nurl:',url)
    req = urllib.request.Request(url, headers = headers)
    response = urllib.request.urlopen(req)
    the_page = response.read()
    print('\nthe_page:',the_page)


if __name__ == '__main__':
    # original:原创 sale 热销 jp：日轻 new：新书 ticket：月票 bm：收藏
    getRanking("original")
    # getRanking("sale")
    # getRanking("jp")
    # getRanking("new")
    # getRanking("ticket")
    # getRanking("bm")

    # getUpdata()
    # getNovelHome()
    # getNovelCharpterList("/i/50076/")
    # getNovelDetail("/c/807732/")

    # search("热血")