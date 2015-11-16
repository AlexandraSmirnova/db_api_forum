__author__ = 'AS'
from common  import DB_connect
from User import u_queries as users

def save_forum(connect, name, short_name, user):
    print('save_forum:')
    #str = DB_connect.select_query(connect, 'SELECT id FROM Forum WHERE short_name = %s', (short_name, ))
    #if len(str) > 0:
    #    raise Exception("Exist")
    DB_connect.update_query(connect, "INSERT INTO Forum (name, short_name, user) VALUES (%s, %s, %s)", (name, short_name, user, ))
    forum = DB_connect.select_query(connect, 'SELECT id, name, short_name, user FROM Forum WHERE short_name = %s', (short_name, ))

    return forum_description(forum)

def forum_description(forum):
    forum = forum[0]
    response = {        
        'name': forum[1],
        'short_name': forum[2],
        'user': forum[3],
        'id': forum[0]
    }
    print(response)
    return response

    
def show_forum(connect, short_name, related):
    forum = DB_connect.select_query(connect,
        'SELECT id, name, short_name, user FROM Forum WHERE short_name = %s LIMIT 1;', (short_name, ))
    if len(forum) == 0:
        raise ("No forum with short_name: " + short_name)
    forum = forum_description(forum)
    if "user" in related:
        forum["user"] = users.show_user(connect, forum["user"])
    return forum


def users_list(connect, short_name, optional):
    query = "SELECT id, email, name, username, isAnonymous, about FROM User WHERE email IN (SELECT DISTINCT user FROM Post WHERE forum = %s)" 
    params = [short_name]   
    if "since_id" in optional:
        query += " AND id >= %s" 
        params.append(optional["since"])
    if "order" in  optional:
        query += " ORDER BY name " + str(optional["order"])
    else:
        query += " ORDER BY name DESC "
    if "limit" in optional:
        query += " LIMIT " + str(optional["limit"])
    
    users_ids = DB_connect.select_query(connect, query, params)
    user_list = []
    for user in users_ids:        
        usr = {
            'id'         : user[0],
            'email'      : user[1],            
            'name'       : user[2], 
            'username'   : user[3],           
            'isAnonymous': bool(user[4]),
            'about'      : user[5],                  
        }
        usr["followers"] = users.followers(connect, usr["email"], "user")
        usr["following"] = users.followers(connect, usr["email"], "follow")
        usr["subscriptions"] = users.subscriptions(connect, usr["email"])
        user_list.append(usr) 
    return user_list