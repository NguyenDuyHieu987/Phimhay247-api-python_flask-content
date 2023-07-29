from flask import *
from flask_cors import cross_origin
import configs
from controllers.AccountControllers import Account


def account_routes(app):
    account = Account()

    @app.route("/account/change-password", methods=["POST"])
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def change_password_route():
        return account.change_password()

    @app.route("/account/change-email", methods=["POST"])
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def change_email_route():
        return account.change_email()

    @app.route("/account/change-fullname", methods=["POST"])
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def change_fullname_route():
        return account.change_fullname()

    @app.route("/account/verify/<type>", methods=["POST"])
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def account_verify_route(type):
        return account.account_verify(type)
