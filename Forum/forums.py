from flask import Blueprint, request
from common.DB_connect import *
from common.helpers import check_data, get_json, intersection, related_exists
from Forum import f_queries as query 
from Post import p_queries as posts
from Thread import t_queries as threads

import json
import MySQLdb

forum = Blueprint('forum', __name__)
BASE_URL = '/forum'


@forum.route(BASE_URL + '/create/', methods = ['POST'])
def create():    
    con = connect()
    content = request.json
    required_data = ["name", "short_name", "user"]
    file = open('forum_create.txt', 'a')   
    file.write("request: " + json.dumps(content) + "\n")    
    try:
        check_data(content, required_data)
        forum = query.save_forum(con, content["name"], content["short_name"], content["user"])
    except Exception as e:
        con.close()
        if e.message == "Exist":
            response = {"code": 4, "response": (e.message)} 
        if e.message == "KeyError":
            response = {"code": 3, "response": (e.message)}
        if e.message == "ValueError":
            response = {"code": 2, "response": (e.message)}
        file.write("response: " +response + "\n\n" )
        file.close()  
        return json.dumps(response)  
    response = json.dumps({"code": 0, "response": forum})
    file.write("response: " +response + "\n\n" )
    file.close()        
    con.close()
    return json.dumps({"code": 0, "response": forum})


@forum.route(BASE_URL + '/details/', methods = ['GET'])
def details():
    con = connect()
    content = get_json(request)
    required_data = ["forum"]
    related = related_exists(content)
    if 'forum' in related:
        con.close()
        return json.dumps({"code": 3, "response": "error"})
    try:
        check_data(content, required_data)
        forum = query.show_forum(con, content["forum"], related)
    except Exception as e:
        con.close()
        return json.dumps({"code": 1, "response": (e.message)})
    con.close()
    return json.dumps({"code": 0, "response": forum})


@forum.route(BASE_URL + "/listPosts/", methods=["GET"])
def list_posts():
    con = connect()
    content = get_json(request)
    required_data = ["forum"]
    related = related_exists(content)
    optional = intersection(content, ["limit", "order", "since"])    
    try:
        check_data(content, required_data)
        posts_l = posts.posts_list(con, "forum", optional, content["forum"], related)
    except Exception as e:
         con.close()
         return json.dumps({"code": 1, "response": (e.message)})
    con.close()
    return json.dumps({"code": 0, "response": posts_l})


@forum.route(BASE_URL + "/listThreads/", methods=["GET"])
def list_threads():
    con = connect()
    content = get_json(request)
    required_data = ["forum"]
    related = related_exists(content)
    optional = intersection(content, ["limit", "order", "since"])
    try:
        check_data(content, required_data)
        threads_l = threads.threads_list(con, "forum", optional, content["forum"], related)
    except Exception as e:
        con.close()
        return json.dumps({"code": 1, "response": (e.message)})
    con.close()
    return json.dumps({"code": 0, "response": threads_l})


@forum.route(BASE_URL + "/listUsers/", methods=["GET"])
def list_users():
    con = connect()
    content = get_json(request)
    required_data = ["forum"]    
    optional = intersection(content, ["limit", "order", "since"])    
    try:
        check_data(content, required_data)
        users_l = query.users_list(con, content["forum"], optional)
    except Exception as e:
         con.close()
         return json.dumps({"code": 1, "response": (e.message)})
    con.close()
    return json.dumps({"code": 0, "response": users_l})