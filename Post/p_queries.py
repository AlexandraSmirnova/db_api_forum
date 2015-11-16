__author__ = 'AS'
from common import DB_connect
from User import u_queries as users
from Forum import f_queries as forums
from Thread import t_queries as threads


def save_post(connect, date, thread, message, user, forum, optional):
    try:
        query = "INSERT INTO Post (date, thread, message, user, forum "
        values = "(%s, %s, %s, %s, %s"
        parameters = [date, thread, message, user, forum]

        for param in optional:
            query += ", " + param
            values += ", %s"
            parameters.append(optional[param])
    except Exception as e:
        print e.message
    query += ") VALUES " + values + ")"
    str = DB_connect.update_query(connect, query, parameters)
    DB_connect.update_query(connect, "UPDATE Thread SET posts = posts + 1 WHERE id = %s", (thread, ))
    id_post = DB_connect.select_query(connect, "SELECT max(id) FROM  Post", ())
    post = DB_connect.select_query(connect, 
            "SELECT date, forum, id,  isApproved, isDeleted, isEdited, isHighlighted, isSpam, message, parent, thread, user \
                FROM Post WHERE forum = %s and thread = %s and user = %s and id = %s", (forum, thread, user, id_post[0][0] ) )
    response = post_description(post)
   
    return response


def post_description(post):
    post = post[0]
    response = {
        'date':         str(post[0]),
        'forum':        post[1],
        'id':           post[2],
        'isApproved':   bool(post[3]),
        'isDeleted':    bool(post[4]),
        'isEdited':     bool(post[5]),
        'isHighlighted':bool(post[6]),
        'isSpam':       bool(post[7]),        
        'message':      post[8],
        'parent':       post[9],        
        'thread':       post[10],
        'user':         post[11],

    }
    print(response)
    return response

def show_post(connect, post, related):
    post_all = DB_connect.select_query(connect, 
                'SELECT  date, forum, id,  isApproved, isDeleted, isEdited, isHighlighted, isSpam, message, \
                parent, thread, user,  dislikes, likes, (likes - dislikes) as points \
                FROM Post WHERE id = %s LIMIT 1;', (post, ) )
    if len(post_all) == 0:
         raise Exception('No post with id=' + str(post))
    post = post_description(post_all)  
    post["dislikes"] = post_all[0][12]  
    post["likes"]    = post_all[0][13]
    post["points"]   = post_all[0][14]
    if "user" in related:
        print("useeeeer")
        post["user"] = users.show_user(connect, post["user"])
    if "thread" in related:
        post["thread"] = threads.show_thread(connect, post["thread"], [])
    if "forum" in related:
        post["forum"] = forums.show_forum(connect, post["forum"], [])
    return post


def posts_list(connect, entity, params, identifier, related=[]):
    query = "SELECT date, dislikes, forum, id, isApproved, isDeleted, isEdited, isHighlighted, isSpam, likes, message,  \
            parent, (likes-dislikes) as points, thread, user FROM Post WHERE " + entity + " = %s "
    print("step2")
    parameters = [identifier]
    if "since" in params:
        query += " AND date >= %s"
        parameters.append(params["since"])

    if "order" in  params:
        query += " ORDER BY date " + params["order"]
    else:
        query += " ORDER BY date DESC "

    if "limit" in params:
        query += " LIMIT " + str(params["limit"])

    post_ids = DB_connect.select_query(connect, query, parameters)
    post_list = []
    for post in post_ids:        
        pf = {
                'date': str(post[0]),
                'dislikes': post[1],
                'forum': post[2],
                'id': post[3],
                'isApproved': bool(post[4]),
                'isDeleted': bool(post[5]),
                'isEdited': bool(post[6]),
                'isHighlighted': bool(post[7]),
                'isSpam': bool(post[8]),
                'likes': post[9],
                'message': post[10],
                'parent': post[11],
                'points': post[12],
                'thread': post[13],
                'user': post[14],
            }
        if "user" in related:
            pf["user"] = users.show_user(connect,pf["user"])
        if "forum" in related:
            pf["forum"] = forums.show_forum(connect, pf["forum"], [])
        if "thread" in related:
            pf["thread"] = threads.show_thread(connect, pf["thread"], [])
        post_list.append(pf)    
    return post_list


def delete_post(connect, post):
    is_deleted = 1
    str = DB_connect.update_query(connect, 
        'UPDATE Post SET  isDeleted = %s WHERE id =  %s', (is_deleted, post, ) )
    threads.dec_posts_count(connect, post)
    return {
        "post": post
    }


def restore_post(connect, post):
    is_deleted = 0
    str = DB_connect.update_query(connect, 
        'UPDATE Post SET  isDeleted = %s WHERE id =  %s', (is_deleted, post, ) )
    threads.inc_posts_count(connect, post)
    return {
        "post": post
    }


def update_post(connect, post, message):
    DB_connect.update_query(connect,'UPDATE Post SET message = %s WHERE id = %s',
                           (message, post, ))
    return show_post(connect,post, [])


def vote_for_post(connect, post, vote):
    print(vote)
    if (vote == 1):        
        DB_connect.update_query(connect,'UPDATE Post SET likes = likes + 1  WHERE id = %s', (post, ))
    else: 
        if (vote == -1):            
            DB_connect.update_query(connect,'UPDATE Post SET dislikes = dislikes + 1  WHERE id = %s',(post, ))
        else:
            raise Exception("VallueError")
    return show_post(connect, post, [])