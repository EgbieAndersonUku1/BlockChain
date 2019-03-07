from transactions.transaction import Transaction
from blocks.block import Block
from rewards.mining_reward import MiningRewards
from utils.converter import Converter
from utils.files import FileHandler
from utils.security.verification import Verification
from wallets.wallet import Wallet


class Blockchain(object):

    def __init__(self, hosting_node_id):

        self.chain = self._get_genesis_block()
        self._open_transactions = []
        self.load_data()
        self.hosting_node = hosting_node_id

    def get_open_transactions(self):
        return Transaction.convert_all_transaction_block_to_ordered_dict(self._open_transactions)

    def load_data(self):
        """Initialize blockchain + open transactions data from a file."""
        try:

            file_content = FileHandler.load()
        except (IOError, IndexError):
            self.chain = self._get_genesis_block()
        else:
            blockchain, open_trans = self._extract_blockchain_and_open_transactions_block_from_file_content(file_content)
            self._update_current_block_chain(blockchain)
            self._update_current_open_transactions(open_trans)

    def _get_genesis_block(self):
        """"""
        genesis_block = Block(0, '', [], 0, 0)
        return [genesis_block]

    def _extract_blockchain_and_open_transactions_block_from_file_content(self, file_content):

        block_chain = Converter.de_serialize_object(file_content[0][:-1])
        transactions_block = Converter.de_serialize_object(file_content[1])
        return block_chain, transactions_block

    def _update_current_block_chain(self, blockchain):
        """"""
        updated_blockchain = []

        for block in blockchain:
            trans_block = [Transaction(tx['sender'], tx['recipient'], tx['signature'], tx['amount']) for tx in block['transactions']]
            block = Block(block['index'], block['previous_hash'], trans_block, block['proof'], block['timestamp'])
            updated_blockchain.append(block)

        self.chain = updated_blockchain

    def _update_current_open_transactions(self, open_transactions):
        """"""
        # We need to convert  the loaded data because Transactions should use OrderedDict
        updated_transactions = []
        for tx in open_transactions:
            updated_transaction = Transaction(tx['sender'], tx['recipient'], tx['signature'], tx['amount'])
            updated_transactions.append(updated_transaction)
        self._open_transactions = updated_transactions

    def save_data(self):
        """Save blockchain + open transactions snapshot to a file."""
        try:

            FileHandler.clear_file_content()
            FileHandler.write(Converter.to_json(self._create_savable_block()))
            FileHandler.write("\n")
            FileHandler.write(Converter.to_json(self._convert_object_in_transaction_block_to_json()))

        except IOError:
            print('Saving failed!')

    def _create_savable_block(self):
        return [block.to_json() for block in [Block(block.index, block.previous_hash,
                                                    [tx.to_json() for tx in block.transactions],
                                                    block.proof, block.timestamp) for block in self.chain]]

    def _convert_object_in_transaction_block_to_json(self):
        return [tx.to_json() for tx in self._open_transactions]

    def proof_of_work(self):
        """Generate a proof of work for the open transactions, the hash of the previous
        block and a random number (which is guessed until it fits)."""

        hashed_block = Block.hash_block(self._get_last_block_in_block_chain())

        proof = 0

        while not Verification.check_proof_validation(self._open_transactions, hashed_block, proof):
            proof += 1
        return proof

    def get_balance(self):
        """Calculate and return the balance for a participant."""

        if self.hosting_node is None:
            return None
        return Transaction.get_balance(self.hosting_node, self.chain, self._open_transactions)

    def get_last_blockchain_value(self):
        """ Returns the last value of the current blockchain. """
        return None if len(self.chain) < 1 else self.chain[-1]

    def add_transaction(self, recipient, sender, signature, amount=1.0):
        """ Append a new value as well as the last blockchain value to the blockchain.

        Arguments:
            :sender: The sender of the coins.
            :recipient: The recipient of the coins.
            :amount: The amount of coins sent with the transaction (default = 1.0)
        """

        if self._is_hosting_node_none():
            return False

        transaction = Transaction(sender, recipient, signature, amount)

        if Verification.verify_transaction(transaction, self.get_balance):

            signature = Wallet.verify_signature(transaction)

            if signature:
                self._open_transactions.append(transaction)
                self.save_data()
                return True
            return False

        self._delete_invalid_transaction_block()
        return False

    def mine_block(self):
        """Create a new block and add open transactions to it."""

        if self._is_hosting_node_none():
            return None

        hashed_block = Block.hash_block(self._get_last_block_in_block_chain())
        proof = self.proof_of_work()
        copied_transactions = self._get_duplicate_open_transaction_block()

        if self._verify_all_signatures_in_transaction_block(copied_transactions):

            copied_transactions.append(MiningRewards.get_mine_reward(self.hosting_node))

            new_block = Block.create_new_block(self.chain, hashed_block, copied_transactions, proof)
            self.chain.append(new_block)
            self._reset_open_transactions()

            self.save_data()
            return new_block

        self._delete_invalid_transaction_block()
        return None

    def convert_a_single_block_to_dict(self, block):

        json_block = block.to_json()
        json_block['transactions'] = Transaction.convert_all_transaction_block_to_ordered_dict(json_block['transactions'])
        return json_block

    def convert_entire_block_chain_to_dict(self):
        """"""

        chains_snapshot = [chain.to_json() for chain in self.chain]

        for chain in chains_snapshot:
            chain['transactions'] = Transaction.convert_all_transaction_block_to_ordered_dict(chain['transactions'])
        return chains_snapshot

    def _is_hosting_node_none(self):
        return self.hosting_node is None

    def _verify_all_signatures_in_transaction_block(self, transactions):

        for transaction in transactions:
            if not Wallet.verify_signature(transaction):
                return False
        return True

    def _get_last_block_in_block_chain(self):
        return None if len(self.chain) < 1 else self.chain[-1]

    def _reset_open_transactions(self):
        self._open_transactions = []

    def _delete_invalid_transaction_block(self):

        self._reset_open_transactions()
        self.save_data()

    def _get_duplicate_open_transaction_block(self):
        return self._open_transactions[:]