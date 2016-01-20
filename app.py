__author__ = 'AS'

from flask import Flask, Blueprint, request
from common.clear import *
from common.status import *
import json
from werkzeug.contrib.fixers import ProxyFix
app = Flask(__name__)
#app.config.from_object('myconf')

from Thread.threads import *
from Forum.forums import *
from Post.posts  import  *
from User.users import  *

 
BASE_URL='/db/api';
app.register_blueprint(forum, url_prefix = BASE_URL )
app.register_blueprint(post,  url_prefix = BASE_URL )
app.register_blueprint(user,  url_prefix = BASE_URL )
app.register_blueprint(thread,  url_prefix = BASE_URL )


@app.route('/db/api/clear/', methods=['POST'])
def clear_db():
    clear()
    return json.dumps({"code" : 0, "response" : "OK" })


@app.route('/db/api/status/', methods=['GET'])
def status_db():
    answer = status()
    return json.dumps({"code" : 0, "response" : answer })


if __name__ == "__main__":
	#app.run(host = '10.20.0.46', port = 8080)
    app.run()
