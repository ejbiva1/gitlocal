# coding:utf-8

import pymysql
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session


#
# class OPMysql:
#     # __pool = None
#
#     # self.cur = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
def get_engine():
    # engine = create_engine('mysql+pymysql://root:Quant123@35.162.98.89:3306/quantcoin?charset=utf8MB4',
    #                        max_overflow=0,  # 超过连接池大小外最多创建的连接
    #                        pool_size=5,  # 连接池大小
    #                        pool_timeout=30,  # 池中没有线程最多等待的时间，否则报错
    #                        pool_recycle=-1  # 多久之后对线程池中的线程进行一次连接的回收（重置）
    #                        )
    engine = create_engine('mysql+pymysql://root:Quant123@52.163.218.233:3306/quantcoin?charset=utf8MB4',
                           max_overflow=0,  # 超过连接池大小外最多创建的连接
                           pool_size=5,  # 连接池大小
                           pool_timeout=30,  # 池中没有线程最多等待的时间，否则报错
                           pool_recycle=-1  # 多久之后对线程池中的线程进行一次连接的回收（重置）
                           )

    SessionFactory = sessionmaker(bind=engine)
    # session = scoped_session(SessionFactory)
    return engine
