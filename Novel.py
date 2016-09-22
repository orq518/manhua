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

    # if request.method == 'POST':
    #     id=request.args.get('id')
    #     print('post--id:',id)
    # else:
    #     id=request.args.get('id')
    #     print('get--id:',id)

    state="0"
    msg="成功"
    datalist=homedate.getRanking(type)
    return creatJson(state,msg,datalist)


#文章的章节列表
@app.route('/getNovelCharpterList/<id>', methods=['GET', 'POST'])
def getNovelCharpterList(id):

    # if request.method == 'POST':
    #     id=request.args.get('id')
    #     print('post--id:',id)
    # else:
    #     id=request.args.get('id')
    #     print('get--id:',id)
    # http://m.ac.qq.com/chapter/index/id/518335/cid/115
    # return chapterlistdata.getChapterDetailData("518335","115")
    state="0"
    msg="成功"
    datalist=homedate.getNovelCharpterList(id)
    return creatJson(state,msg,datalist)


#文章详情
@app.route('/getNovelDetail/<id>', methods=['GET', 'POST'])
def getNovelDetail(id):

    # if request.method == 'POST':
    #     id=request.args.get('id')
    #     print('post--id:',id)
    # else:
    #     id=request.args.get('id')
    #     print('get--id:',id)
    # http://m.ac.qq.com/chapter/index/id/518335/cid/115
    # chapterlistdata=homedate.getNovelDetail()
    # return chapterlistdata.getChapterDetailData("518335","115")
    state="0"
    msg="成功"
    datalist=homedate.getNovelDetail(id)
    return creatJson(state,msg,datalist)



# #搜索
# @app.route('/search/', methods=['GET', 'POST'])
# def search():
#     homedate.search()
#
# #日轻列表 latest:最新更新  hot：热门推荐   finish完结
# @app.route('/rq/', methods=['GET', 'POST'])
# def getChapterListData():
#     homedate.getRQ("latest","1")
# #更新
# @app.route('/getUpdata/', methods=['GET', 'POST'])
# def getUpdata():
#     homedate.getUpdata()


# @app.route('/login', methods=['POST', 'GET'])
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
    data["state"]="0"
    data["msg"]="成功"
    data["data"]=datalist
    jsondata=json.encode(data,"utf8")
    print('\n##生成json数据:\n',jsondata)
    return jsondata


@app.route('/')
def hello_world():
    return "hello world"

if __name__ == '__main__':
    app.run()
