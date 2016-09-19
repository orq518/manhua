# coding:utf-8
# author： ou
import urllib.request
from bs4 import BeautifulSoup
from txspider import  txmhrul
import demjson as json


#首页数据
class HomePage(object):
    def __init__(self):
        self.urlhome =txmhrul.urlhome
        self.user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'
        self.headers = { 'User-Agent' : self.user_agent}

    #首页数据
    def get_home_data(self):
        # print('gamedate_url:',gamedate_url)
        req = urllib.request.Request(self.urlhome, headers = self.headers)
        response = urllib.request.urlopen(req)
        the_page = response.read()
        # print('the_page:',the_page)
        soup = BeautifulSoup(the_page, 'html.parser')

        homedata={}

        binnerdata=soup.find("ul",{"class":"banner-list"})#binner
        homedata["binnerdata"]=self.get_home_binner(binnerdata)

        todayupdate=soup.find("section",{"class":"update-today"})#今日更新
        homedata["todayupdate"]=self.get_home_todayupdata(todayupdate)

        timelist=soup.find("section",{"class":"time-list"})#追更入口
        homedata["timelist"]=self.get_home_zgdata(timelist)

        japancomic=soup.find("section",{"class":"japan-comic"})#日漫推荐
        homedata["japancomic"]=self.get_home_japancomic(japancomic)

        newcomic=soup.find("section",{"class":"new-comic"})#新作推荐
        homedata["newcomic"]=self.get_home_newcomic(newcomic)

        animation=soup.find("section",{"class":"animation"})#动画专区
        homedata["animation"]=self.get_home_animation(animation)


        data={}
        data["state"]="0"
        data["msg"]="成功"
        data["data"]=homedata
        jsondata=json.encode(data,"utf8")
        print('\n##生成首页json数据:\n',jsondata)

        return jsondata


    #binner
    def get_home_binner(self,binnerdata):
        data=[]
        binners=binnerdata.find_all("a",{"class":"link"})
        for binner in binners:
            # print('\n##japan:',japan)
            contentdata={}
            href=binner.get('href')#链接
            if href.endswith('.html'):
                continue
            title=binner.get('title')#标题
            img=binner.find("img",{"class":"cover"}).get('src')#图片

            print('\n##binner_title:',title)
            print('##href:',href)
            print('##img:',img)

            contentdata["title"]=title
            contentdata["img"]=img
            contentdata["href"]=href
            data.append(contentdata)
        return data


    #今日更新
    def get_home_todayupdata(self,todayupdate):
        # print('##今日更新:',todayupdate)
        data=[]
        moredata={}

        moreTitle=todayupdate.find("strong",{"class":"title-content"}).text#今日更新更多标题
        moreLink=todayupdate.find("a",{"class":"link-more"}).get('href')#今日更新更多链接
        moreDes=todayupdate.find("small",{"class":"desc"}).text#今日更新描述

        # print('\n##今日更新Title:',moreTitle)
        # print('##more:',moreLink)
        # print('##moreDes:',moreDes)

        moredata["moreTitle"]=moreTitle
        moredata["moreLink"]=moreLink
        moredata["moreDes"]=moreDes
        data.append(moredata)

        moreContent=todayupdate.find("div",{"class":"update-area"}).find_all("a",{"class":"comic-link"})#今日更新内容
        for today in moreContent:
            # print('\n##today:',today)
            contentdata={}
            href=today.get('href')#链接
            dataid=today.get('data-id')#id
            content=today.find("div",{"class":"comic-content"})
            title=content.find("strong",{"class":"comic-title"}).text#书名
            author=content.find("small",{"class":"comic-artist"}).text#作者
            charpter=content.find("small",{"class":"comic-latest"}).text#更新到多少

            # print('\n##title:',title)
            # print('##dataid:',dataid)
            # print('##author:',author)
            # print('##charpter:',charpter)
            # print('##href:',href)

            contentdata["title"]=title
            contentdata["dataid"]=dataid
            contentdata["author"]=author
            contentdata["charpter"]=charpter
            contentdata["href"]=href
            data.append(contentdata)

        return data

    #追更入口
    def get_home_zgdata(self,timelist):
        # print('\n##追更链接:',timelist)
        zgContent=timelist.find("a",{"class":"time-list-link"}).get('href')#追更链接
        zgText=timelist.find("img").get('alt')#追更链接
        zgImg=timelist.find("img").get('src')#追更图片

        # print('\n##追更链接:',zgContent)
        # print('\n##追更文字:',zgText)
        # print('\n##追更图片:',zgImg)

        moredata={}
        moredata["zgContent"]=zgContent
        moredata["zgText"]=zgText
        moredata["zgImg"]=zgImg
        return moredata

    #日漫推荐
    def get_home_japancomic(self,japancomic):
        # print('\n##日漫推荐:',japancomic)
        data=[]
        moredata={}
        moreTitle=japancomic.find("strong",{"class":"title-content"}).text#日漫更多标题
        moreDes=japancomic.find("small",{"class":"desc"}).text#日漫描述
        moreLink=japancomic.find("a",{"class":"link-more"}).get('href')#日漫更多链接

        # print('\n##日漫推荐Title:',moreTitle)
        # print('##more:',moreLink)
        # print('##moreDes:',moreDes)

        moredata["moreTitle"]=moreTitle
        moredata["moreLink"]=moreLink
        moredata["moreDes"]=moreDes
        data.append(moredata)

        moreContent=japancomic.find_all("a",{"class":"comic-link"})#日漫内容
        for japan in moreContent:
            # print('\n##japan:',japan)
            contentdata={}
            href=japan.get('href')#链接
            dataid=japan.get('data-id')#id
            content=japan.find("div",{"class":"comic-content"})
            title=content.find("strong",{"class":"comic-title"}).text#书名
            tag=content.find("small",{"class":"comic-tag"}).text#作者
            covercontent=japan.find("div",{"class":"comic-cover"})
            img=covercontent.find("img",{"class":"cover-image"}).get('src')

            # print('\n##title:',title)
            # print('##dataid:',dataid)
            # print('##tag:',tag)
            # print('##img:',img)
            # print('##href:',href)

            contentdata["title"]=title
            contentdata["dataid"]=dataid
            contentdata["tag"]=tag
            contentdata["img"]=img
            contentdata["href"]=href
            data.append(contentdata)
        return data

    #新作推荐
    def get_home_newcomic(self,newcomic):
        # print('##新作推荐:',newcomic)
        data=[]
        moredata={}
        moreTitle=newcomic.find("strong",{"class":"title-content"}).text#新作推荐标题
        moreLink=newcomic.find("a",{"class":"link-more"}).get('href')#新作推荐更多链接
        moreDes=newcomic.find("small",{"class":"desc"}).text#新作推荐描述

        # print('\n##新作推荐moreTitle:',moreTitle)
        # print('##moreLink:',moreLink)
        # print('##moreDes:',moreDes)

        moredata["moreTitle"]=moreTitle
        moredata["moreLink"]=moreLink
        moredata["moreDes"]=moreDes
        data.append(moredata)

        newcomics=newcomic.find_all("a",{"class":"comic-link"})#新作推荐更新内容
        for news in newcomics:
            # print('\n##japan:',japan)
            contentdata={}
            href=news.get('href')#链接
            dataid=news.get('data-id')#id
            content=news.find("div",{"class":"comic-content"})
            title=content.find("strong",{"class":"comic-title"}).text#书名
            tag=content.find("small",{"class":"comic-tag"}).text#作者
            covercontent=news.find("div",{"class":"comic-cover"})
            img=covercontent.find("img",{"class":"cover-image"}).get('src')

            # print('\n##title:',title)
            # print('##dataid:',dataid)
            # print('##tag:',tag)
            # print('##img:',img)
            # print('##href:',href)

            contentdata["title"]=title
            contentdata["dataid"]=dataid
            contentdata["tag"]=tag
            contentdata["img"]=img
            contentdata["href"]=href
            data.append(contentdata)
        return data

    #动画专区
    def get_home_animation(self,animation):
        # print('##新作推荐:',animation)
        data=[]
        moredata={}
        moreTitle=animation.find("strong",{"class":"title-content"}).text#新作推荐标题
        moreLink=animation.find("a",{"class":"link-more"}).get('href')#新作推荐更多链接
        moreDes=animation.find("small",{"class":"desc"}).text#新作推荐描述

        # print('\n##动画专区moreTitle:',moreTitle)
        # print('##moreLink:',moreLink)
        # print('##moreDes:',moreDes)

        moredata["moreTitle"]=moreTitle
        moredata["moreLink"]=moreLink
        moredata["moreDes"]=moreDes
        data.append(moredata)


        animations=animation.find_all("a",{"class":"animation-link"})#新作推荐更新内容
        for ams in animations:
            # print('\n##japan:',japan)
            contentdata={}
            href=ams.get('href')#链接
            dataid=ams.get('data-id')#id
            content=ams.find("strong",{"class":"animation-title"})
            title=content.find("span",{"class":"text"}).text#动画名
            covercontent=ams.find("div",{"class":"animation-cover"})
            img=covercontent.find("img",{"class":"cover-image"}).get('src')
            num=ams.find("small",{"class":"animation-length"}).text#集数

            # print('\n##title:',title)
            # print('##dataid:',dataid)
            # print('##num:',num)
            # print('##img:',img)
            # print('##href:',href)

            contentdata["title"]=title
            contentdata["dataid"]=dataid
            contentdata["num"]=num
            contentdata["img"]=img
            contentdata["href"]=href
            data.append(contentdata)
        return data
