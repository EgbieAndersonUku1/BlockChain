from transactions.transaction import Transaction


class MiningReward(object):

    @classmethod
    def get_reward(cls, hosting_node_id):

        MINING_REWARD = 10
        OWNER = ""

        return Transaction("MINING", hosting_node_id, MINING_REWARD)
