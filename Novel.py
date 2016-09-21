# coding:utf-8
# author： ou
from flask import Flask, request
from novel import novelspider


app = Flask(__name__)


@app.before_request
def before_request():
    global homedate
    homedate=novelspider.NovelSpider()

#首页数据
@app.route('/home/')
def gethomedata():
    return homedate.getNovelHome()



#日轻列表 latest:最新更新  hot：热门推荐   finish完结
@app.route('/rq/', methods=['GET', 'POST'])
def getChapterListData():

    # if request.method == 'POST':
    #     id=request.args.get('id')
    #     print('post--id:',id)
    # else:
    #     id=request.args.get('id')
    #     print('get--id:',id)
    # latest:最新更新  hot：热门推荐   finish完结
    homedate.getRQ()



#排行中的这些栏目类型--original:原创 sale 热销 jp：日轻 new：新书 ticket：月票 bm：收藏
@app.route('/rank/', methods=['GET', 'POST'])
def getRanking():

    # if request.method == 'POST':
    #     id=request.args.get('id')
    #     print('post--id:',id)
    # else:
    #     id=request.args.get('id')
    #     print('get--id:',id)
    homedate.getRanking()

#文章的章节列表
@app.route('/getNovelCharpterList/', methods=['GET', 'POST'])
def getNovelCharpterList():

    # if request.method == 'POST':
    #     id=request.args.get('id')
    #     print('post--id:',id)
    # else:
    #     id=request.args.get('id')
    #     print('get--id:',id)
    # http://m.ac.qq.com/chapter/index/id/518335/cid/115
    chapterlistdata=homedate.getNovelCharpterList()
    # return chapterlistdata.getChapterDetailData("518335","115")


#文章详情
@app.route('/getNovelDetail/', methods=['GET', 'POST'])
def getNovelDetail():

    # if request.method == 'POST':
    #     id=request.args.get('id')
    #     print('post--id:',id)
    # else:
    #     id=request.args.get('id')
    #     print('get--id:',id)
    # http://m.ac.qq.com/chapter/index/id/518335/cid/115
    chapterlistdata=homedate.getNovelDetail()
    # return chapterlistdata.getChapterDetailData("518335","115")



    #文章详情
@app.route('/search/', methods=['GET', 'POST'])
def search():

    # if request.method == 'POST':
    #     id=request.args.get('id')
    #     print('post--id:',id)
    # else:
    #     id=request.args.get('id')
    #     print('get--id:',id)
    # http://m.ac.qq.com/chapter/index/id/518335/cid/115
    chapterlistdata=homedate.search()
    # return chapterlistdata.getChapterDetailData("518335","115")



#文章详情
@app.route('/getUpdata/', methods=['GET', 'POST'])
def getUpdata():

    # if request.method == 'POST':
    #     id=request.args.get('id')
    #     print('post--id:',id)
    # else:
    #     id=request.args.get('id')
    #     print('get--id:',id)
    # http://m.ac.qq.com/chapter/index/id/518335/cid/115
    chapterlistdata=homedate.getUpdata()
    # return chapterlistdata.getChapterDetailData("518335","115")


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

@app.route('/')
def hello_world():
    return "hello world"

if __name__ == '__main__':
    app.run()
