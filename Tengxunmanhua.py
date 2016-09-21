# coding:utf-8
# author： ou
from flask import Flask, request
from txspider import homepage
from txspider import chapterlist


app = Flask(__name__)



#首页数据
@app.route('/homedata/')
def gethomedata():
    homedate=homepage.HomePage()
    return homedate.get_home_data()

#章节列表
@app.route('/chapterlist/', methods=['GET', 'POST'])
def getChapterListData():

    # if request.method == 'POST':
    #     id=request.args.get('id')
    #     print('post--id:',id)
    # else:
    #     id=request.args.get('id')
    #     print('get--id:',id)
    chapterlistdata=chapterlist.ChapterList()
    return chapterlistdata.getChapterListData("518335")

#集数详情图片
@app.route('/chapterdetail/', methods=['GET', 'POST'])
def getChapterDetailData():

    # if request.method == 'POST':
    #     id=request.args.get('id')
    #     print('post--id:',id)
    # else:
    #     id=request.args.get('id')
    #     print('get--id:',id)
    # http://m.ac.qq.com/chapter/index/id/518335/cid/115
    chapterlistdata=chapterlist.ChapterList()
    return chapterlistdata.getChapterDetailData("518335","115")


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
