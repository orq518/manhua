# coding:utf-8
# author： ou
import os
from flask import Flask, request, render_template, send_from_directory, make_response, send_file
from werkzeug.utils import secure_filename
from androidtest import AndroidTest
import zipfile
import shutil
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/tmp/'

@app.before_request
def before_request():
    global android
    android=AndroidTest.AndroidTest()

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    # return 'User %s' % username
    print("@@@11",username)
    return render_template('welcome.html', title=username)

@app.route('/hello')
def hello_world():
    print("@@@22")
    return "hello"

@app.route('/home')
def home():
    print("@@@33")
    return "home"


@app.route('/teststart')
def teststart():
        #切换到android工程目录
        os.chdir("E:/new_android_projects/AndroidTestDemo-master")
        print('进入目录： ' + os.getcwd())
        #执行单元测试命令
        cmd = 'gradle cAT'
        os.system(cmd)

        print('当前目录： ' + os.getcwd())
        # path="E:/new_android_projects/AndroidTestDemo-master/app/build/reports/androidTests/connected/index.html"
        path=r"E:/new_android_projects/AndroidTestDemo-master/app/build/reports/androidTests"

        outname=r"E:/new_android_projects/AndroidTestDemo-master/app/build/reports/androidTests.zip"
        print('压缩输出： ' +outname)
        # # return render(request, "blogapp/test.html")
        zip_dir(path,outname)
        print("压缩完成")
        copy()
        print("复制完成")
        return render_template('androidreport.html',title=outname)

# #复制
# @app.route('/copy/',methods = ['GET','POST'])
def copy():
    print('复制')
    outname=r"E:/new_android_projects/AndroidTestDemo-master/app/build/reports/androidTests.zip"
    toFile=r"E:/python_workspaace/manhua.git/static/androidTests.zip"
    copyFiles(outname,toFile)
    return 'upload success'

@app.route('/', methods=['POST'])
def upload_file1():
    file = request.files['file']
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return 'upload success'

#下载
@app.route('/download/',methods = ['GET','POST'])
def upload_file():
    print('下载报告')
    return  render_template('androidTests.zip')

#压缩
def zip_dir(dirname,zipfilename):
    filelist = []
    if os.path.isfile(dirname):
        filelist.append(dirname)
    else :
        for root, dirs, files in os.walk(dirname):
            for name in files:
                filelist.append(os.path.join(root, name))

    zf = zipfile.ZipFile(zipfilename, "w", zipfile.zlib.DEFLATED)
    for tar in filelist:
        arcname = tar[len(dirname):]
        #print arcname
        zf.write(tar,arcname)
    zf.close()

#文件复制
def copyFiles(sourceDir,  targetDir):
    shutil.copyfile(sourceDir,targetDir)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
