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


# 初始化数据库连接:
engine = create_engine('mysql+pymysql://root:Quant123@35.162.98.89:3306/quantcoin?charset=utf8MB4')
# 创建DBSession类型:
LogDBSession = sessionmaker(bind=engine)
