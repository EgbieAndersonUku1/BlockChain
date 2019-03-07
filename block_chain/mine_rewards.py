from transactions.transaction import Transaction


class MiningReward(object):

    @staticmethod
    def get_reward(hosting_node_id):

        MINING_REWARD = 10
        OWNER = ""

        return Transaction("MINING", hosting_node_id, MINING_REWARD)
