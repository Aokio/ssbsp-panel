import sqlite3
import json
import os
from random import choice
import string
conn = sqlite3.connect("/etc/byte/bsp.db")
cur = conn.cursor()

def initdb():
    cur.execute('''CREATE TABLE user_info
       (id INTEGER PRIMARY KEY  autoincrement NOT NULL,
       email           CHAR(50)    ,
       username        CHAR(50)    NOT NULL,
       user_passwd     CHAR(50)    NOT NULL,
       port            INTEGER     NOT NULL,
       port_passwd     CHAR(50)    NOT NUll,
       flux            INTEGER     NOT NULL default 0,
       invite_code     CHAR(50)    NOT NULL,       
       flux_limit      INTEGER     NOT NULL,
       create_at       DATETIME    NOT NULL default CURRENT_TIMESTAMP,
       update_at       DATETIME    NOT NULL default CURRENT_TIMESTAMP
       );''')
       
    cur.execute('''CREATE TABLE invate_code
       (id INTEGER PRIMARY KEY  autoincrement NOT NULL,
       username        CHAR(50)    NOT NULL,
       port            INTEGER     NOT NULL,
       code            CHAR(50)    NOT NULL,       
       flux_limit      INTEGER     NOT NULL,
       is_activate     INTEGER     NOT NULL default 0,
       create_at       DATETIME    NOT NULL default CURRENT_TIMESTAMP,
       update_at       DATETIME    NOT NULL default CURRENT_TIMESTAMP
       );''')
    print "Table created successfully";
    conn.commit()

def GenPassword(length=8,chars=string.ascii_letters+string.digits):
    return ''.join([choice(chars) for i in range(length)])

def get_ports_info(port):
    cur.execute("select email, username, limit, limit_flux from port_flux where port = {}".format(port))
    por_info = cur.fetchall()
    return por_info

def get_invite_info(invate_code):
    cur.execute("select port, limit from invate_code where code='{}' and is_activate=0 ".format(invate_code))
    code_info = cur.fetone()
    if code_info:
        return code_info
    else:
        return 0

def check_user_exeist(username):
    cur.execute("select * from user_info where username='{}'".format(username))
    user = cur.fetchone()
    if user:
        return 1
    else:
        return 0

def add_user(username, password, invite_code):

    code_info = get_invite_info(invate_code)
    if check_user_exeist(username):
        return 0
    else:
        user_passwd = password

    if code_info:
        port = code_info[0]
        port_passwd = GenPassword(16)
        flux_limit = code_info[1]
        try:
            cur.exccute("insert into user_info (username, user_passwd, port, port_passwd, flux_limit, invite_code) values ('{}', '{}', {}, '{}', {}, '{}')".format(username,user_passwd,port,port_passwd,flux_limit, invite_code))
            os.system("bsp -p {} -P '{}' -s {} -a -A -j".format(port, passwd, flux_limit))
            conn.commit()
        except Exception as e:
            conn.rollback()
    else:   
        return 0

if __name__ == "__main__":
    initdb()