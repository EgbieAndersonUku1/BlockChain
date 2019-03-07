from collections import OrderedDict

from utils.show import Display


class Transaction(Display):

    def __init__(self, sender, recipient, signature='', amount=0):
        self.sender = sender
        self.recipient = recipient
        self.signature = signature
        self.amount = amount

    @staticmethod
    def convert_all_transaction_block_to_ordered_dict(transactions_block):
        return [tx.to_ordered_dict() for tx in transactions_block]

    @classmethod
    def get_balance(cls, client, block_chain, open_transactions):
        return cls._process_transaction(client, block_chain, open_transactions)

    @classmethod
    def _process_transaction(cls, client, block_chain, open_transactions):
        """"""

        sent_coins_list = Transaction.get_all_sent_coins_transactions_list(block_chain, client)
        open_trans_coins_list = Transaction.get_all_open_sent_transactions_list(open_transactions, client)

        sent_coins_list.append(open_trans_coins_list)

        processed_received_coins = Transaction.get_all_processed_received_coins_list(client, block_chain)

        amount_sent = Transaction.calculate_amount(sent_coins_list)
        amount_received = Transaction.calculate_amount(processed_received_coins)

        return amount_received - amount_sent

    @classmethod
    def get_all_sent_coins_transactions_list(cls, block_chain, participant):
        return [[tx.amount for tx in block.transactions if tx.sender == participant] for block in block_chain]

    @classmethod
    def get_all_open_sent_transactions_list(cls, open_transactions, participant):
        return [tx.amount for tx in open_transactions if tx.sender == participant]

    @staticmethod
    def get_all_processed_received_coins_list(participant, block_chain):
        return [[tx.amount for tx in block.transactions if tx.recipient == participant] for block in block_chain]

    @classmethod
    def _calculate_balance(cls, sent_coins_list, received_coins_list):

        amount_sent = cls.calculate_amount(sent_coins_list)
        received_coins = cls.calculate_amount(received_coins_list)

        return received_coins - amount_sent

    @classmethod
    def calculate_amount(cls, amount_list):
        return sum([sum(amount) for amount in amount_list if len(amount) > 0])

    def to_ordered_dict(self):
        return OrderedDict([('sender', self.sender), ('recipient', self.recipient), ('amount', self.amount)])

    def to_json(self):
        return self.__dict__.copy()
