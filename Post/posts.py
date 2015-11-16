from flask import Blueprint, request
from common.DB_connect import *
from common.helpers import check_data, intersection, get_json, related_exists 
from Post import p_queries as query

import json
import MySQLdb

post = Blueprint('post', __name__)
BASE_URL = '/post'


@post.route(BASE_URL + '/create/', methods = ['POST'])
def create():
    con = connect()     
    content = request.json
    required_data = ["date", "thread", "message", "user", "forum"]
    optional = intersection(content, ["parent", "isApproved", "isHighlighted", "isEdited", "isSpam", "isDeleted"])
    try:
        check_data(content, required_data)
        post = query.save_post(con , content["date"], content["thread"], content["message"], content["user"], content["forum"], optional)
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
    return json.dumps({"code": 0, "response": post})


@post.route(BASE_URL + "/details/", methods=["GET"])
def details():
    con = connect()
    content = get_json(request)
    required_data = ["post"]
    related = related_exists(content)
    if 'post' in related:
        con.close()
        return json.dumps({"code": 3, "response": "error"})
    try:
        check_data(content, required_data)
        post = query.show_post(con, content["post"], related)
    except Exception as e:
        con.close()
        return json.dumps({"code": 1, "response": (e.message)})
    con.close()
    return json.dumps({"code": 0, "response": post})


@post.route(BASE_URL + "/list/", methods=["GET"])
def post_list():
    con = connect()
    content = get_json(request)
    try:
        identifier = content["forum"]
        entity = "forum"
    except KeyError:
        try:
            identifier = content["thread"]
            entity = "thread"
        except Exception as e:
            con.close()
            return json.dumps({"code": 1, "response": (e.message)})
    optional = intersection(content, ["limit", "order", "since"])    
    try:
        posts_l = query.posts_list(con, entity, optional, identifier, [])
    except Exception as e:
         con.close()
         return json.dumps({"code": 1, "response": (e.message)})
    con.close()
    return json.dumps({"code": 0, "response": posts_l})


@post.route(BASE_URL + '/remove/', methods = ['POST'])
def remove():
    con = connect()     
    content = request.json
    required_data = ["post"]
    try:
        check_data(content, required_data)
        post = query.delete_post(con , content["post"])       
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
    return json.dumps({"code": 0, "response": post})


@post.route(BASE_URL + '/restore/', methods = ['POST'])
def restore():
    con = connect()     
    content = request.json
    required_data = ["post"]
    try:
        check_data(content, required_data)
        post = query.restore_post(con , content["post"])       
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
    return json.dumps({"code": 0, "response": post})


@post.route(BASE_URL + "/update/", methods=["POST"])
def update():
    con = connect()
    request_data = request.json
    required_data = ["post", "message"]
    try:
        check_data(data=request_data, required=required_data)
        post = query.update_post(con, request_data["post"], request_data["message"])
    except Exception as e:
        con.close()
        return json.dumps({"code": 1, "response": (e.message)})
    con.close()
    return json.dumps({"code": 0, "response": post})


@post.route(BASE_URL + '/vote/', methods = ['POST'])
def vote():
    con = connect()     
    content = request.json
    required_data = ["post", "vote"]
    try:
        check_data(content, required_data)
        post = query.vote_for_post(con , content["post"], content["vote"])      
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
    return json.dumps({"code": 0, "response": post})
