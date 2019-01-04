# 作者：赖伟文
# 邮箱：lwwens@gmail.com ; lai_wei_wen@qq.com ;

from flask import Flask

app = Flask(__name__)

from app import routes
