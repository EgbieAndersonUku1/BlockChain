from flask import jsonify, request, send_from_directory
from flask_script import Manager, Server
from flask_cors import CORS

from app import wallet, block_chain
from app import create_app


app = create_app()
manager = Manager(app)
CORS(app)

manager.add_command("runserver", Server(use_reloader=True, use_debugger=True, port=5001
                                        ))

@app.route("/", methods=['GET'])
def get_user_interface():
    return send_from_directory("user_interface", "node.html")


@app.route("/wallet/create/keys", methods=['POST'])
def create_keys():

    responses = {}

    wallet.create_keys()

    if wallet.save_keys():
        responses["public_key"] = wallet.public_key
        responses["private_key"] = wallet.private_key

        block_chain.hosting_node = wallet.public_key

        return jsonify(responses), 200

    responses['created_keys'] = "Failed to create keys"
    return jsonify(responses), 501


@app.route("/wallet/load/keys", methods=["GET"])
def load_keys():
    """"""
    responses = {}

    if wallet.load_existing_keys():
        responses["public_key"] = wallet.public_key
        responses["private_key"] = wallet.private_key

        block_chain.hosting_node = wallet.public_key

        return jsonify(responses), 200

    responses['load_keys'] = "Failed to load keys"
    return jsonify(responses), 501


@app.route("/transactions/fetchall", methods=['GET'])
def get_all_transactions():
    return jsonify(result=block_chain.get_open_transactions()), 200


@app.route("/transactions/add", methods=['POST'])
def add_transaction():

    responses = {}
    values = request.get_json()
    status_code = None
    success = False
    signature = None

    if wallet.public_key is None:
        responses['messages'] = "The public key is not setup"
        return jsonify(responses), 400

    elif not values:
        responses['messages'] = "No data found"

    if _are_transactions_field_valid(values):

        signature = wallet.sign_transaction(wallet.public_key, values['recipient'], values['amount'])
        success = block_chain.add_transaction(values['recipient'], wallet.public_key, signature, values['amount'])

    else:
        responses["message"] = "Reguired data fields missing"

    if success:

        responses["message"] = "Successfully added transaction"
        responses["transactions"] = {
            "sender": wallet.public_key,
            "recipient": values["recipient"],
            "amount":  values["amount"],
            "signature": signature,
        }
        responses["funds"] = block_chain.get_balance()
        status_code = 201
    else:
        responses["message"] = "Failed to add transactions"
        status_code = 400

    return jsonify(responses), status_code


def _are_transactions_field_valid(values):

    required_fields = ["recipient", "amount"]

    if all([field in values for field in required_fields]):
        return True
    return False


@app.route("/wallet/balance", methods=['GET'])
def get_balance():

    response = {}
    balance = block_chain.get_balance()
    status_code = None

    if balance:
        response['message'] = "The balance was successully received"
        response["wallet_set_up"] = wallet.public_key
        response["funds"] = block_chain.get_balance()
        status_code = 200

    else:
        response["message"] = "Falied to load the balance"
        response["wallet_set_up"] = wallet.public_key is not None
        status_code = 500

    return jsonify(response), status_code


@app.route("/mine", methods=['POST'])
def mine_block():

    response = {}
    block = block_chain.mine_block()

    if block is not None:

        response['message'] = "Block was successfully added"
        response['block'] = block_chain.convert_a_single_block_to_dict(block)
        response["wallet_set_up"] = wallet.public_key is not None
        response["funds"] = block_chain.get_balance()

        return jsonify(response), 201

    response['message'] = "Failed to add block"
    response["wallet_set_up"] = wallet.public_key is not None

    return jsonify(response), 501


@app.route("/chain", methods=["GET"])
def get_chain():
    return jsonify(results=block_chain.convert_entire_block_chain_to_dict()), 200



if __name__ == "__main__":
    manager.run()