from utils.converter import Converter
from utils.printable import Display
from utils.security.verification import Verification


class Balance(object):

    @classmethod
    def get_balance(cls, participant, block_chain, open_transactions):

        amount_sent = Transaction.get_sender_transaction(participant, block_chain)
        amount_received = Transaction.get_recipient_transaction(participant, open_transactions)


        open_tx_sender = Transaction.get_all_open_user_transaction(participant, open_transactions)
        amount_sent.append(open_tx_sender)

        bal_sent = cls._calculate_balance(amount_sent)
        bal_received = cls._calculate_balance(amount_received)

        return bal_received - bal_sent

    @classmethod
    def _calculate_balance(cls, amount_list):
        return sum([sum(amount) for amount in amount_list if len(amount) > 0])


class Transaction(Display):

    def __init__(self, sender, recipient, amount):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
       # self._transactions = []

    def create_new_transaction(self):
        """"""

        open_transactions = []

        transaction = Transaction(self.sender, self.recipient, self.amount)

        if Verification.verify_transaction(transaction, Balance.get_balance):
            open_transactions.append(transaction)
        self._transactions = open_transactions

    def get_transaction(self):
        return self._transactions

    @classmethod
    def get_transactions_from_block(cls, block):
        """"""
        return [cls(transaction['sender'], transaction['recipient'], transaction['amount'])
                for transaction in block['transactions']]

    def to_ordered_dictionary(self):
        """"""
        return Converter.to_ordered_dict([('sender', self.sender), ('recipient', self.recipient),
                                          ('amount', self.amount)])

    @staticmethod
    def get_sender_transaction(participant, block_chain):
        return [[tx.amount for tx in block.transactions if tx.sender == participant] for block in block_chain]

    @staticmethod
    def get_recipient_transaction(participant, open_transactions):
        return [tx.amount for tx in open_transactions if tx.sender == participant]

    @staticmethod
    def get_all_open_user_transaction(participant, open_transactions):
        """"""
        return [tx.amount for tx in open_transactions if tx.sender == participant]
