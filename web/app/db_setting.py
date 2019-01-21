#!/usr/bin/env python
# -*- coding:utf-8 -*-

from DBUtils.PooledDB import PooledDB, SharedDBConnection
import pymysql

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

try:
    DB_ONLINE = PooledDB(
        creator=pymysql,
        maxconnections=100,
        mincached=20,
        maxcached=50,
        maxshared=30,
        blocking=True,
        maxusage=None,
        setsession=[],
        ping=1,
        host='localhost',
        port=3306,
        user='root',
        password='Quant123',
        database='quantcoin',
        charset='utf8'
    )
except Exception:
    print("sql connt error")

# database config
default_db = DB_ONLINE


def fetch_db(sql):
    conn = default_db.connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    conn.close()

    return result


def fetch_one(sql):
    conn = default_db.connection()
    cursor = conn.cursor()
    result = cursor.fetchone(sql)
    conn.close()

    return result

#
# def fetch_one_list():
#     conn = default_db.connection()
#     cursor = conn.cursor()
#     result = cursor.fetchone()
#     conn.close()
#
#     return result


def fetch_db_with_param(sql, params):
    conn = default_db.connection()
    cursor = conn.cursor()
    cursor.execute(sql, params)
    result = cursor.fetchall()
    conn.close()
    return result


def update_db(sql):
    conn = default_db.connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    result = conn.commit()
    conn.close()

    return result


def insert_db(sql):
    conn = default_db.connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    result = conn.commit()
    conn.close()

    return result


def update_db_with_params(sql, params):
    conn = default_db.connection()
    cursor = conn.cursor()
    cursor.execute(sql, params)
    result = conn.commit()
    conn.close()

    return result
