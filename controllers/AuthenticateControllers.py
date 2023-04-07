import pymongo
from pymongo.errors import PyMongoError
from utils.JsonResponse import ConvertJsonResponse as cvtJson
from utils.ErrorMessage import errorMessage
from flask import *
from pymongo import ReturnDocument

myclient = pymongo.MongoClient(
    "mongodb+srv://admin:hieusen123@the-movie-database.fczrzon.mongodb.net/Phimhay247_DB"
)

db = myclient["Phimhay247_DB"]


def login():
    formUser = request.form
    account = db["accounts"].find_one({"email": formUser["email"]})
    if account != None:
        if account["password"] == formUser["password"]:
            get_account = db["accounts"].find_one_and_update(
                {"email": formUser["email"], "password": formUser["password"]},
                {
                    "$set": {
                        "user_token": formUser["user_token"],
                    }
                },
                return_document=ReturnDocument.AFTER,
            )

            return {
                "isLogin": True,
                "result": {
                    "id": get_account["id"],
                    "username": get_account["username"],
                    "full_name": get_account["full_name"],
                    "avatar": get_account["avatar"],
                    "email": get_account["email"],
                    "user_token": get_account["user_token"],
                    "role": get_account["role"],
                },
            }
        else:
            return {"isLogin": False, "result": "Wrong Password"}
    else:
        return {"success": False, "result": "Account does not exists"}


def loginfacebook():
    formUser = request.form
    account = db["accounts"].find_one({"id": formUser["id"]})
    try:
        if account == None:
            list = db["lists"].find_one(
                {
                    "id": formUser["id"],
                },
            )

            newList = {
                "created_by": formUser["full_name"],
                "description": "List movie which users are added",
                "favorite_count": 0,
                "id": formUser["id"],
                "name": "List",
                "items": [],
            }

            if list == None:
                db["lists"].insert_one(newList)

            watchlist = db["watchlists"].find_one(
                {
                    "id": formUser["id"],
                },
            )

            newWatchList = {
                "created_by": formUser["full_name"],
                "description": "Videos which users watched",
                "favorite_count": 0,
                "id": formUser["id"],
                "item_count": 0,
                "name": "WatchList",
                "items": [],
            }

            if watchlist == None:
                db["watchlists"].insert_one(newWatchList)

            db["accounts"].insert_one(
                formUser.to_dict() | {"role": "normal"},
            )

            get_account = db["accounts"].find_one(
                {
                    "id": formUser["id"],
                },
            )

            return {
                "isSignUp": True,
                "result": {
                    "id": get_account["id"],
                    "username": get_account["username"],
                    "full_name": get_account["full_name"],
                    "avatar": get_account["avatar"],
                    "email": get_account["email"],
                    "user_token": get_account["user_token"],
                    "role": get_account["role"],
                },
            }

        else:
            get_account = db["accounts"].find_one_and_update(
                {"id": formUser["id"]},
                {
                    "$set": {
                        "user_token": formUser["user_token"],
                        "avatar": formUser["avatar"],
                    },
                },
                return_document=ReturnDocument.AFTER,
            )
            return {
                "isLogin": True,
                "result": {
                    "id": get_account["id"],
                    "username": get_account["username"],
                    "full_name": get_account["full_name"],
                    "avatar": get_account["avatar"],
                    "email": get_account["email"],
                    "user_token": get_account["user_token"],
                    "role": get_account["role"],
                },
            }
    except:
        return {"isLogin": False, "result": "Sign up Facebook failed"}


def signup():
    formUser = request.form
    account = db["accounts"].find_one({"email": formUser["email"]})
    try:
        if account == None:
            list = db["lists"].find_one(
                {
                    "id": formUser["id"],
                },
            )

            newList = {
                "full_name": formUser["full_name"],
                "description": "List movie which users are added",
                "favorite_count": 0,
                "id": formUser["id"],
                "name": "List",
                "items": [],
            }

            if list == None:
                db["lists"].insert_one(newList)

            watchlist = db["watchlists"].find_one(
                {
                    "id": formUser["id"],
                },
            )

            newWatchList = {
                "full_name": formUser["full_name"],
                "description": "Videos which users watched",
                "favorite_count": 0,
                "id": formUser["id"],
                "item_count": 0,
                "name": "WatchList",
                "items": [],
            }

            if watchlist == None:
                db["watchlists"].insert_one(newWatchList)

            if "role" in formUser.to_dict():
                db["accounts"].insert_one(formUser.to_dict())
            else:
                db["accounts"].insert_one(
                    formUser.to_dict() | {"role": "normal"},
                )

            get_account = db["accounts"].find_one(
                {"id": formUser["id"]},
            )

            return {
                "isSignUp": True,
                "result": {
                    "id": get_account["id"],
                    "username": get_account["username"],
                    "full_name": get_account["full_name"],
                    "avatar": get_account["avatar"],
                    "email": get_account["email"],
                    "user_token": get_account["user_token"],
                    "role": get_account["role"],
                },
            }
        else:
            return {"isSignUp": False, "result": "Email is already exists"}

    except PyMongoError as e:
        return {"isLogin": False, "result": e._message}


def getuser_by_token():
    formUser = request.form
    account = db["accounts"].find_one({"user_token": formUser["user_token"]})

    try:
        if account != None:
            return {
                "isLogin": True,
                "result": {
                    "id": account["id"],
                    "username": account["username"],
                    "full_name": account["full_name"],
                    "avatar": account["avatar"],
                    "email": account["email"],
                    "user_token": account["user_token"],
                    "role": account["role"],
                },
            }
        else:
            return {"isLogin": False, "result": "Account does not exist"}

    except PyMongoError as e:
        return {"isLogin": False, "result": e._message}
