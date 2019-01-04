# 作者：赖伟文
# 邮箱：lwwens@gmail.com ; lai_wei_wen@qq.com ;

import os
import re
import codecs
from os import path
from flask import render_template
from app import app

cur_dir = path.dirname(__file__)
wc_path = 'data' + os.sep + 'wcimage'

def getWCname():
    res = []
    for root_dir, alldirs, allfiles in os.walk(path.join(cur_dir, os.pardir, wc_path)):
        for afile in allfiles:
            match = re.search(r'\d{4}-\d{2}-\d{2}', afile)
            res.append(match.group(0))
    return res

@app.route('/')
@app.route('/index')
def index():
    wcnames = getWCname()
    return render_template('index.html', wcnames=wcnames)

@app.route('/wc/<dateno>')
def wcimage(dateno):
    import base64
    img_stream = ''
    with codecs.open(path.join(cur_dir, os.pardir, wc_path, dateno + '.jpg'), 'r', encoding='utf-8') as img_file:
        img_stream = img_file.read()
        img_stream = base64.b64encode(img_stream)

    return render_template('wcimage.html', wcnames=getWCname(), img_stream=img_stream)
