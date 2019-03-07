from transactions.transaction import Transaction


class MiningRewards(object):

    MINING_REWARD = 10

    @classmethod
    def get_mine_reward(cls, host_name):

        return Transaction("MINING", host_name, amount=cls.MINING_REWARD)

