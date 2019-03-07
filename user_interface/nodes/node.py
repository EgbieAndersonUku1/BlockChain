from utils.security.verification import Verification
from block_chain.block_chain import BlockChain


class Node(object):

    def __init__(self):
        self.node_id = "egbie"
        self.block_chain = BlockChain(self.node_id)

    def run(self):

        running = True

        while running:

            self.display_menu()
            choice = self.get_user_choice()

            if choice == "1":
                transaction_amount = self.get_transaction_value()
                if self.block_chain.add_transaction(transaction_amount['recipient'], self.node_id,
                                                    amount=transaction_amount['amount']):
                    print("Added transaction")
                else:
                    print("Transaction failed")

            elif choice == "2":
                self.block_chain.mine_block()
            elif choice == "3":
                self.display_blockchain_elements()
            elif choice.lower() == "q":
                running = False

            else:
                print("Invalid input")
            if not Verification.verify_chain(self.block_chain.block_chain):
                print("Invalid blockchain")
                break
            print(self.block_chain.get_balance())

        print("Done!")

    def display_menu(self):

        print("[1] Add a new transaction value")
        print("[2] Mine a new block")
        print("[3] Output the blockchain blocks")
        print("[4] Output participants")
        print("[5] Verify transactions")
        print("[h] Hack the blockchain")
        print("[q] Quit")

    def get_user_choice(self):
        return input("Your choice: ")

    def display_blockchain_elements(self, block_chain):
        """"""

        print("\n")
        print("-" * 80)
        for block in self.block_chain:
            print("Outputting block")
            print(block)
        print("\n")
        print("-" * 80)

    def get_transaction_value(self):
        """Get the user transactional input value"""

        recipient = input("Enter the recipient of the transaction: ")
        amount = input("Please enter your transaction amount: ")

        return {"recipient": recipient, "amount": float(amount)}



node = Node()
node.run()