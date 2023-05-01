import pymongo
from pymongo.errors import PyMongoError
from utils.JsonResponse import ConvertJsonResponse as cvtJson
from utils.ErrorMessage import errorMessage
from flask import *
from pymongo import ReturnDocument
import jwt
import os
from datetime import datetime, timezone, timedelta
import requests
import configs
from utils.Sendinblue_Email_Verification import Email_Verification
from utils.OTP_Generation import generateOTP


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
#             + timedelta(seconds=configs.TIME_OFFSET ),
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
#         configs.TIME_OFFSET
#     ):
#         print("decode")


# except jwt.ExpiredSignatureError as e:
#     print(e)
# except jwt.exceptions.DecodeError as e:
#     print(e)


def login():
    formUser = request.form
    try:
        account = db["accounts"].find_one(
            {"$and": [{"email": formUser["email"]}, {"auth_type": "email"}]}
        )
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
                        "id": get_account["id"],
                        "username": get_account["username"],
                        "password": get_account["password"],
                        "full_name": get_account["full_name"],
                        "avatar": get_account["avatar"],
                        "role": get_account["role"],
                        "email": get_account["email"],
                        "auth_type": get_account["auth_type"],
                        "exp": datetime.now(tz=timezone.utc)
                        + timedelta(seconds=configs.TIME_OFFSET),
                    },
                    str(os.getenv("ACCESS_TOKEN_SECRET")),
                    algorithm="HS256",
                )

                response = make_response(
                    {
                        "isLogin": True,
                        "result": {
                            "id": get_account["id"],
                            "username": get_account["username"],
                            "full_name": get_account["full_name"],
                            "avatar": get_account["avatar"],
                            "email": get_account["email"],
                            "auth_type": get_account["auth_type"],
                            "role": get_account["role"],
                            # "user_token": encoded,
                        },
                    }
                )
                response.headers.set("Access-Control-Expose-Headers", "Authorization")
                response.headers.set("Authorization", encoded)

                return response
            else:
                return {"isWrongPassword": True, "result": "Wrong Password"}
        else:
            return {"isNotExist": True, "result": "Account does not exists"}
    except:
        return {"isLogin": False, "result": "Log in failed"}


def loginfacebook():
    accessToken = request.headers["Authorization"].replace("Bearer ", "")

    faceBookUser = requests.get(
        f"https://graph.facebook.com/v15.0/me?access_token={accessToken}&fields=id,name,email,picture"
    )
    formUser = faceBookUser.json()

    account = db["accounts"].find_one({"id": formUser["id"]})

    try:
        if account == None:
            list = db["lists"].find_one(
                {
                    "id": formUser["id"],
                },
            )

            newList = {
                "created_by": formUser["name"],
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
                "created_by": formUser["name"],
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
                {
                    "id": formUser["id"],
                    "username": formUser["name"],
                    "full_name": formUser["name"],
                    "avatar": formUser["picture"]["data"]["url"],
                    "email": formUser.get("email", ""),
                    "auth_type": "facebook",
                    "role": "normal",
                },
            )

            get_account = db["accounts"].find_one(
                {
                    "id": formUser["id"],
                },
            )

            encoded = jwt.encode(
                {
                    "id": get_account["id"],
                    "username": get_account["username"],
                    "full_name": get_account["full_name"],
                    "avatar": get_account["avatar"],
                    "email": get_account["email"],
                    "auth_type": account["auth_type"],
                    "role": "normal",
                    "exp": datetime.now(tz=timezone.utc)
                    + timedelta(seconds=configs.TIME_OFFSET),
                },
                str(os.getenv("ACCESS_TOKEN_SECRET")),
                algorithm="HS256",
            )

            response = make_response(
                {
                    "isSignUp": True,
                    "result": {
                        "id": get_account["id"],
                        "username": get_account["username"],
                        "full_name": get_account["full_name"],
                        "avatar": get_account["avatar"],
                        "email": get_account["email"],
                        "auth_type": account["auth_type"],
                        "role": get_account["role"],
                        # "user_token": encoded,
                    },
                }
            )
            response.headers.set("Access-Control-Expose-Headers", "Authorization")
            response.headers.set("Authorization", encoded)

            return response

        else:
            encoded = jwt.encode(
                {
                    "id": account["id"],
                    "username": account["username"],
                    "full_name": account["full_name"],
                    "avatar": account["avatar"],
                    "email": account["email"],
                    "auth_type": account["auth_type"],
                    "role": "normal",
                    "exp": datetime.now(tz=timezone.utc)
                    + timedelta(seconds=configs.TIME_OFFSET),
                },
                str(os.getenv("ACCESS_TOKEN_SECRET")),
                algorithm="HS256",
            )

            # get_account = db["accounts"].find_one_and_update(
            # get_account = db["accounts"].find_one(
            #     {"id": formUser["id"]},
            #     # {
            #     #     "$set": {
            #     #         "user_token": encoded,
            #     #         # "avatar": formUser["avatar"],
            #     #     },
            #     # },
            #     # return_document=ReturnDocument.AFTER,
            # )
            response = make_response(
                {
                    "isLogin": True,
                    "result": {
                        "id": account["id"],
                        "username": account["username"],
                        "full_name": account["full_name"],
                        "avatar": account["avatar"],
                        "email": account["email"],
                        "auth_type": account["auth_type"],
                        "role": account["role"],
                        # "user_token": encoded,
                    },
                }
            )
            response.headers.set("Access-Control-Expose-Headers", "Authorization")
            response.headers.set("Authorization", encoded)

            return response

    except:
        return {"isLogin": False, "result": "Log in Facebook failed"}


def logingoogle():
    accessToken = request.headers["Authorization"]

    Headers = {"Authorization": accessToken}
    faceBookUser = requests.get(
        f"https://www.googleapis.com/oauth2/v3/userinfo", headers=Headers
    )

    formUser = faceBookUser.json()

    account = db["accounts"].find_one({"id": formUser["sub"]})

    try:
        if account == None:
            list = db["lists"].find_one(
                {
                    "id": formUser["sub"],
                },
            )

            newList = {
                "created_by": formUser["name"],
                "description": "List movie which users are added",
                "favorite_count": 0,
                "id": formUser["sub"],
                "name": "List",
                "items": [],
            }

            if list == None:
                db["lists"].insert_one(newList)

            watchlist = db["watchlists"].find_one(
                {
                    "id": formUser["sub"],
                },
            )

            newWatchList = {
                "created_by": formUser["name"],
                "description": "Videos which users watched",
                "favorite_count": 0,
                "id": formUser["sub"],
                "item_count": 0,
                "name": "WatchList",
                "items": [],
            }

            if watchlist == None:
                db["watchlists"].insert_one(newWatchList)

            db["accounts"].insert_one(
                {
                    "id": formUser["sub"],
                    "username": formUser["name"],
                    "full_name": formUser["name"],
                    "avatar": formUser["picture"],
                    "email": formUser["email"],
                    "auth_type": "google",
                    "role": "normal",
                },
            )

            get_account = db["accounts"].find_one(
                {
                    "id": formUser["sub"],
                },
            )

            encoded = jwt.encode(
                {
                    "id": get_account["id"],
                    "username": get_account["username"],
                    "full_name": get_account["full_name"],
                    "avatar": get_account["avatar"],
                    "email": get_account["email"],
                    "auth_type": get_account["auth_type"],
                    "role": "normal",
                    "exp": datetime.now(tz=timezone.utc)
                    + timedelta(seconds=configs.TIME_OFFSET),
                },
                str(os.getenv("ACCESS_TOKEN_SECRET")),
                algorithm="HS256",
            )

            response = make_response(
                {
                    "isSignUp": True,
                    "result": {
                        "id": get_account["id"],
                        "username": get_account["username"],
                        "full_name": get_account["full_name"],
                        "avatar": get_account["avatar"],
                        "email": get_account["email"],
                        "auth_type": get_account["auth_type"],
                        "role": get_account["role"],
                        # "user_token": encoded,
                    },
                }
            )
            response.headers.set("Access-Control-Expose-Headers", "Authorization")
            response.headers.set("Authorization", encoded)

            return response

        else:
            encoded = jwt.encode(
                {
                    "id": account["id"],
                    "username": account["username"],
                    "full_name": account["full_name"],
                    "avatar": account["avatar"],
                    "email": account["email"],
                    "auth_type": account["auth_type"],
                    "role": "normal",
                    "exp": datetime.now(tz=timezone.utc)
                    + timedelta(seconds=configs.TIME_OFFSET),
                },
                str(os.getenv("ACCESS_TOKEN_SECRET")),
                algorithm="HS256",
            )

            # get_account = db["accounts"].find_one_and_update(
            # get_account = db["accounts"].find_one(
            #     {"id": formUser["id"]},
            #     # {
            #     #     "$set": {
            #     #         "user_token": encoded,
            #     #         # "avatar": formUser["avatar"],
            #     #     },
            #     # },
            #     # return_document=ReturnDocument.AFTER,
            # )
            response = make_response(
                {
                    "isLogin": True,
                    "result": {
                        "id": account["id"],
                        "username": account["username"],
                        "full_name": account["full_name"],
                        "avatar": account["avatar"],
                        "email": account["email"],
                        "auth_type": account["auth_type"],
                        "role": account["role"],
                        # "user_token": encoded,
                    },
                }
            )
            response.headers.set("Access-Control-Expose-Headers", "Authorization")
            response.headers.set("Authorization", encoded)

            return response

    except:
        return {"isLogin": False, "result": "Log in Facebook failed"}


def getuser_by_token():
    # formUser = request.form
    user_token = request.headers["Authorization"].replace("Bearer ", "")

    try:
        jwtUser = jwt.decode(
            user_token,
            str(os.getenv("ACCESS_TOKEN_SECRET")),
            algorithms=["HS256"],
        )

        if jwtUser["auth_type"] == "facebook":
            facebook_account = db["accounts"].find_one(
                {"id": jwtUser["id"]},
            )
            if facebook_account == None:
                return {"isNotExist": True, "result": "Account does not exists"}
            else:
                response = make_response(
                    {
                        "isLogin": True,
                        "result": {
                            "id": facebook_account["id"],
                            "username": facebook_account["username"],
                            "full_name": facebook_account["full_name"],
                            "avatar": facebook_account["avatar"],
                            "email": facebook_account["email"],
                            "auth_type": facebook_account["auth_type"],
                            "role": facebook_account["role"],
                            # "user_token": user_token,
                        },
                    }
                )
                response.headers.set("Access-Control-Expose-Headers", "Authorization")
                response.headers.set("Authorization", user_token)

                return response
        elif jwtUser["auth_type"] == "google":
            google_account = db["accounts"].find_one(
                {"id": jwtUser["id"]},
            )
            if google_account == None:
                return {"isNotExist": True, "result": "Account does not exists"}
            else:
                response = make_response(
                    {
                        "isLogin": True,
                        "result": {
                            "id": google_account["id"],
                            "username": google_account["username"],
                            "full_name": google_account["full_name"],
                            "avatar": google_account["avatar"],
                            "email": google_account["email"],
                            "auth_type": google_account["auth_type"],
                            "role": google_account["role"],
                            # "user_token": user_token,
                        },
                    }
                )
                response.headers.set("Access-Control-Expose-Headers", "Authorization")
                response.headers.set("Authorization", user_token)

                return response
        elif jwtUser["auth_type"] == "email":
            account = db["accounts"].find_one(
                {"$and": [{"email": jwtUser["email"]}, {"auth_type": "email"}]}
            )

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
                    #             seconds=configs.TIME_OFFSET
                    #         ),
                    #     },
                    #     str(os.getenv("ACCESS_TOKEN_SECRET")),
                    #     algorithm="HS256",
                    # )

                    response = make_response(
                        {
                            "isLogin": True,
                            "result": {
                                "id": get_account["id"],
                                "username": get_account["username"],
                                "full_name": get_account["full_name"],
                                "avatar": get_account["avatar"],
                                "email": get_account["email"],
                                "auth_type": get_account["auth_type"],
                                "role": get_account["role"],
                                # "user_token": user_token,
                            },
                        }
                    )
                    response.headers.set(
                        "Access-Control-Expose-Headers", "Authorization"
                    )
                    response.headers.set("Authorization", user_token)

                    return response
                else:
                    return {"isWrongPassword": True, "result": "Wrong Password"}
            else:
                return {"isNotExist": True, "result": "Account does not exists"}

    except:
        return {"isLogin": False, "result": "Log in failed"}


# def signup():
#     formUser = request.form

#     try:
#         emailValidate = requests.get(
#             f"https://emailvalidation.abstractapi.com/v1/?api_key=e23c5b9c07dc432796eea058c9d99e82&email={formUser['email']}"
#         )
#         emailValidateResponse = emailValidate.json()

#         if emailValidateResponse["is_smtp_valid"]["value"] == True:
#             account = db["accounts"].find_one(
#                 {"$and": [{"email": formUser["email"]}, {"auth_type": "email"}]}
#             )
#             if account == None:
#                 list = db["lists"].find_one(
#                     {
#                         "id": formUser["id"],
#                     },
#                 )

#                 newList = {
#                     "full_name": formUser["full_name"],
#                     "description": "List movie which users are added",
#                     "favorite_count": 0,
#                     "id": formUser["id"],
#                     "name": "List",
#                     "items": [],
#                 }

#                 if list == None:
#                     db["lists"].insert_one(newList)

#                 watchlist = db["watchlists"].find_one(
#                     {
#                         "id": formUser["id"],
#                     },
#                 )

#                 newWatchList = {
#                     "full_name": formUser["full_name"],
#                     "description": "Videos which users watched",
#                     "favorite_count": 0,
#                     "id": formUser["id"],
#                     "item_count": 0,
#                     "name": "WatchList",
#                     "items": [],
#                 }

#                 if watchlist == None:
#                     db["watchlists"].insert_one(newWatchList)

#                     # if "role" in formUser.to_dict():
#                     #     db["accounts"].insert_one(
#                     #         formUser.to_dict()
#                     #         | {
#                     #             "auth_type": "email",
#                     #         }
#                     #     )
#                     # else:

#                 db["accounts"].insert_one(
#                     formUser.to_dict()
#                     | {
#                         "role": "normal",
#                         "auth_type": "email",
#                     },
#                 )

#                 # get_account = db["accounts"].find_one(
#                 #     {"id": formUser["id"]},
#                 # )

#                 return {
#                     "isSignUp": True,
#                     "result": "Sign up account successfully"
#                     # {
#                     # "id": get_account["id"],
#                     # "username": get_account["username"],
#                     # "full_name": get_account["full_name"],
#                     # "avatar": get_account["avatar"],
#                     # "email": get_account["email"],
#                     # "auth_type": get_account["auth_type"],
#                     # "role": get_account["role"],
#                     # },
#                 }
#             else:
#                 return {"isEmailExist": True, "result": "Email is already exists"}
#         else:
#             return {"isInValidEmail": True, "result": "Email is Invalid"}
#     except:
#         return {"isSignUp": False, "result": "Sign Up Failed"}


def signup():
    formUser = request.form
    user_token = request.headers["Authorization"].replace("Bearer ", "")

    try:
        jwtUser = jwt.decode(
            user_token,
            str(formUser["otp"]),
            algorithms=["HS256"],
        )
        account = db["accounts"].find_one(
            {"$and": [{"id": jwtUser["id"]}, {"auth_type": "email"}]}
        )
        if account == None:
            list = db["lists"].find_one(
                {
                    "id": jwtUser["id"],
                },
            )

            newList = {
                "full_name": jwtUser["full_name"],
                "description": "List movie which users are added",
                "favorite_count": 0,
                "id": jwtUser["id"],
                "name": "List",
                "items": [],
            }

            if list == None:
                db["lists"].insert_one(newList)

            watchlist = db["watchlists"].find_one(
                {
                    "id": jwtUser["id"],
                },
            )

            newWatchList = {
                "full_name": jwtUser["full_name"],
                "description": "Videos which users watched",
                "favorite_count": 0,
                "id": jwtUser["id"],
                "item_count": 0,
                "name": "WatchList",
                "items": [],
            }

            if watchlist == None:
                db["watchlists"].insert_one(newWatchList)

                # if "role" in formUser.to_dict():
                #     db["accounts"].insert_one(
                #         formUser.to_dict()
                #         | {
                #             "auth_type": "email",
                #         }
                #     )
                # else:

            db["accounts"].insert_one(
                {
                    "id": jwtUser["id"],
                    "username": jwtUser["username"],
                    "password": jwtUser["password"],
                    "full_name": jwtUser["full_name"],
                    "avatar": jwtUser["avatar"],
                    "email": jwtUser["email"],
                    "auth_type": jwtUser["auth_type"],
                    "role": jwtUser["role"],
                }
            )

            return {
                # "isSignUp": True, "result": jwtUser
                "isSignUp": True,
                "result": "Sign up account successfully",
            }
        else:
            return {"isAccountExist": True, "result": "Account is already exists"}
    except jwt.ExpiredSignatureError as e:
        return {"isOTPExpired": True, "result": "OTP is expired"}

    except jwt.exceptions.DecodeError as e:
        return {"isInvalidOTP": True, "result": "OTP is invalid"}
    except:
        return {"isSignUp": False, "result": "Sign Up Failed"}


def verify_email():
    formUser = request.form

    try:
        emailValidate = requests.get(
            f"https://emailvalidation.abstractapi.com/v1/?api_key=e23c5b9c07dc432796eea058c9d99e82&email={formUser['email']}"
        )
        emailValidateResponse = emailValidate.json()

        if emailValidateResponse["is_smtp_valid"]["value"] == True:
            account = db["accounts"].find_one(
                {"$and": [{"email": formUser["email"]}, {"auth_type": "email"}]}
            )
            if account == None:
                OTP = generateOTP(length=6)
                encoded = jwt.encode(
                    {
                        "id": formUser["id"],
                        "username": formUser["username"],
                        "password": formUser["password"],
                        "full_name": formUser["full_name"],
                        "avatar": formUser["avatar"],
                        "role": "normal",
                        "email": formUser["email"],
                        "auth_type": "email",
                        "exp": datetime.now(tz=timezone.utc) + timedelta(seconds=60),
                    },
                    str(OTP),
                    algorithm="HS256",
                )
                response = make_response(
                    {"isVerify": True, "result": "Send otp email successfully"}
                )
                response.headers.set("Access-Control-Expose-Headers", "Authorization")
                response.headers.set("Authorization", encoded)
                email_response = Email_Verification(to=formUser["email"], otp=OTP)

                # print(email_response)
                # if "message_id" in dict(email_response):
                return response
                # else:
                #     return {"isSendEmail": False, "result": "Send otp email failed"}
            else:
                return {"isEmailExist": True, "result": "Email is already exists"}
        else:
            return {"isInValidEmail": True, "result": "Email is Invalid"}
    except:
        return {"isVerify": False, "result": "Send otp email failed"}
