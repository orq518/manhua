# coding:utf-8
# author： ou
from flask import Flask, request
from novel import novelspider
import demjson as json

app = Flask(__name__)


@app.before_request
def before_request():
    global homedate
    homedate=novelspider.NovelSpider()

#首页数据
@app.route('/home/')
def gethomedata():
    state="0"
    msg="成功"
    datalist=homedate.getNovelHome()
    return creatJson(state,msg,datalist)

#排行中的这些栏目类型--original:原创 sale 热销 jp：日轻 new：新书 ticket：月票 bm：收藏
@app.route('/rank/<type>', methods=['GET', 'POST'])
def getRanking(type):

    state="0"
    msg="成功"
    datalist=homedate.getRanking(type)
    return creatJson(state,msg,datalist)


#文章的章节列表
@app.route('/getNovelCharpterList/', methods=['GET', 'POST'])
def getNovelCharpterList():
    id=""
    if request.method == 'POST':
        id=request.values.get('id')
        print('post--id:',id)
    state="0"
    msg="成功"
    datalist=homedate.getNovelCharpterList(id)
    return creatJson(state,msg,datalist)


#文章详情
@app.route('/getNovelDetail/', methods=['GET', 'POST'])
def getNovelDetail():
    id=""
    if request.method == 'POST':
        id=request.values.get('id')
        print('post--id:',id)
    state="0"
    msg="成功"
    datalist=homedate.getNovelDetail(id)
    return creatJson(state,msg,datalist)



#搜索
@app.route('/search/', methods=['GET', 'POST'])
def search():
    key=""
    if request.method == 'POST':
        key=request.values.get('key')
        print('post--key:',key)


    state="0"
    msg="成功"
    datalist=homedate.search(key)
    return creatJson(state,msg,datalist)

#日轻列表 latest:最新更新  hot：热门推荐   finish完结
@app.route('/rq/<type>', methods=['GET', 'POST'])
def getChapterListData(type):

    index=""
    if request.method == 'POST':
        index=request.values.get('index')
        print('post--index:',index)
    state="0"
    msg="成功"
    datalist=homedate.getRQ(type,index)
    return creatJson(state,msg,datalist)


#更新
@app.route('/getUpdate/', methods=['GET', 'POST'])
def getUpdate():
    index=0
    if request.method == 'POST':
        index=request.values.get('index')
        print('post--index:',index)
    state="0"
    msg="成功"
    datalist=homedate.getUpdate(index)
    return creatJson(state,msg,datalist)
    # http://rs.sfacg.com/web/novel/images/NovelCover/Big/2016/09/3340225b-8b61-474c-8d09-341a9dacf055.jpg

#美女
@app.route('/getGirlsData/<page>', methods=['GET', 'POST'])
def getGirlsData(page):
    state="0"
    msg="成功"
    datalist=homedate.getGirlsData(page)
    return creatJson(state,msg,datalist)


@app.route('/login', methods=['POST', 'GET'])
# def login():
#     error = None
#     if request.method == 'POST':
#         if valid_login(request.form['username'],
#                        request.form['password']):
#             return log_the_user_in(request.form['username'])
#         else:
#             error = 'Invalid username/password'
#     # the code below is executed if the request method
#     # was GET or the credentials were invalid
#     return render_template('login.html', error=error)

def creatJson(state,msg,datalist):
    data={}
    data["state"]=state
    data["msg"]=msg
    data["data"]=datalist
    jsondata=json.encode(data,"utf8")
    # print('\n##生成json数据:\n',jsondata)
    return jsondata


@app.route('/')
def hello_world():
    return "hello world"

if __name__ == '__main__':
    app.run()
