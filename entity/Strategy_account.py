# 导入:
from sqlalchemy import Column, create_engine
from sqlalchemy.types import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类:
Base = declarative_base()


# 定义Account对象:
class Account(Base):
    # 表的名字:
    __tablename__ = 'strategy_account'

    # 表的结构:
    strategy_account_id = Column(Integer, primary_key=True)
    strategy_log_id = Column(Integer)
    current_cash_balance = Column(DECIMAL(20, 6))
    current_coin_balance = Column(DECIMAL(20, 6))
    cost = Column(DECIMAL(20, 6))
    total_net_balance = Column(DECIMAL(20, 6))
    current_net_value = Column(DECIMAL(20, 6))
    current_total_margin_rate = Column(DECIMAL(20, 6))
    current_margin_rate = Column(DECIMAL(20, 6))
    current_position = Column(DECIMAL(20, 6))
    signal = Column(Integer)
    transaction_status = Column(Integer)
    t = Column(BIGINT)
    open = Column(DECIMAL(20, 6))
    close = Column(DECIMAL(20, 6))
    high = Column(DECIMAL(20, 6))
    low = Column(DECIMAL(20, 6))


# 初始化数据库连接:
engine = create_engine('mysql+pymysql://root:Quant123@35.162.98.89:3306/quantcoin?charset=utf8MB4')
# 创建DBSession类型:
AccountDBSession = sessionmaker(bind=engine)
