__author__ = 'AS'
from common import DB_connect
from User import u_queries as users
from Forum import f_queries as forums

def save_thread(connect, forum, title, isClosed, user, date, message, slug, optional):
    isDeleted = 0;
    if "isDeleted" in optional:
        isDeleted= optional["isDeleted"]
    str = DB_connect.update_query(connect,
                'INSERT INTO Thread (forum, title, isClosed, user, date, message, slug, isDeleted) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', 
                (forum, title, isClosed, user, date, message, slug, isDeleted, ))
    max_id = DB_connect.select_query(connect, 'SELECT max(id) FROM Thread', ())
    print(max_id[0][0])
    thread = DB_connect.select_query(connect, 
                'SELECT  date, forum, id,  isClosed,  isDeleted, message, slug,  title,  user FROM Thread  WHERE id = %s', (max_id[0][0], ) )    
    return thread_description(thread)



def thread_description(thread):
    thread = thread[0]
    response = {
        'date':      str(thread[0]),
        'forum':     thread[1],
        'id':        thread[2],
        'isClosed':  bool(thread[3]),
        'isDeleted': bool(thread[4]),
        'message':   thread[5],
        'slug':      thread[6],
        'title':     thread[7],
        'user':      thread[8],
    }
    print(response)
    return response


def show_thread(connect, thread, related):
    thread_all = DB_connect.select_query(connect, 
                'SELECT  date, forum, id,  isClosed,  isDeleted, message, slug,  title,  user, dislikes, likes, posts, (likes - dislikes) as points \
                FROM Thread WHERE id = %s LIMIT 1;', (thread, ) )
    if len(thread_all) == 0:
         raise Exception('No thread with id=' + str(thread))
    thread = thread_description(thread_all) 
    thread["dislikes"] = thread_all[0][9]   
    thread["likes"]    = thread_all[0][10]
    thread["posts"]    = thread_all[0][11]
    thread["points"]   = thread_all[0][12]
    if "user" in related:
        thread["user"] = users.show_user(connect, thread["user"])
    if "forum" in related:
        thread["forum"] = forums.show_forum(connect, thread["forum"], [])
    return thread


def threads_list(connect, entity, params, identifier, related=[]):
    query = "SELECT date, forum, id, isClosed, isDeleted, message, slug, title, user, dislikes, likes, (likes - dislikes) as points, posts  \
            FROM Thread WHERE " + entity + " = %s "
    parameters = [identifier]
    if "since" in params:
        query += " AND date >= %s"
        parameters.append(params["since"])

    if "order" in  params:
        query += " ORDER BY date " + str(params["order"])
    else:
        query += " ORDER BY date DESC "

    if "limit" in params:
        
        query += " LIMIT " + str(params["limit"])

    thread_ids = DB_connect.select_query(connect, query, parameters)
    thread_list = []
    for thread in thread_ids:
        thr = {
            'date': str(thread[0]),
            'forum': thread[1],
            'id': thread[2],
            'isClosed': bool(thread[3]),
            'isDeleted': bool(thread[4]),
            'message': thread[5],
            'slug': thread[6],
            'title': thread[7],
            'user': thread[8],
            'dislikes': thread[9],
            'likes': thread[10],
            'points': thread[11],
            'posts': thread[12],
        }
        if "user" in related:
            thr["user"] = users.show_user(connect,thr["user"])
        if "forum" in related:
            thr["forum"] = forums.show_forum(connect, thr["forum"], [])    
        thread_list.append(thr)    
    return thread_list


def update_thread(connect, message, slug, thread):
    DB_connect.update_query(connect,'UPDATE Thread SET message = %s, slug = %s WHERE id = %s',
                           (message, slug, thread, ))
    return show_thread(connect,thread, [])


def open_close_thread(connect, thread, isClosed):
    DB_connect.update_query(connect,'UPDATE Thread SET isClosed = %s WHERE id = %s', (isClosed, thread,))
    return {
        "thread": thread 
    }


def remove_restore(connect,thread, isDeleted):
    if isDeleted == 1:
        posts = 0
    else:
        posts = DB_connect.select_query(connect,"SELECT COUNT(id) FROM Post WHERE thread = %s", (thread, ))[0][0]
    DB_connect.update_query(connect,"UPDATE Thread SET isDeleted = %s, posts = %s WHERE id = %s", (isDeleted,posts, thread ))
    DB_connect.update_query(connect,"UPDATE Post SET isDeleted = %s WHERE thread = %s", (isDeleted,thread, ))
    return {
        "thread": thread    
    }


def subscribe_user(connect, thread, user):
    isDeleted = 0;

    DB_connect.update_query(connect, "INSERT INTO Subscription (user, thread_id, isDeleted) VALUES (%s, %s, %s)", (user, thread, isDeleted))
    return {
        "thread": thread,
        "user":   user
    }


def unsubscribe_user(connect, thread, user):
    isDeleted = 1;
    try:   
        DB_connect.update_query(connect, "UPDATE Subscription SET isDeleted = %s WHERE user = %s AND thread_id = %s ",(isDeleted, user, thread,))
    except Exception as e:
        raise Exception("user " + user + " does not subscribe thread #" + str(thread))
    return {
        "thread": thread,
        "user":   user
    }



def inc_posts_count(connect,post):
    thread = DB_connect.select_query(connect,"SELECT thread FROM Post WHERE id = %s", (post, ))
    DB_connect.update_query(connect,"UPDATE Thread SET posts = posts + 1 WHERE id = %s", (thread[0][0], ))
    return

def dec_posts_count(connect,post):
    thread = DB_connect.select_query(connect,"SELECT thread FROM Post WHERE id = %s", (post, ))
    try:
        DB_connect.update_query(connect,"UPDATE Thread SET posts = posts - 1 WHERE id = %s", (thread[0][0], ))
    except Exception as e:
        print(e.message)
    return


def vote_for_thread(connect, thread, vote):
    print(vote)
    if (vote == 1):        
        DB_connect.update_query(connect,'UPDATE Thread SET likes = likes + 1  WHERE id = %s', (thread, ))
    else: 
        if (vote == -1):            
            DB_connect.update_query(connect,'UPDATE Thread SET dislikes = dislikes + 1  WHERE id = %s',(thread, ))
        else:
            raise Exception("VallueError")
    return show_thread(connect, thread, [])