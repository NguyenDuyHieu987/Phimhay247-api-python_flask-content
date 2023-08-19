from flask import *


def BadRequestMessage(
    message="The browser (or proxy) sent a request that this server could not understand",
):
    result = {
        "status_code": 400,
        "error": "Bad request",
        "message": str(message),
        "success": False,
    }
    abort(400, result)


def InternalServerErrorMessage(
    message="The server encountered an internal error and was unable to complete your request. Either the server is overloaded or there is an error in the application",
):
    result = {
        "status_code": 500,
        "error": "Internal Server Error",
        "message": str(message),
        "success": False,
    }
    abort(500, result)
