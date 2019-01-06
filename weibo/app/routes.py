# 作者：赖伟文
# 邮箱：lwwens@gmail.com ; lai_wei_wen@qq.com ;

import os
import re
from os import path
from flask import render_template
from app import app

cur_dir = path.dirname(__file__)
wc_path = 'static' + os.sep + 'image'


def getWCname():
    res = []
    for root_dir, alldirs, allfiles in os.walk(path.join(cur_dir, wc_path)):
        for afile in allfiles:
            match = re.search(r'\d{4}-\d{2}-\d{2}', afile)
            res.append(match.group(0))
    return res


@app.route('/')
@app.route('/index')
def index():
    im_names = getWCname()
    im_names.sort()
    return render_template('index.html', im_names=im_names)
