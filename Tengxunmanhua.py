# coding:utf-8
# author： ou
from flask import Flask
from txspider import homepage
app = Flask(__name__)


@app.route('/')
def hello_world():
    return "hello world"

@app.route('/homedata/')
def gethomedata():
    homedate=homepage.HomePage()
    return homedate.get_home_data()

if __name__ == '__main__':
    app.run()
