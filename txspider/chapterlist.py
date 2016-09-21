# coding:utf-8
# author： ou
import urllib.request
from bs4 import BeautifulSoup
from txspider import  txmhrul
import demjson as json
import requests
import re
#首页数据
class ChapterList(object):
    def __init__(self):
        self.urlchapterList =txmhrul.urlchapterList
        self.urlchapterDetail =txmhrul.urlchapterDetail
        self.user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'
        self.headers = { 'User-Agent' : self.user_agent}
        self.requestSession = requests.session()
        self.requestSession.headers.update({'User-Agent': self.user_agent})

    #章节列表数据
    def getChapterListData(self,id):
        # print('id:',id)
        # print('self.urlchapterList:',self.urlchapterList)
        data=[]
        url=self.urlchapterList.format(id)
        if url.startswith(txmhrul.urlhome)==False:
            url=txmhrul.urlhome+url;
        # print('章节列表url:',url)
        req = urllib.request.Request(url, headers = self.headers)
        response = urllib.request.urlopen(req)
        the_page = response.read()
        # print('the_page:',the_page)
        soup = BeautifulSoup(the_page, 'html.parser')

        chapterList=[]
        chapterListData=soup.find_all("li",{"class":"chapter-item"})#章节列表
        for chapter in chapterListData:
            chapterdata=chapter.find("a",{"class":"chapter-link "})#章节列表
            if chapterdata==None:
                chapterdata=chapter.find("a",{"class":"chapter-link"})#章节列表
            datacid=chapterdata.get('data-cid')#cid
            dataseq=chapterdata.get('data-seq')#data-seq
            href=chapterdata.get('href')#href
            text=chapterdata.text#集数文字

            # print('\n##章节:',datacid)
            # print('##dataseq:',dataseq)
            # print('##href:',href)
            # print('##text:',text)

            # <a class="chapter-link "
            #     data-cid="289" data-seq="270"
            #     href="/chapter/index/id/518333/cid/289">270</a>
            contentdata={}
            contentdata["datacid"]=datacid
            contentdata["dataseq"]=dataseq
            contentdata["href"]=href
            contentdata["text"]=text
            chapterList.append(contentdata)


        data={}
        data["state"]="0"
        data["msg"]="成功"
        data["data"]=chapterList
        jsondata=json.encode(data,"utf8")
        print('\n##生成章节列表json数据:\n',jsondata)

        return jsondata



    #集数详情数据http://m.ac.qq.com/chapter/index/id/518335/cid/115
    def getChapterDetailData(self,id,cid):
        # print('id:',id)
        # print('self.urlchapterList:',self.urlchapterList)
        data=[]
        url=self.urlchapterDetail.format(id,cid)
        if url.startswith(txmhrul.urlhome)==False:
            url=txmhrul.urlhome+url;
        print('章节详情url:',url)
        req = urllib.request.Request(url, headers = self.headers)
        response = urllib.request.urlopen(req)
        the_page = response.read()
        # print('the_page:',the_page)
        soup = BeautifulSoup(the_page, 'html.parser')
        # print('soup:',soup)
        chapterList=[]
        chapterData=soup.find_all("li",{"class":"comic-pic-item pic-loaded"})#章节列表
        for chapter in chapterData:
            chapterdata=chapter.find("img",{"class":"comic-pic"})#章节列表

            datasrc=chapterdata.get('data-src')#cid
            src=chapterdata.get('src')#data-seq

            print('\n##章节详情:',datasrc)
            print('##src:',src)

            contentdata={}
            contentdata["datasrc"]=datasrc
            contentdata["src"]=src
            chapterList.append(contentdata)


        data={}
        data["state"]="0"
        data["msg"]="成功"
        data["data"]=chapterList
        jsondata=json.encode(data,"utf8")
        print('\n##生成章节详情json数据:\n',jsondata)


        # self.getImgList(id,cid)

        return jsondata

    def getImgList(self,id,cid):
        self.requestSession.headers.update({'Referer': 'http://ac.qq.com/Comic/comicInfo/id/{}'.format(id)})
        cid_page = self.requestSession.get('http://ac.qq.com/ComicView/index/id/{0}/cid/{1}'.format(id,cid),timeout=5).text

        print('\n##id:',id)
        print('##cid:',cid)
        print('##cid_page:',cid_page)


        base64data = re.findall(r"DATA\s*=\s*'(.+?)'", cid_page)[0][1:]
        img_detail_json = json.loads(self.__decode_base64_data(base64data))

        print('\n##哈哈img_detail_json:',img_detail_json)

        imgList = []
        for img_url in img_detail_json.get('picture'):
            print('\n##img_url:',img_url)
            imgList.append(img_url['url'])
        return imgList


    def __decode_base64_data(self,base64data):
        base64DecodeChars = [- 1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 62, -1, -1, -1, 63, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, -1, -1, -1, -1, -1, -1, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, -1, -1, -1, -1, -1, -1, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, -1, -1, -1, -1, -1]
        data_length = len(base64data)
        i = 0
        out = ""
        c1 = c2 = c3 = c4 = 0
        while i < data_length:
            while True:
                c1 = base64DecodeChars[ord(base64data[i]) & 255]
                i += 1
                if not (i < data_length and c1 == -1):
                    break
            if c1 == -1:
                break
            while True:
                c2 = base64DecodeChars[ord(base64data[i]) & 255]
                i += 1
                if not (i < data_length and c2 == -1):
                    break
            if c2 == -1:
                break
            out += chr(c1 << 2 | (c2 & 48) >> 4)
            while True:
                c3 = ord(base64data[i]) & 255
                i += 1
                if c3 == 61:
                    return out
                c3 = base64DecodeChars[c3]
                if not (i < data_length and c3 == - 1):
                    break
            if c3 == -1:
                break
            out += chr((c2 & 15) << 4 | (c3 & 60) >> 2)
            while True:
                c4 = ord(base64data[i]) & 255
                i += 1
                if c4 == 61:
                    return out
                c4 = base64DecodeChars[c4]
                if not (i < data_length and c4 == - 1):
                    break
            out += chr((c3 & 3) << 6 | c4)
        return out