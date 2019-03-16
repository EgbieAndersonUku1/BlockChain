

class UserChoice(object):

    @staticmethod
    def get_recipient_name():
        """ Returns the input of the user (a new transaction amount) as a float. """
        return input('Enter the recipient of the transaction: ')

    @staticmethod
    def get_amount():
        return float(input('Your transaction amount please: '))

    @staticmethod
    def get_user_choice():
        """Prompts the user for its choice and return it."""
        return input('Your choice: ').lower()
