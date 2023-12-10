from flask import *

# from flask_cors import cross_origin
import configs
from controllers.AccountControllers import Account


def account_routes(app):
    account = Account()

    @app.route("/account/confirm/<type>", methods=["POST"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def account_confirm_route(type):
        return account.account_confirm(type)

    @app.route("/account/change-password", methods=["POST"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def change_password_route():
        return account.change_password()

    @app.route("/account/change-email", methods=["POST"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def change_email_route():
        return account.change_email()

    @app.route("/account/verify-email", methods=["POST"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def verify_email_route():
        return account.verify_email()

    @app.route("/account/reset-password", methods=["GET"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def reset_password_retrieve_token_route():
        return account.reset_password_retrieve_token()

    @app.route("/account/reset-password", methods=["POST"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def reset_password_route():
        return account.reset_password()
