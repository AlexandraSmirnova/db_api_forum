from flask import Blueprint, request
from common.DB_connect import *
from common.helpers import check_data, intersection, get_json 
from User import u_queries as query
from Post import p_queries as posts

import json
import MySQLdb

user = Blueprint('user', __name__)
BASE_URL = '/user'


@user.route(BASE_URL + '/create/', methods = ['POST'])
def create():
    con = connect()     
    content = request.json
    required_data = ["username", "about", "name", "email"]
    optional = intersection(request = content, values=["isAnonymous"])
    try:
        check_data(data=content, required=required_data)
        user = query.save_user(connect = con , username = content["username"], about = content["about"],name =  content["name"], email =content["email"], optional = optional)
    except Exception as e:        
        con.close()
        if e.message == "Exist":            
            return json.dumps({"code": 5, "response": (e.message)}) 
        if e.message == "KeyError":            
            return json.dumps({"code": 3, "response": (e.message)}) 
        if e.message == "ValueError":            
            return json.dumps({"code": 2, "response": (e.message)}) 
                    
        return json.dumps({"code": 1, "response": (e.message)})
    con.close()    
    return json.dumps({"code": 0, "response": user})


@user.route(BASE_URL + '/details/', methods = ['GET'])
def details():
    con = connect()
    request_data = get_json(request)
    required_data = ["user"]
    try:
        check_data(request_data, required_data)
        user = query.show_user(connect = con, email = request_data["user"])
    except Exception as e:
        con.close()
        return json.dumps({"code" : 1, "response": (e.message)})
    con.close()
    return json.dumps({"code": 0, "response": user})


@user.route(BASE_URL + '/follow/', methods = ['POST'])
def follow():
    con = connect()
    request_data = get_json(request)
    required_data = ["follower", "followee"]   
    try:
        check_data(request_data, required_data)
        user = query.follow_user(con, request_data["follower"], request_data["followee"])
    except Exception as e:
        con.close()
        if e.message == "Exist":
            return json.dumps({"code": 4, "response": (e.message)})                
        return json.dumps({"code" : 1, "response": (e.message)})
    con.close()
    return json.dumps({"code": 0, "response": user })


@user.route(BASE_URL + "/listFollowers/", methods=["GET"])
def list_followers():
    con = connect()
    request_data = get_json(request)
    required_data = ["user"]
    followers_param = intersection(request=request_data, values=["limit", "order", "since_id"])
    try:
        check_data(data=request_data, required=required_data)
        follower_l = query.followers_list(connect=con, email=request_data["user"], type="user", params=followers_param)
    except Exception as e:
        con.close()
        return json.dumps({"code": 1, "response": (e.message)})
    con.close()
    return json.dumps({"code": 0, "response": follower_l})


@user.route(BASE_URL + "/listFollowing/", methods=["GET"])
def list_following():
    con = connect()
    request_data = get_json(request)
    required_data = ["user"]
    followers_param = intersection(request=request_data, values=["limit", "order", "since_id"])
    try:
        check_data(data=request_data, required=required_data)
        follower_l = query.followers_list(connect=con, email=request_data["user"], type="follow", params=followers_param)
    except Exception as e:
        con.close()
        return json.dumps({"code": 1, "response": (e.message)})
    con.close()
    return json.dumps({"code": 0, "response": follower_l})


@user.route(BASE_URL + "/listPosts/", methods=["GET"])
def user_posts():
    con = connect()
    content = get_json(request)
    required_data = ["user"]
    optional = intersection(content, ["limit", "order", "since"])    
    try:
        check_data(content, required_data)
        posts_l = posts.posts_list(con, "user", optional, content["user"], [])
    except Exception as e:
         con.close()
         return json.dumps({"code": 1, "response": (e.message)})
    con.close()
    return json.dumps({"code": 0, "response": posts_l})


@user.route(BASE_URL + '/unfollow/', methods = ['POST'])
def unfollow():
    con = connect()
    request_data = get_json(request)
    required_data = ["follower", "followee"]   
    try:
        check_data(request_data, required_data)
        user = query.unfollow_user(con, request_data["follower"], request_data["followee"])
    except Exception as e:
        con.close()        
        return json.dumps({"code" : 1, "response": (e.message)})
    con.close()
    return json.dumps({"code": 0, "response": user })


@user.route(BASE_URL + "/updateProfile/", methods=["POST"])
def update():
    con = connect()
    request_data = request.json
    required_data = ["user", "name", "about"]
    try:
        check_data(data=request_data, required=required_data)
        user = query.update_user(connect=con,email=request_data["user"], name=request_data["name"], about=request_data["about"])
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
    return json.dumps({"code": 0, "response": user})

