__author__ = 'AS'
from common import DB_connect


def save_user(connect, username, about, name, email, optional):
    isAnonim = 0
    if "isAnonymous" in optional:
        isAnonim = optional["isAnonymous"]
        if isAnonim:
            name = username = about = ''
    str = DB_connect.update_query(connect,
                'INSERT INTO User (email, about, name, username, isAnonymous) VALUES (%s, %s, %s, %s, %s)', 
                (email, about, name, username, isAnonim, ))
    user = DB_connect.select_query(connect, 'Select  email, about, id, isAnonymous, name, username FROM User WHERE email = %s', (email, ) )
    return user_description(user)


def show_user(connect, email):
    user = DB_connect.select_query(connect, 'Select  email, about, id, isAnonymous, name, username FROM User WHERE email = %s', (email, ) )
    user = user_description(user)
    print("1")
    if user is None:
       raise Exception("User with email " + email +" doesn't exist ")
    user["followers"] = followers(connect, email, "user")
    user["following"] = followers(connect, email, "follow")
    user["subscriptions"] = subscriptions(connect, email)
    return user


def follow_user(connect, follower, followee):    
    user1 = DB_connect.select_query(connect, 'SELECT email FROM User WHERE email = %s', (follower, ))
    user2 = DB_connect.select_query(connect, 'SELECT email FROM User WHERE email = %s', (follower, ))
    print(user1)
    if user1 and user2:                
        str = DB_connect.update_query(connect, 
                'INSERT INTO Follow (user, follow) VALUES (%s, %s)', (follower, followee, ) )
    else:
        raise Exception("Error. Such users don't exist");
    user = show_user(connect, follower)
    return user
     

def unfollow_user(connect, follower, followee):    
    str = DB_connect.update_query(connect, 
        'DELETE FROM Follow  WHERE user =  %s AND follow = %s', (follower, followee, ) )
    if str == "Exist":
        raise Exception("Such row in db does not exist");
    user = show_user(connect, follower)
    return user


def user_description(user):
    user = user[0]
    response = {
        'email'      : user[0] ,
        'about'      : user[1],
        'id'         : user[2],
        'isAnonymous': bool(user[3]),
        'name'       : user[4],        
        'username'   : user[5]
    }
    if response['isAnonymous'] == True:
        response['about'] = response['name'] = response['username'] = None
    print(response)
    return response


def followers(connect, email, type):
    where = "user"
    if type == "user":
        where = "follow"    
    f_list = DB_connect.select_query(connect,
        "SELECT " + type + " FROM Follow WHERE " + where + " = %s ", (email, ))
    return convert_to_list(f_list)


def followers_list(connect, email, type, params):
    where = "user"
    if type == "user":
        where = "follow"

    query = "SELECT " + type + " FROM Follow JOIN User ON User.email = Follow." + type + \
            " WHERE " + where + " = %s "

    if "since_id" in params:
        query += " AND User.id >= " + str(params["since_id"])
    if "order" in params:
        query += " ORDER BY User.name " + params["order"]
    else:
        query += " ORDER BY User.name DESC "
    if "limit" in params:
        query += " LIMIT " + str(params["limit"])

    followers_ids_tuple = DB_connect.select_query(connect=connect,query=query, params=(email, ))

    f_list = []
    for id in followers_ids_tuple:
        id = id[0]
        f_list.append(show_user(connect=connect,email=id))
        
    return f_list


def subscriptions(connect, email):
    s_list = DB_connect.select_query(connect,
        "Select thread_id FROM Subscription WHERE user = %s and isDeleted = 0 ", (email, ))
    return convert_to_list(s_list)


def update_user(connect,email, about, name):
    DB_connect.update_query(connect,'UPDATE User SET email = %s, about = %s, name = %s WHERE email = %s',
                           (email, about, name, email, ))
    return show_user(connect,email)


def convert_to_list(tuple):
    list = []
    for el in tuple:
        list.append(el[0])
    return list