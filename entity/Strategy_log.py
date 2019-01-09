# coding:utf-8
# 导入:
from sqlalchemy import Column, create_engine
from sqlalchemy.types import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

# 创建对象的基类:
Base = declarative_base()


# 定义Log对象:
class Log(Base):
    # 表的名字:
    __tablename__ = 'strategy_log'

    # 表的结构:
    strategy_log_id = Column(Integer, primary_key=True)
    strategy_id = Column(Integer)
    creator = Column(Integer)
    create_time = Column(TIMESTAMP, default=datetime.now)
    start_date = Column(BigInteger)
    end_date = Column(BigInteger)
    init_balance = Column(DECIMAL(10, 2))
    coin_category = Column(String(45))
    execution_result = Column(Integer)
    final_margin = Column(DECIMAL(10, 2))
    benchmark = Column(DECIMAL(10, 2))


# # 初始化数据库连接:
# engine = create_engine('mysql+pymysql://root:Quant123@35.162.98.89:3306/quantcoin?charset=utf8MB4',
#                        max_overflow=0,  # 超过连接池大小外最多创建的连接
#                        pool_size=5,  # 连接池大小
#                        pool_timeout=30,  # 池中没有线程最多等待的时间，否则报错
#                        pool_recycle=-1  # 多久之后对线程池中的线程进行一次连接的回收（重置）
#                        )
# # 创建DBSession类型:
# LogDBSession = sessionmaker(bind=engine)
