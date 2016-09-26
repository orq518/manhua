# coding:utf-8
# author： ou
import urllib.request
import urllib
import time
from bs4 import BeautifulSoup
import re
import json

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

        homedata=[]
        for book_Content in book_Contents:

            lanmu={}
            book_Content_title=book_Content.find("div",{"class":"book_bk_qs1 book_Content_title"})
            content_title=book_Content_title.text;

            print('\n栏目标题:',book_Content_title.text)

            books=book_Content.find_all("a")
            lanmu["title"]=content_title
            booksList=[]
            for book in books:
                bookmap={}
                title=book.text
                href=book.get("href")
                src=book.find("img").get("src")
                id=re.findall(r'\d+',href)[0]
                bookmap["title"]=title
                bookmap["href"]=href
                bookmap["src"]=src
                bookmap["id"]=id

                booksList.append(bookmap)
                print('\ntitle:',title)
                print('href:',href)
                print('src:',src)
                print('id:',id)
            lanmu["books"]=booksList
            homedata.append(lanmu)
        return  homedata




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
        data=[]
        for book in book_list:
            bookmap={}
            bookherf=book.parent.get("href")
            src=book.find("img").get("src")
            title=book.find("span",{"id":"book_title"}).text
            bookmap["title"]=title
            bookmap["href"]=bookherf
            bookmap["src"]=src
            id=re.findall(r'\d+',bookherf)[0]
            bookmap["id"]=id
            data.append(bookmap)
            # print('\n##title:',title)
            # print('##bookherf:',bookherf)
            # print('##src:',src)

        return  data


    #文章的章节列表
    def getNovelCharpterList(self,index):

        # url =urlhome+"/i/50076/"
        url=self.urlhome+"/i/"+str(index)+"/"

        req = urllib.request.Request(url, headers = self.headers)
        response = urllib.request.urlopen(req)
        the_page = response.read()
        # print('the_page:',the_page)
        soup = BeautifulSoup(the_page, 'html.parser')
        # print('soup:',soup)

        list_menu_title=soup.find_all("div",{"class":"mulu"})
        # print('list_menu_title:',list_menu_title)
        mulu_list=soup.find_all("ul",{"class":"mulu_list"})
        print('list_Content:',mulu_list)

        data=[]
        menuTitleList=[]
        for menu_title in list_menu_title:
            title=menu_title.text;
            menuTitleList.append(title)
            print('text:',title)
            print('list长度:',len(menuTitleList))

        index=0
        for menu in mulu_list:
            charpterMap={}
            charpter=menu.find_all("a")
            print('#title:',menuTitleList[index])
            print('#index:',index)
            charpterMap["title"]=menuTitleList[index]
            index+=1
            charpterList=[]
            for c in charpter:
                cMap={}
                href=c.get("href")
                title=c.find("li").text
                id=re.findall(r'\d+',href)[0]
                cMap["id"]=id
                cMap["href"]=href
                cMap["title"]=title
                charpterList.append(cMap)
                print('\nhref:',href)
                print('title:',title)
                # getNovelDetail(href)
            charpterMap["charpter"]=charpterList
            data.append(charpterMap)
        return  data




    #文章详情
    def getNovelDetail(self,index):
        print('\n开始下载内容')
        url=self.urlhome+"/c/"+str(index)+"/"
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

        return contentAll



    #####============以下几个接口可以通过程序自己调用api=======================
    #搜索
    def search(self,key):
        key=urllib.request.quote(key)
        url =self.urlhome+"/API/HTML5.ashx?op=search&keyword="+key+"&_="+str(int(time.time()))
        print('\nurl:',url)
        req = urllib.request.Request(url, headers = self.headers)
        response = urllib.request.urlopen(req)
        the_page = response.read()
        data=the_page.decode("utf-8")
        # print('\ndata:',data)
        jsondata = json.loads(data)
        datalist=[]
        datalist=jsondata.get("Novels")
        print('\nhjson:',datalist)
        return datalist

 # http://m.sfacg.com/API/HTML5.ashx?op=jpnovels&index=10&listype=latest&_=1474445188394
    # http://m.sfacg.com/API/HTML5.ashx?op=jpnovels&index=2&listype=finish&_=1474445335160
    # http://m.sfacg.com/API/HTML5.ashx?op=jpnovels&index=1&listype=hot&_=1474445451544
    #日轻中的   latest:最新更新  hot：热门推荐   finish完结
    def getRQ(self,type,index):

        url =self.urlhome+"/API/HTML5.ashx?op=jpnovels&index="+str(index)+"&listype="+type+"&_="+str(int(time.time()))
        print('\nurl:',url)
        req = urllib.request.Request(url, headers = self.headers)
        response = urllib.request.urlopen(req)
        the_page = response.read()
        data=the_page.decode("utf-8")
        # print('\ndata:',data)
        jsondata = json.loads(data)
        datalist=[]
        datalist=jsondata
        return datalist
        #更新
    def getUpdate(self,index):
        url =self.urlhome+"/API/HTML5.ashx?op=latest&index="+str(index)+"&_="+str(int(time.time()))
        print('\nurl:',url)
        req = urllib.request.Request(url, headers = self.headers)
        response = urllib.request.urlopen(req)
        the_page = response.read()
        data=the_page.decode("utf-8")
        # print('\ndata:',data)
        jsondata = json.loads(data)
        datalist=[]
        datalist=jsondata
        return datalist
        # http://m.sfacg.com/API/HTML5.ashx?op=latest&index=1&_=1474442424293

    def getGirlsData(self,page):
        key=urllib.request.quote("福利")
        url="http://gank.io/api/data/"+key+"/20/"+str(page)
        # url =self.urlhome+"/API/HTML5.ashx?op=latest&index="+str(index)+"&_="+str(int(time.time()))
        print('\nurl:',url)
        req = urllib.request.Request(url, headers = self.headers)
        response = urllib.request.urlopen(req)
        the_page = response.read()
        # print('the_page:',the_page)
        data=the_page.decode("utf-8")
        # print('data:',data)
        jsondata = json.loads(data)
        datalist=[]
        datalist=jsondata.get("results")
        # print('\nhjson:',datalist)
        return datalist



