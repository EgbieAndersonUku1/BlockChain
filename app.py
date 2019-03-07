from flask import Flask
from flask_mongoengine import MongoEngine

from blockchain import Blockchain
from wallets.wallet import Wallet


db = MongoEngine()
wallet = Wallet()
block_chain = Blockchain(wallet.public_key)


def create_app():

    app = Flask(__name__)

    app.config.from_pyfile("settings.py")

    # initialise the database
    db.init_app(app)

    # add the blueprints
    from wallets.views import wallet_app

    # register the blueprints
    app.register_blueprint(wallet_app)



    return app