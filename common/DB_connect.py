__author__ = 'ASmirnova'

import MySQLdb as db

def connect():
    return db.connect(host="localhost",
                      user="admin",
                      passwd="secret",
                      db="forumdb",
                      charset="utf8")


def select_query(connect,query, params):
    try:
        cursor = connect.cursor()
        cursor.execute(query, params)
        result = cursor.fetchall()
        cursor.close()
    except db.Error:
        cursor.close()        
        raise Exception("Database error in usual query")
    return result


def execute(connect,query):
    try:
        cursor = connect.cursor()
        cursor.execute(query)
        connect.commit()
        cursor.close()
    except db.Error:
        connect.rollback()
	cursor.close()
    return

def update_query(connect,query, params):
    try:
        cursor = connect.cursor()

        cursor.execute(query, params)
        
        inserted_id = cursor.lastrowid
        connect.commit()
        cursor.close()
    except ValueError:
        connect.rollback()
        cursor.close()  
        raise Exception("ValueError")
    except KeyError:
        connect.rollback()
        cursor.close()  
        raise Exception("KeyError")
    except db.Error:
        connect.rollback()
        cursor.close()
        raise Exception("Exist")
    return inserted_id

