import os
import sys
from flask import Flask, render_template

app = Flask(__name__)
@app.route('/') 
def index():    # 定义根目录处理器
    return render_template('index.html')

@app.route('/detail')
def detail():
    return render_template('detail.html')

if __name__ == '__main__':
    app.run() # 启动服务