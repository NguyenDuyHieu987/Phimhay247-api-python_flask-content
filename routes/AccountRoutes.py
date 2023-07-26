from flask import *
from flask_cors import cross_origin
import configs
from controllers.AccountControllers import Account


def account_routes(app):
    account = Account()

    @app.route("/account/change-password", methods=["POST"])
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def change_password_route(type):
        return account.change_password(type)
