from flask import Blueprint, request
from common.DB_connect import *
from common.helpers import check_data, intersection, get_json, related_exists 
from Thread import t_queries as query
from Post import p_queries as posts
import json
import MySQLdb

thread = Blueprint('thread', __name__)
BASE_URL = '/thread'


@thread.route(BASE_URL + '/create/', methods = ['POST'])
def create():
    con = connect()     
    content = request.json
    required_data = ["forum", "title", "isClosed", "user", "date", "message", "slug"]
    optional = intersection(request = content, values=["isDeleted"])
    try:
        check_data(data=content, required=required_data)        
        thread = query.save_thread(con , content["forum"], content["title"], 
        content["isClosed"], content["user"], content["date"], content["message"], content["slug"], optional)
    except Exception as e:
        con.close()
        if e.message == "Exist":            
            return json.dumps({"code": 5, "response": (e.message)})        
        return json.dumps({"code": 1, "response": (e.message)})
    con.close()    
    return json.dumps({"code": 0, "response": thread})


@thread.route(BASE_URL + "/details/", methods=["GET"])
def details():
    con = connect()
    content = get_json(request)
    required_data = ["thread"]
    related = related_exists(content)
    if 'thread' in related:
        con.close()
        return json.dumps({"code": 3, "response": "error"})
    try:
        check_data(content, required_data)
        thread = query.show_thread(con, content["thread"], related)
    except Exception as e:
        con.close()
        return json.dumps({"code": 1, "response": (e.message)})
    con.close()
    return json.dumps({"code": 0, "response": thread})


@thread.route(BASE_URL + "/list/", methods=["GET"])
def thread_list():
    con = connect()
    content = get_json(request)
    try:
        identifier = content["forum"]
        entity = "forum"
    except KeyError:
        try:
            identifier = content["user"]
            entity = "user"
        except Exception as e:
            con.close()
            return json.dumps({"code": 1, "response": (e.message)})
    optional = intersection(content, ["limit", "order", "since"])    
    try:
        threads_l = query.threads_list(con, entity, optional, identifier, [])
    except Exception as e:
        con.close()
        return json.dumps({"code": 1, "response": (e.message)})
    con.close()
    return json.dumps({"code": 0, "response": threads_l})


@thread.route(BASE_URL + "/listPosts/", methods=["GET"])
def thread_posts():
    con = connect()
    content = get_json(request)
    required_data = ["thread"]
    optional = intersection(content, ["limit", "order", "since"])    
    try:
        check_data(content, required_data)
        posts_l = posts.posts_list(con, "thread", optional, content["thread"], [])
    except Exception as e:
         con.close()
         return json.dumps({"code": 1, "response": (e.message)})
    con.close()
    return json.dumps({"code": 0, "response": posts_l})


@thread.route(BASE_URL + "/open/", methods=["POST"])
def open():
    con = connect()
    request_data = request.json
    required_data = ["thread"]
    try:
        check_data(data=request_data, required=required_data)
        thread = query.open_close_thread(con, request_data["thread"], 0)
    except Exception as e:
        con.close()
        return json.dumps({"code": 1, "response": (e.message)})
    con.close()
    return json.dumps({"code": 0, "response": thread})


@thread.route(BASE_URL + "/close/", methods=["POST"])
def close():
    con = connect()
    request_data = request.json
    required_data = ["thread"]
    try:
        check_data(data=request_data, required=required_data)
        thread = query.open_close_thread(con, request_data["thread"], 1)
    except Exception as e:
        con.close()
        return json.dumps({"code": 1, "response": (e.message)})
    con.close()
    return json.dumps({"code": 0, "response": thread})


@thread.route(BASE_URL + '/remove/', methods = ['POST'])
def remove():
    con = connect()     
    content = request.json
    required_data = ["thread"]
    try:
        check_data(content, required_data)
        print("xa")
        thread = query.remove_restore(con , content["thread"], 1) 
        print("xa2")      
    except Exception as e:
        con.close()
        if e.message == "Exist":
            return json.dumps({"code": 4, "response": (e.message)}) 
        if e.message == "KeyError":
            return json.dumps({"code": 3, "response": (e.message)}) 
        if e.message == "ValueError":
            return json.dumps({"code": 2, "response": (e.message)}) 
        return json.dumps({"code": 1, "response": (e.message)})
    con.close()    
    return json.dumps({"code": 0, "response": thread})


@thread.route(BASE_URL + '/restore/', methods = ['POST'])
def restore():
    con = connect()     
    content = request.json
    required_data = ["thread"]
    try:
        check_data(content, required_data)    
        thread = query.remove_restore(con , content["thread"], 0)       
    except Exception as e:
        con.close()
        if e.message == "Exist":
            return json.dumps({"code": 4, "response": (e.message)}) 
        if e.message == "KeyError":
            return json.dumps({"code": 3, "response": (e.message)}) 
        if e.message == "ValueError":
            return json.dumps({"code": 2, "response": (e.message)}) 
        return json.dumps({"code": 1, "response": (e.message)})
    con.close()    
    return json.dumps({"code": 0, "response": thread})


@thread.route(BASE_URL + '/subscribe/', methods = ['POST'])
def subscribe():
    con = connect()     
    content = request.json
    required_data = ["thread", "user"]
    try:
        check_data(content, required_data)    
        thread = query.subscribe_user(con , content["thread"], content["user"])       
    except Exception as e:
        con.close()
        if e.message == "Exist":
            return json.dumps({"code": 4, "response": (e.message)}) 
        if e.message == "KeyError":
            return json.dumps({"code": 3, "response": (e.message)}) 
        if e.message == "ValueError":
            return json.dumps({"code": 2, "response": (e.message)}) 
        return json.dumps({"code": 1, "response": (e.message)})
    con.close()    
    return json.dumps({"code": 0, "response": thread})


@thread.route(BASE_URL + '/unsubscribe/', methods = ['POST'])
def unsubscribe():
    con = connect()     
    content = request.json
    required_data = ["thread", "user"]
    try:
        check_data(content, required_data)    
        thread = query.unsubscribe_user(con , content["thread"], content["user"])       
    except Exception as e:
        con.close()
        if e.message == "Exist":
            return json.dumps({"code": 4, "response": (e.message)}) 
        if e.message == "KeyError":
            return json.dumps({"code": 3, "response": (e.message)}) 
        if e.message == "ValueError":
            return json.dumps({"code": 2, "response": (e.message)}) 
        return json.dumps({"code": 1, "response": (e.message)})
    con.close()    
    return json.dumps({"code": 0, "response": thread})


@thread.route(BASE_URL + "/update/", methods=["POST"])
def update():
    con = connect()
    request_data = request.json
    required_data = ["message", "slug", "thread"]
    try:
        check_data(data=request_data, required=required_data)
        thread = query.update_thread(con, request_data["message"], request_data["slug"], request_data["thread"])
    except Exception as e:
        con.close()
        return json.dumps({"code": 1, "response": (e.message)})
    con.close()
    return json.dumps({"code": 0, "response": thread})



@thread.route(BASE_URL + '/vote/', methods = ['POST'])
def vote():
    con = connect()     
    content = request.json
    required_data = ["thread", "vote"]
    try:
        check_data(content, required_data)
        thread = query.vote_for_thread(con , content["thread"], content["vote"])      
    except Exception as e:
        con.close()
        if e.message == "Exist":
            return json.dumps({"code": 4, "response": (e.message)}) 
        if e.message == "KeyError":
            return json.dumps({"code": 3, "response": (e.message)}) 
        if e.message == "ValueError":
            return json.dumps({"code": 2, "response": (e.message)}) 
        return json.dumps({"code": 1, "response": (e.message)})
    con.close()    
    return json.dumps({"code": 0, "response": thread})