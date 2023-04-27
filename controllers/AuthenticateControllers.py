import pymongo
from pymongo.errors import PyMongoError
from utils.JsonResponse import ConvertJsonResponse as cvtJson
from utils.ErrorMessage import errorMessage
from flask import *
from pymongo import ReturnDocument
import jwt
import os
from datetime import datetime, timezone, timedelta


myclient = pymongo.MongoClient(
    "mongodb+srv://admin:hieusen123@the-movie-database.fczrzon.mongodb.net/Phimhay247_DB"
)

db = myclient["Phimhay247_DB"]

# try:
#     encoded = jwt.encode(
#         {
#             "email": 123,
#             "password": 456,
#             "exp": datetime.now(tz=timezone.utc)
#             + timedelta(seconds=int(os.getenv("TIME_OFFSET")) * 60 * 60),
#         },
#         str(os.getenv("ACCESS_TOKEN_SECRET")),
#         algorithm="HS256",
#     )

#     print(encoded)

#     decode = jwt.decode(
#         encoded,
#         "@HIEUSEN123",
#         algorithms=["HS256"],
#     )
#     print(decode)
#     print(int(datetime.now(tz=timezone.utc).timestamp()))
#     if int(decode["exp"]) - int(datetime.now(tz=timezone.utc).timestamp()) > (
#         int(os.getenv("TIME_OFFSET")) * 60 * 60
#     ):
#         print("decode")


# except jwt.ExpiredSignatureError as e:
#     print(e)
# except jwt.exceptions.DecodeError as e:
#     print(e)


def login():
    formUser = request.form
    try:
        account = db["accounts"].find_one({"email": formUser["email"]})
        if account != None:
            if account["password"] == formUser["password"]:
                # get_account = db["accounts"].find_one_and_update(
                get_account = db["accounts"].find_one(
                    {"email": formUser["email"], "password": formUser["password"]},
                    # {
                    #     "$set": {
                    #         "user_token": formUser["user_token"],
                    #     }
                    # },
                    # return_document=ReturnDocument.AFTER,
                )

                encoded = jwt.encode(
                    {
                        "email": formUser["email"],
                        "password": formUser["password"],
                        "exp": datetime.now(tz=timezone.utc)
                        + timedelta(seconds=int(os.getenv("TIME_OFFSET")) * 60 * 60),
                    },
                    str(os.getenv("ACCESS_TOKEN_SECRET")),
                    algorithm="HS256",
                )

                return {
                    "isLogin": True,
                    "result": {
                        "id": get_account["id"],
                        "username": get_account["username"],
                        "full_name": get_account["full_name"],
                        "avatar": get_account["avatar"],
                        "email": get_account["email"],
                        "user_token": encoded,
                        "role": get_account["role"],
                    },
                }
            else:
                return {"isWrongPassword": True, "result": "Wrong Password"}
        else:
            return {"isNotExist": True, "result": "Account does not exists"}
    except:
        return {"isLogin": False, "result": "Log in failed"}


def loginfacebook():
    formUser = request.form.to_dict()
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
                formUser | {"role": "normal"},
            )

            get_account = db["accounts"].find_one(
                {
                    "id": formUser["id"],
                },
            )

            encoded = jwt.encode(
                {
                    "facebook_id": formUser["id"],
                    "exp": datetime.now(tz=timezone.utc)
                    + timedelta(seconds=int(os.getenv("TIME_OFFSET")) * 60 * 60),
                },
                str(os.getenv("ACCESS_TOKEN_SECRET")),
                algorithm="HS256",
            )

            return {
                "isSignUp": True,
                "result": {
                    "id": get_account["id"],
                    "username": get_account["username"],
                    "full_name": get_account["full_name"],
                    "avatar": get_account["avatar"],
                    "email": get_account["email"],
                    "user_token": encoded,
                    "role": get_account["role"],
                },
            }

        else:
            encoded = jwt.encode(
                {
                    "facebook_id": formUser["id"],
                    "exp": datetime.now(tz=timezone.utc)
                    + timedelta(seconds=int(os.getenv("TIME_OFFSET")) * 60 * 60),
                },
                str(os.getenv("ACCESS_TOKEN_SECRET")),
                algorithm="HS256",
            )

            # get_account = db["accounts"].find_one_and_update(
            get_account = db["accounts"].find_one(
                {"id": formUser["id"]},
                # {
                #     "$set": {
                #         "user_token": encoded,
                #         # "avatar": formUser["avatar"],
                #     },
                # },
                # return_document=ReturnDocument.AFTER,
            )

            return {
                "isLogin": True,
                "result": {
                    "id": get_account["id"],
                    "username": get_account["username"],
                    "full_name": get_account["full_name"],
                    "avatar": get_account["avatar"],
                    "email": get_account["email"],
                    "user_token": encoded,
                    "role": get_account["role"],
                },
            }

    except:
        return {"isLogin": False, "result": "Log in Facebook failed"}


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
            return {"isEmailExist": True, "result": "Email is already exists"}
    except:
        return {"isSignUp": False, "result": "Sign Up Failed"}


def getuser_by_token():
    # formUser = request.form
    user_token = request.headers["Authorization"].replace("Bearer ", "")
    try:
        jwtUser = jwt.decode(
            user_token,
            str(os.getenv("ACCESS_TOKEN_SECRET")),
            algorithms=["HS256"],
        )

        if "facebook_id" in jwtUser:
            facebook_account = db["accounts"].find_one(
                {"id": jwtUser["facebook_id"]},
            )
            if facebook_account == None:
                return {"isNotExist": True, "result": "Account does not exists"}
            else:
                return {
                    "isLogin": True,
                    "result": {
                        "id": facebook_account["id"],
                        "username": facebook_account["username"],
                        "full_name": facebook_account["full_name"],
                        "avatar": facebook_account["avatar"],
                        "email": facebook_account["email"],
                        "user_token": user_token,
                        "role": facebook_account["role"],
                    },
                }
        else:
            account = db["accounts"].find_one({"email": jwtUser["email"]})

            if account != None:
                if account["password"] == jwtUser["password"]:
                    get_account = db["accounts"].find_one(
                        {"email": jwtUser["email"], "password": jwtUser["password"]},
                    )

                    # encoded = jwt.encode(
                    #     {
                    #         "email": jwtUser["email"],
                    #         "password": jwtUser["password"],
                    #         "exp": datetime.now(tz=timezone.utc)
                    #         + timedelta(
                    #             seconds=int(os.getenv("TIME_OFFSET")) * 60 * 60
                    #         ),
                    #     },
                    #     str(os.getenv("ACCESS_TOKEN_SECRET")),
                    #     algorithm="HS256",
                    # )

                    return {
                        "isLogin": True,
                        "result": {
                            "id": get_account["id"],
                            "username": get_account["username"],
                            "full_name": get_account["full_name"],
                            "avatar": get_account["avatar"],
                            "email": get_account["email"],
                            "user_token": user_token,
                            "role": get_account["role"],
                        },
                    }
                else:
                    return {"isWrongPassword": True, "result": "Wrong Password"}
            else:
                return {"isNotExist": True, "result": "Account does not exists"}

    except:
        return {"isLogin": False, "result": "Log in failed"}
