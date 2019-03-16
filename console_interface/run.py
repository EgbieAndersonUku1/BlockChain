
from console_interface.menu import Menu
from block_chain.blockchain import Blockchain
from console_interface.user_choice import UserChoice
from wallets.wallet import Wallet



class Node(object):

    def __init__(self):
        self._wallet = Wallet()
        self._wallet.create_keys()
        self._id = self._wallet.public_key
        self._block_chain = Blockchain(hosting_node_id=self._id)

    def listen(self):

        waiting = True

        while waiting:

            Menu.display()
            choice = UserChoice.get_user_choice()

            if choice == "a":
                recipient = UserChoice.get_recipient_name()
                amount = UserChoice.get_amount()

                if recipient and amount:
                    signature = self._wallet.sign_transaction(self._id, recipient, amount)

                    if self._block_chain.add_transaction(recipient, self._id, signature, amount):
                        print("Transaction successfully added.")
                    else:
                        print("Failed  to add transaction")

            elif choice == 'm':
                if not self._block_chain.mine_block():
                    print("Failed to mine block because no wallet was found!!")
                else:
                    print("Successfully mined a block")

            elif choice == 'c':
                self._wallet.create_keys()
                self._id = self._wallet.public_key
                self._block_chain = Blockchain(self._wallet.public_key)
                print("[+] Keys successfully created.")


node = Node()
node.listen()

