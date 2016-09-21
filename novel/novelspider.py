# coding:utf-8
# author： ou
import urllib.request
import urllib
import time

from bs4 import BeautifulSoup


class NovelSpider(object):
    def __init__(self):
        self.urlhome="http://m.sfacg.com"
        self.user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'
        self.headers = { 'User-Agent' : self.user_agent}


    #首页数据
    def getNovelHome(self):

        url =self.urlhome
        req = urllib.request.Request(url, headers = self.headers)
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

    # http://m.sfacg.com/API/HTML5.ashx?op=jpnovels&index=10&listype=latest&_=1474445188394
    # http://m.sfacg.com/API/HTML5.ashx?op=jpnovels&index=2&listype=finish&_=1474445335160
    # http://m.sfacg.com/API/HTML5.ashx?op=jpnovels&index=1&listype=hot&_=1474445451544
    #日轻中的   latest:最新更新  hot：热门推荐   finish完结
    def getRQ(self,type,index):
        url =self.urlhome+"/API/HTML5.ashx?op=jpnovels&index="+index+"&listype="+type+"&_="+str(int(time.time()))
        print('\nurl:',url)
        req = urllib.request.Request(url, headers = self.headers)
        response = urllib.request.urlopen(req)
        the_page = response.read()
        print('\nthe_page:',the_page)


    #排行中的这些栏目类型--original:原创 sale 热销 jp：日轻 new：新书 ticket：月票 bm：收藏
    def getRanking(self,type):

        url =self.urlhome+"/rank/"+type+".html"
        print('\nurl:',url)
        req = urllib.request.Request(url, headers = self.headers)
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
    def getNovelCharpterList(self,herf):

        # url =urlhome+"/i/50076/"
        url=herf
        if herf.startswith(self.urlhome)==False:
            url =self.urlhome+herf

        req = urllib.request.Request(url, headers = self.headers)
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
                # getNovelDetail(href)




    #文章详情
    def getNovelDetail(self,detailurl):
        print('\n开始下载内容')
        url=detailurl
        if detailurl.startswith(self.urlhome)==False:
            url =self.urlhome+detailurl
        # url =urlhome+detailurl
        req = urllib.request.Request(url, headers = self.headers)
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
    def search(self,key):
        key=urllib.request.quote(key)
        url =self.urlhome+"/API/HTML5.ashx?op=search&keyword="+key+"&_="+str(int(time.time()))
        print('\nurl:',url)
        req = urllib.request.Request(url, headers = self.headers)
        response = urllib.request.urlopen(req)
        the_page = response.read()
        print('\nthe_page:',the_page)


        #更新
    def getUpdata(self,index):
        url =self.urlhome+"/API/HTML5.ashx?op=latest&index="+index+"&_="+str(int(time.time()))
        print('\nurl:',url)
        req = urllib.request.Request(url, headers = self.headers)
        response = urllib.request.urlopen(req)
        the_page = response.read()
        print('\nthe_page:',the_page)
        # http://m.sfacg.com/API/HTML5.ashx?op=latest&index=1&_=1474442424293



