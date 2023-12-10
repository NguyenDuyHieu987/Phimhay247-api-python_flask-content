import pymongo
from pymongo.errors import PyMongoError
from flask import *
from pymongo import ReturnDocument
import jwt
import os
from datetime import datetime, timezone, timedelta
import time
import requests
from argon2 import exceptions
import configs
from configs.database import Database
from utils.SendinblueEmail import SendiblueEmail
from utils.OTPGeneration import generateOTP
from utils.JwtRedis import JwtRedis
from utils.EmalValidation import Validate_Email
from utils.encryptPassword import encryptPassword, verifyPassword
from utils.JsonResponse import ConvertJsonResponse as cvtJson
from utils.ErrorMessage import BadRequestMessage, InternalServerErrorMessage
from utils.exceptions import NotInTypeError
from utils.exceptions import DefaultError


class Authentication(SendiblueEmail):
    def __init__(self):
        database = Database()
        self.__db = database.ConnectMongoDB()
        self.__jwtredis = JwtRedis()

    def login(self):
        try:
            formUser = request.form
            account = self.__db["accounts"].find_one(
                {"email": formUser["email"], "auth_type": "email"}
            )
            if account != None:
                is_correct_password = verifyPassword(
                    account["password"], formUser["password"]
                )

                if is_correct_password == True:
                    encoded = jwt.encode(
                        {
                            "id": account["id"],
                            "username": account["username"],
                            "full_name": account["full_name"],
                            "avatar": account["avatar"],
                            "role": account["role"],
                            "email": account["email"],
                            "auth_type": account["auth_type"],
                            "created_at": str(account["created_at"]),
                            "exp": (
                                datetime.now(tz=timezone.utc)
                                + timedelta(seconds=configs.JWT_EXP_OFFSET * 60 * 60)
                            ).timestamp(),
                        },
                        str(os.getenv("JWT_SIGNATURE_SECRET")),
                        algorithm="HS256",
                    )

                    response = make_response(
                        {
                            "isLogin": True,
                            "exp_token_hours": int(os.getenv("JWT_EXP_OFFSET")),
                            "result": {
                                "id": account["id"],
                                "username": account["username"],
                                "full_name": account["full_name"],
                                "avatar": account["avatar"],
                                "email": account["email"],
                                "auth_type": account["auth_type"],
                                "role": account["role"],
                                "created_at": account["created_at"],
                            },
                        }
                    )

                    response.headers.set(
                        "Access-Control-Expose-Headers", "Authorization"
                    )

                    response.set_cookie(
                        key="user_token",
                        value=encoded,
                        max_age=configs.JWT_EXP_OFFSET * 60 * 60,
                        samesite="lax",
                        secure=True,
                        httponly=False,
                    )

                    response.headers.set("Authorization", encoded)

                    return response
                else:
                    return {"isWrongPassword": True, "result": "Wrong Password"}
            else:
                return {"isNotExist": True, "result": "Account does not exists"}
        except (exceptions.InvalidHashError, exceptions.VerifyMismatchError) as e:
            return {"isWrongPassword": True, "result": "Wrong Password"}
        except PyMongoError as e:
            InternalServerErrorMessage(e._message)
        except Exception as e:
            InternalServerErrorMessage(e)

    def loginfacebook(self):
        try:
            accessToken = request.headers["Authorization"].replace("Bearer ", "")

            faceBookUser = requests.get(
                f"https://graph.facebook.com/v15.0/me?access_token={accessToken}&fields=id,name,email,picture"
            )

            formUser = faceBookUser.json()

            account = self.__db["accounts"].find_one({"id": formUser["id"]})

            if account == None:
                self.__db["accounts"].insert_one(
                    {
                        "id": formUser["id"],
                        "username": formUser["name"],
                        "full_name": formUser["name"],
                        "avatar": formUser["picture"]["data"]["url"],
                        "email": formUser["email"],
                        "auth_type": "facebook",
                        "role": "normal",
                        "created_at": str(datetime.now()),
                        "updated_at": str(datetime.now()),
                    },
                )

                get_account = self.__db["accounts"].find_one(
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
                        "auth_type": get_account["auth_type"],
                        "role": "normal",
                        "created_at": str(get_account["created_at"]),
                        "exp": (
                            datetime.now(tz=timezone.utc)
                            + timedelta(seconds=configs.JWT_EXP_OFFSET * 60 * 60)
                        ).timestamp(),
                    },
                    str(os.getenv("JWT_SIGNATURE_SECRET")),
                    algorithm="HS256",
                )

                response = make_response(
                    {
                        "isSignUp": True,
                        "exp_token_hours": int(os.getenv("JWT_EXP_OFFSET")),
                        "result": {
                            "id": get_account["id"],
                            "username": get_account["username"],
                            "full_name": get_account["full_name"],
                            "avatar": get_account["avatar"],
                            "email": get_account["email"],
                            "auth_type": get_account["auth_type"],
                            "role": get_account["role"],
                            "created_at": get_account["created_at"],
                        },
                    }
                )

                response.headers.set("Access-Control-Expose-Headers", "Authorization")

                response.set_cookie(
                    key="user_token",
                    value=encoded,
                    max_age=configs.JWT_EXP_OFFSET * 60 * 60,
                    samesite="lax",
                    secure=True,
                    httponly=False,
                )

                response.headers.set("Authorization", encoded)

                return response

            else:
                account_modified = self.__db["accounts"].find_one_and_update(
                    {"id": formUser["id"]},
                    {
                        "$set": {
                            "avatar": formUser["picture"]["data"]["url"],
                        }
                    },
                    return_document=ReturnDocument.AFTER,
                )

                encoded = jwt.encode(
                    {
                        "id": account_modified["id"],
                        "username": account_modified["username"],
                        "full_name": account_modified["full_name"],
                        "avatar": account_modified["avatar"],
                        "email": account_modified["email"],
                        "auth_type": account_modified["auth_type"],
                        "role": "normal",
                        "created_at": str(account_modified["created_at"]),
                        "exp": (
                            datetime.now(tz=timezone.utc)
                            + timedelta(seconds=configs.JWT_EXP_OFFSET * 60 * 60)
                        ).timestamp(),
                    },
                    str(os.getenv("JWT_SIGNATURE_SECRET")),
                    algorithm="HS256",
                )

                # get_account = self.__db["accounts"].find_one_and_update(
                # get_account = self.__db["accounts"].find_one(
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
                        "exp_token_hours": int(os.getenv("JWT_EXP_OFFSET")),
                        "result": {
                            "id": account["id"],
                            "username": account["username"],
                            "full_name": account["full_name"],
                            "avatar": account["avatar"],
                            "email": account["email"],
                            "auth_type": account["auth_type"],
                            "role": account["role"],
                            "created_at": account["created_at"],
                        },
                    }
                )

                response.headers.set("Access-Control-Expose-Headers", "Authorization")

                response.set_cookie(
                    key="user_token",
                    value=encoded,
                    max_age=configs.JWT_EXP_OFFSET * 60 * 60,
                    samesite="lax",
                    secure=True,
                    httponly=False,
                )

                response.headers.set("Authorization", encoded)

                return response

        except PyMongoError as e:
            InternalServerErrorMessage(e._message)
        except Exception as e:
            InternalServerErrorMessage(e)

    def logingoogle(self):
        try:
            accessToken = request.headers["Authorization"]

            Headers = {"Authorization": accessToken}
            googleUser = requests.get(
                f"https://www.googleapis.com/oauth2/v3/userinfo", headers=Headers
            )

            formUser = googleUser.json()

            account = self.__db["accounts"].find_one({"id": formUser["sub"]})

            if account == None:
                self.__db["accounts"].insert_one(
                    {
                        "id": formUser["sub"],
                        "username": formUser["name"],
                        "full_name": formUser["name"],
                        "avatar": formUser["picture"],
                        "email": formUser["email"],
                        "auth_type": "google",
                        "role": "normal",
                        "created_at": str(datetime.now()),
                        "updated_at": str(datetime.now()),
                    },
                )

                get_account = self.__db["accounts"].find_one(
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
                        "created_at": str(get_account["created_at"]),
                        "exp": (
                            datetime.now(tz=timezone.utc)
                            + timedelta(seconds=configs.JWT_EXP_OFFSET * 60 * 60)
                        ).timestamp(),
                    },
                    str(os.getenv("JWT_SIGNATURE_SECRET")),
                    algorithm="HS256",
                )

                response = make_response(
                    {
                        "isSignUp": True,
                        "exp_token_hours": int(os.getenv("JWT_EXP_OFFSET")),
                        "result": {
                            "id": get_account["id"],
                            "username": get_account["username"],
                            "full_name": get_account["full_name"],
                            "avatar": get_account["avatar"],
                            "email": get_account["email"],
                            "auth_type": get_account["auth_type"],
                            "role": get_account["role"],
                            "created_at": get_account["created_at"],
                        },
                    }
                )

                response.headers.set("Access-Control-Expose-Headers", "Authorization")

                response.set_cookie(
                    key="user_token",
                    value=encoded,
                    max_age=configs.JWT_EXP_OFFSET * 60 * 60,
                    samesite="lax",
                    secure=True,
                    httponly=False,
                )

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
                        "created_at": str(account["created_at"]),
                        "exp": (
                            datetime.now(tz=timezone.utc)
                            + timedelta(seconds=configs.JWT_EXP_OFFSET * 60 * 60)
                        ).timestamp(),
                    },
                    str(os.getenv("JWT_SIGNATURE_SECRET")),
                    algorithm="HS256",
                )

                # get_account = self.__db["accounts"].find_one_and_update(
                # get_account = self.__db["accounts"].find_one(
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
                        "exp_token_hours": int(os.getenv("JWT_EXP_OFFSET")),
                        "result": {
                            "id": account["id"],
                            "username": account["username"],
                            "full_name": account["full_name"],
                            "avatar": account["avatar"],
                            "email": account["email"],
                            "auth_type": account["auth_type"],
                            "role": account["role"],
                            "created_at": account["created_at"],
                        },
                    }
                )
                response.headers.set("Access-Control-Expose-Headers", "Authorization")

                response.set_cookie(
                    key="user_token",
                    value=encoded,
                    max_age=configs.JWT_EXP_OFFSET * 60 * 60,
                    samesite="lax",
                    secure=True,
                    httponly=False,
                )

                response.headers.set("Authorization", encoded)

                return response

        except PyMongoError as e:
            InternalServerErrorMessage(e._message)
        except Exception as e:
            InternalServerErrorMessage(e)

    def getuser_by_token(self):
        try:
            user_token = request.headers["Authorization"].replace(
                "Bearer ", ""
            ) or request.cookies.get("user_token")

            if user_token == None:
                return

            jwtUser = jwt.decode(
                user_token,
                str(os.getenv("JWT_SIGNATURE_SECRET")),
                algorithms=["HS256"],
            )

            is_alive = self.__jwtredis.set_prefix("user_logout").verify(jwtUser)

            if is_alive:
                response = make_response(
                    {
                        "isLogin": True,
                        "result": {
                            "id": jwtUser["id"],
                            "username": jwtUser["username"],
                            "full_name": jwtUser["full_name"],
                            "avatar": jwtUser["avatar"],
                            "email": jwtUser["email"],
                            "auth_type": jwtUser["auth_type"],
                            "role": jwtUser["role"],
                            "created_at": jwtUser["created_at"],
                        },
                    }
                )

                response.headers.set("Access-Control-Expose-Headers", "Authorization")

                response.headers.set("Authorization", user_token)

                return response
            else:
                return {"isLogin": False, "result": "Token is no longer active"}

        except jwt.ExpiredSignatureError as e:
            response = make_response(
                {"isTokenExpired": True, "result": "Token is expired"}
            )

            response.delete_cookie(
                "user_token", samesite="lax", secure=True, httponly=False
            )

            return response
        except (jwt.exceptions.DecodeError, jwt.exceptions.InvalidSignatureError) as e:
            response = make_response(
                {"isInvalidToken": True, "result": "Token is invalid"}
            )

            response.delete_cookie(
                "user_token", samesite="lax", secure=True, httponly=False
            )

            return response
        except PyMongoError as e:
            InternalServerErrorMessage(e._message)
        except Exception as e:
            InternalServerErrorMessage(e)

    def signup(self):
        try:
            formUser = request.form
            # signup_token = request.headers["Authorization"].replace("Bearer ", "")
            signup_token = (
                request.cookies.get("vrf_signup_token") or formUser["vrf_signup_token"]
            )

            jwtUser = jwt.decode(
                signup_token,
                str(formUser["otp"]),
                algorithms=["HS256"],
            )

            is_alive = self.__jwtredis.set_prefix("verify_signup").verify(signup_token)

            if is_alive == False:
                return {"success": False, "result": "Token is no longer active"}

            account = self.__db["accounts"].find_one(
                {"id": jwtUser["id"], "auth_type": "email"}
            )

            if account == None:
                # if "role" in formUser.to_dict():
                #     self.__db["accounts"].insert_one(
                #         formUser.to_dict()
                #         | {
                #             "auth_type": "email",
                #         }
                #     )
                # else:

                self.__db["accounts"].insert_one(
                    {
                        "id": jwtUser["id"],
                        "username": jwtUser["username"],
                        "password": jwtUser["password"],
                        "full_name": jwtUser["full_name"],
                        "avatar": jwtUser["avatar"],
                        "email": jwtUser["email"],
                        "auth_type": jwtUser["auth_type"],
                        "role": jwtUser["role"],
                        "created_at": str(datetime.now()),
                        "updated_at": str(datetime.now()),
                    }
                )

                self.__jwtredis.set_prefix("verify_signup")

                self.__jwtredis.sign(
                    signup_token,
                    option={"exp": configs.OTP_EXP_OFFSET * 60},
                )

                return {
                    "isSignUp": True,
                    "result": "Sign up account successfully",
                }
            else:
                return {"isAccountExist": True, "result": "Account is already exists"}
        except jwt.ExpiredSignatureError as e:
            return {"isOTPExpired": True, "result": "OTP is expired"}
        except (jwt.exceptions.DecodeError, jwt.exceptions.InvalidSignatureError) as e:
            return {"isInvalidOTP": True, "result": "OTP is invalid"}
        except PyMongoError as e:
            InternalServerErrorMessage(e._message)
        except Exception as e:
            InternalServerErrorMessage(e)

    def signup_verify(self, type):
        try:
            formUser = request.form

            if type == "email":
                account = self.__db["accounts"].find_one(
                    {"email": formUser["email"], "auth_type": "email"}
                )

                if account == None:
                    if Validate_Email(formUser["email"]):
                        # if True:
                        OTP = generateOTP(length=6)

                        password_encrypted = encryptPassword(formUser["password"])

                        encoded = jwt.encode(
                            {
                                "id": formUser["id"],
                                "username": formUser["username"],
                                "password": password_encrypted,
                                "full_name": formUser["full_name"],
                                "avatar": formUser["avatar"],
                                "role": "normal",
                                "email": formUser["email"],
                                "auth_type": "email",
                                "description": "Register new account",
                                "exp": (
                                    datetime.now(tz=timezone.utc)
                                    + timedelta(seconds=configs.OTP_EXP_OFFSET * 60)
                                ).timestamp(),
                            },
                            str(OTP),
                            algorithm="HS256",
                        )

                        response = make_response(
                            {
                                "isSended": True,
                                "exp_offset": configs.OTP_EXP_OFFSET * 60,
                                "result": "Send otp email successfully",
                            }
                        )

                        # response.headers.set(
                        #     "Access-Control-Expose-Headers", "Authorization"
                        # )

                        # response.headers.set("Authorization", encoded)

                        response.set_cookie(
                            key="vrf_signup_token",
                            value=encoded,
                            max_age=configs.OTP_EXP_OFFSET * 60,
                            samesite="lax",
                            secure=True,
                            httponly=False,
                        )

                        email_response = self.Verification_OTP(
                            to=formUser["email"],
                            otp=OTP,
                            title="Xác nhận đăng ký tài khoản",
                            noteExp=os.getenv("OTP_EXP_OFFSET"),
                        )

                        # print(email_response)
                        # if "message_id" in dict(email_response):
                        return response
                        # else:
                        #     return {"isSended": False, "result": "Send otp email failed"}

                    else:
                        return {"isInValidEmail": True, "result": "Email is Invalid"}
                else:
                    return {"isEmailExist": True, "result": "Email is already exists"}
            else:
                raise NotInTypeError("verify sign up", type)
        except NotInTypeError as e:
            BadRequestMessage(e.message)
        except PyMongoError as e:
            InternalServerErrorMessage(e._message)
        except Exception as e:
            InternalServerErrorMessage(e)

    def forgot_password(self, type):
        try:
            formUser = request.form

            if type == "email":
                account = self.__db["accounts"].find_one(
                    {
                        "email": formUser["email"],
                        "auth_type": "email",
                    }
                )

                if account != None:
                    # if Validate_Email(formUser["email"]):
                    if True:
                        encoded = jwt.encode(
                            {
                                "id": account["id"],
                                "email": account["email"],
                                "auth_type": "email",
                                "description": "Reset your password",
                                "exp": (
                                    datetime.now(tz=timezone.utc)
                                    + timedelta(
                                        seconds=configs.FORGOT_PASSWORD_EXP_OFFSET * 60
                                    )
                                ).timestamp(),
                            },
                            str(os.getenv("JWT_SIGNATURE_SECRET")),
                            algorithm="HS256",
                        )

                        reset_password_link = (
                            f"{os.getenv('CLIENT_URL')}/ResetPassword?token={encoded}"
                        )

                        print(reset_password_link)

                        email_response = self.Verification_Link(
                            to=formUser["email"],
                            title="Đặt lại mật khẩu của bạn",
                            subject="Hoàn thành yêu cầu đặt lại mật khẩu",
                            nameLink="Đặt lại mật khẩu",
                            linkVerify=reset_password_link,
                            note1="Truy cập dường liên kết sau đây để đặt lại mật khẩu của bạn:",
                            noteExp=int(os.getenv("FORGOT_PASSWORD_EXP_OFFSET")),
                        )

                        return {
                            "isSended": True,
                            "exp_offset": configs.FORGOT_PASSWORD_EXP_OFFSET,
                            "result": "Send email successfully",
                        }

                    else:
                        return {
                            "isInValidEmail": True,
                            "result": "Email is Invalid",
                        }

                else:
                    return {"isEmailExist": False, "result": "Email is not registered"}

            else:
                raise DefaultError(
                    f"Forgot password with method: {type} is not support!"
                )

        except NotInTypeError as e:
            BadRequestMessage(e.message)
        except PyMongoError as e:
            InternalServerErrorMessage(e._message)
        except DefaultError as e:
            BadRequestMessage(e.message)
        except Exception as e:
            InternalServerErrorMessage(e)

    def logout(self):
        try:
            user_token = request.headers["Authorization"].replace(
                "Bearer ", ""
            ) or request.cookies.get("user_token")

            jwtUser = jwt.decode(
                user_token,
                str(os.getenv("JWT_SIGNATURE_SECRET")),
                algorithms=["HS256"],
            )

            self.__jwtredis.set_prefix("user_logout")

            self.__jwtredis.sign(
                user_token,
                option={"exp": configs.JWT_EXP_OFFSET * 60 * 60},
            )

            response = make_response(
                {"isLogout": True, "result": "Log out successfully"}
            )

            response.delete_cookie(
                "user_token", samesite="lax", secure=True, httponly=False
            )

            return response

        except (
            jwt.exceptions.ExpiredSignatureError,
            jwt.exceptions.DecodeError,
            jwt.exceptions.InvalidSignatureError,
        ) as e:
            response = make_response({"isLogout": False, "result": "Log out failed"})

            response.delete_cookie(
                "user_token", samesite="lax", secure=True, httponly=False
            )

            return response
        # except jwt.exceptions.ExpiredSignatureError as e:
        #     response.delete_cookie(
        #         "user_token", samesite="lax", secure=True, httponly=False
        #     )
        #     InternalServerErrorMessage("Token is expired")
        # except (jwt.exceptions.DecodeError, jwt.exceptions.InvalidSignatureError) as e:
        #     response.delete_cookie(
        #         "user_token", samesite="lax", secure=True, httponly=False
        #     )
        #     InternalServerErrorMessage("Token is invalid")
        except PyMongoError as e:
            InternalServerErrorMessage(e._message)
        except Exception as e:
            InternalServerErrorMessage(e)
