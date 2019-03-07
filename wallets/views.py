from flask import Blueprint, jsonify
from app import wallet, block_chain


wallet_app = Blueprint("wallet_app", __name__, url_prefix="/wallet")


@wallet_app.route("/keys/create", methods=['POST'])
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


@wallet_app.route("/keys/load", methods=["GET"])
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