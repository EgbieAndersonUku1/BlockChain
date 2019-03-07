from block.block import Block
from block_chain.mine_rewards import MiningReward
from transactions.transaction import Balance
from transactions.transaction import Transaction
from utils.converter import Converter
from utils.files import FileHandler
from utils.security.verification import Verification

participant = "Egbie"


class BlockChain(MiningReward):

    def __init__(self, hosting_node):
        self.block_chain = []
        self.open_transactions = []
        self.load_block_chain_data()
        self.hosting_node = hosting_node

    def load_block_chain_data(self):

        try:
            block_chain_data = FileHandler.load()
            block_chain, open_transactions = self._get_data_from_block_chain(block_chain_data)

            self._extract_block_chain(block_chain)
            self._extract_transactions(open_transactions)

        except(IOError, IndexError):
            self._load_genesis_block()

    def _load_genesis_block(self):
        """"""
        genesis_block = Block(0, '', [], 100, 0)
        self.block_chain = [genesis_block]
        self._reset_open_transactions()

    def _get_data_from_block_chain(self, block_chain_data):

        block_chain = Converter.de_serialize_object(block_chain_data[0][:-1])
        open_transactions = Converter.de_serialize_object(block_chain_data[1])

        return block_chain, open_transactions

    def _extract_transactions(self, open_transactions):

        updated_transactions = []
        for transaction in open_transactions:
            updated_transactions.append(Transaction.get_transactions_from_block(transaction))
        self.open_transactions = updated_transactions

    def _extract_block_chain(self, block_chain):

        updated_block_chain = []
        for block in block_chain:
            updated_transactions = Transaction.get_transactions_from_block(block)
            updated_block = Block(block["index"], block["previous_hash"], updated_transactions,
                                  block['proof'], block['time_stamp']
                                  )
            updated_block_chain.append(updated_block)
        self.block_chain = updated_block_chain

    def add_transaction(self, recipient, sender, amount):

        transaction = Transaction(sender, recipient, amount)
        transaction.create_new_transaction()
        self.open_transactions.append(transaction.get_transaction())
        self.save_data()

    def save_data(self):

        FileHandler.clear_file_content()
        FileHandler.write(Converter.to_json(self._create_savable_block_chain()))
        FileHandler.write("\n")
        FileHandler.write(Converter.to_json(self._create_savable_transaction_block()))

    def _create_savable_block_chain(self):
        """"""
        return [block.to_json() for block in [Block(block_el.index, block_el.previous_hash,
                                                             [tx.to_ordered_dictionary() for tx in block_el.transactions],
                                                             block_el.proof, block_el.time_stamp)
                                                             for block_el in self.block_chain]]

    def _create_savable_transaction_block(self):
        return [transaction.to_json() for transaction in self.open_transactions]

    def proof_of_work(self):

        last_block = self.get_last_block_chain_value()
        last_hash = Block.hash_block(last_block)

        proof = 0

        while not Verification.check_proof_validation(self.open_transactions, last_hash, proof):
            proof += 1
        return proof

    def get_balance(self):
        return Balance.get_balance(self.hosting_node, self.block_chain, self.open_transactions)

    def mine_block(self):

        hashed_block = Block.hash_block(self.get_last_block_chain_value())

        proof = self.proof_of_work()

        copied_transactions = self.open_transactions[:]
        copied_transactions.append(self.get_reward(self.hosting_node))

        self.block_chain.append(Block.create_block(hashed_block, self.block_chain, copied_transactions, proof))

        self._reset_open_transactions()
        self.save_data()

    def _reset_open_transactions(self):
        """"""
        self.open_transactions = []

    def get_last_block_chain_value(self):
        """Returns the last value in the block chain"""

        return None if len(self.block_chain) < 1 else self.block_chain[-1]