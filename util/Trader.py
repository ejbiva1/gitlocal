class Trader:
    # judge position status
    @staticmethod
    def position_judge(position, strategy_id):
        if position == True:
            return True
        else:
            return False
    #
    # @staticmethod
    # def buy(cost, amount, position):
    #     if Trader.position_judge(position):
    #         # todo  do buy
    #         return 1
    #     else:
    #         return 0
    #
    # @staticmethod
    # def sell(price, amount, postion):
    #     return 0
