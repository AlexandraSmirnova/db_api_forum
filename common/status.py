__author__ = 'AS'

from common.DB_connect import *
from common import DB_connect

def status():
    con = connect()
    result = {}
    tables = ['User', 'Thread', 'Forum', 'Post' ]
    for table in tables:
        count  = DB_connect.select_query(con,"SELECT count(*) FROM " + table, ())
        result[table.lower()] = count[0][0]
    con.close()
    return result
