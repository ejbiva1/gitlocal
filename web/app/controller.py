
import web.app.DB as db;

def getStrategy():
    return db.getStrategy()


def getLogList(strategy_instance_id):
    return db.getStrategyInstanceLogList(strategy_instance_id)


def getStrategyInstance(strategy_id):
    return db.getStrategyInstance(strategy_id)