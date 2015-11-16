__author__ = 'AS'

from common.DB_connect import *
from common import *

def clear():
    con = connect()
    tables = ['Post', 'Thread', 'Forum', 'Subscription', 'Follow', 'User']
    DB_connect.execute(con,"SET SESSION FOREIGN_KEY_CHECKS = 0;")
    for table in tables:
        DB_connect.execute(con,"TRUNCATE TABLE %s;" % table)
    DB_connect.execute(con,"SET SESSION FOREIGN_KEY_CHECKS = 1;")
    con.close()
    return
