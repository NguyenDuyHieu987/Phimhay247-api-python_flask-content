import pymongo
from pymongo.errors import PyMongoError
from pymongo import ReturnDocument
from utils.JsonResponse import ConvertJsonResponse as cvtJson
from utils.ErrorMessage import BadRequestMessage, InternalServerErrorMessage
from flask import *
import jwt
import os
from argon2 import exceptions
from datetime import datetime, timezone, timedelta
import configs
from utils.SendinblueEmail import SendiblueEmail
from utils.JwtRedis import JwtRedis
from utils.OTPGeneration import generateOTP
from configs.database import Database
from utils.exceptions import NotInTypeError
from utils.exceptions import DefaultError
from utils.encryptPassword import encryptPassword, verifyPassword
from utils.EmalValidation import Validate_Email


class Account(Database, SendiblueEmail):
    def __init__(self):
        self.__db = self.ConnectMongoDB()
        self.__jwtredis = JwtRedis()

    def account_confirm(self, type):
        try:
            formUser = request.form

            user_token = request.headers["Authorization"].replace(
                "Bearer ", ""
            ) or request.cookies.get("user_token")

            jwtUser = jwt.decode(
                user_token,
                str(os.getenv("JWT_SIGNATURE_SECRET")),
                algorithms=["HS256"],
            )

            is_alive = self.__jwtredis.set_prefix("user_logout").verify(user_token)

            if is_alive == False:
                return {"isTokenAlive": False, "result": "Token is no longer active"}

            OTP = generateOTP(length=6)

            print(OTP)

            if type == "email":
                encoded = jwt.encode(
                    {
                        "id": jwtUser["id"],
                        "email": jwtUser["email"],
                        "auth_type": "email",
                        "description": "Verify your Email",
                        "exp": (
                            datetime.now(tz=timezone.utc)
                            + timedelta(seconds=configs.OTP_EXP_OFFSET * 60)
                        ).timestamp(),
                    },
                    str(OTP),
                    algorithm="HS256",
                )

                email_response = self.Verification_OTP(
                    to=jwtUser["email"],
                    otp=OTP,
                    title="Xác nhận Email của bạn",
                    noteExp=os.getenv("OTP_EXP_OFFSET"),
                )

                response = make_response(
                    {
                        "isSended": True,
                        "exp_offset": configs.OTP_EXP_OFFSET * 60,
                        "result": "Send otp email successfully",
                    }
                )

                response.set_cookie(
                    key="vrf_email_token",
                    value=encoded,
                    max_age=configs.OTP_EXP_OFFSET * 60,
                    samesite="lax",
                    secure=True,
                    httponly=False,
                )

            elif type == "change-password":
                account = self.__db["accounts"].find_one(
                    {
                        "email": jwtUser["email"],
                        "auth_type": "email",
                    }
                )

                if account != None:
                    is_correct_password = verifyPassword(
                        account["password"], formUser["old_password"]
                    )

                    if is_correct_password == True:
                        new_password_encrypted = encryptPassword(
                            formUser["new_password"]
                        )

                        encoded = jwt.encode(
                            {
                                "id": jwtUser["id"],
                                "email": jwtUser["email"],
                                "auth_type": "email",
                                "new_password": new_password_encrypted,
                                "logout_all_device": formUser["logout_all_device"],
                                "description": "Change your password",
                                "exp": (
                                    datetime.now(tz=timezone.utc)
                                    + timedelta(seconds=configs.OTP_EXP_OFFSET * 60)
                                ).timestamp(),
                            },
                            str(OTP),
                            algorithm="HS256",
                        )

                        email_response = self.Verification_OTP(
                            to=jwtUser["email"],
                            otp=OTP,
                            title="Xác nhận thay đổi mật khẩu của bạn",
                            noteExp=os.getenv("OTP_EXP_OFFSET"),
                        )

                        response = make_response(
                            {
                                "isSended": True,
                                "exp_offset": configs.OTP_EXP_OFFSET * 60,
                                "result": "Send otp email successfully",
                            }
                        )

                        response.set_cookie(
                            key="chg_pwd_token",
                            value=encoded,
                            max_age=configs.OTP_EXP_OFFSET * 60,
                            samesite="lax",
                            secure=True,
                            httponly=False,
                        )

                    else:
                        return {"isWrongPassword": True, "result": "Wrong password"}
                else:
                    raise DefaultError("Account is not found")

            elif type == "change-email":
                account1 = self.__db["accounts"].find_one(
                    {
                        "email": formUser["new_email"],
                        "auth_type": "email",
                    }
                )

                if account1 == None:
                    # if SendiblueEmail(formUser.email):
                    if True:
                        encoded = jwt.encode(
                            {
                                "id": jwtUser["id"],
                                "email": jwtUser["email"],
                                "auth_type": "email",
                                "new_email": formUser["new_email"],
                                "description": "Change your email",
                                "exp": (
                                    datetime.now(tz=timezone.utc)
                                    + timedelta(
                                        seconds=configs.CHANGE_EMAIL_EXP_OFFSET * 60
                                    )
                                ).timestamp(),
                            },
                            str(os.getenv("JWT_SIGNATURE_SECRET")),
                            algorithm="HS256",
                        )

                        change_email_link = (
                            f"{os.getenv('CLIENT_URL')}/ChangeEmail?token={encoded}"
                        )

                        print(change_email_link)

                        emailResponse = self.Verification_Link(
                            to=formUser["new_email"],
                            title="Thay đổi email của bạn",
                            subject="Hoàn thành yêu cầu đặt thay đổi email",
                            nameLink="Thay đổi email",
                            linkVerify=change_email_link,
                            note1="Truy cập dường liên kết sau đây để thay đổi email của bạn:",
                            noteExp=configs.CHANGE_EMAIL_EXP_OFFSET,
                        )

                        response = make_response(
                            {
                                "isSended": True,
                                "exp_offset": configs.CHANGE_EMAIL_EXP_OFFSET * 60,
                                "result": "Send email successfully",
                            }
                        )

                        response.set_cookie(
                            key="chg_email_token",
                            value=encoded,
                            max_age=configs.CHANGE_EMAIL_EXP_OFFSET * 60,
                            samesite="lax",
                            secure=True,
                            httponly=False,
                        )

                        return response
                    else:
                        return {
                            "isInValidEmail": True,
                            "result": "Email is Invalid",
                        }

                else:
                    return {
                        "isEmailExist": True,
                        "result": "Email is already exists",
                    }

            else:
                raise NotInTypeError("account service", type)

            response.headers.set("Access-Control-Expose-Headers", "Authorization")

            response.headers.set("Authorization", encoded)

            if len(encoded) == 0:
                return {"isSended": False, "result": "Send otp email failed"}
            else:
                return response

        except (exceptions.InvalidHashError, exceptions.VerifyMismatchError) as e:
            return {"isWrongPassword": True, "result": "Wrong password"}
        except jwt.ExpiredSignatureError as e:
            response.delete_cookie(
                "user_token", samesite="lax", secure=True, httponly=False
            )
            InternalServerErrorMessage("Token is expired")
        except (jwt.exceptions.DecodeError, jwt.exceptions.InvalidSignatureError) as e:
            response.delete_cookie(
                "user_token", samesite="lax", secure=True, httponly=False
            )
            InternalServerErrorMessage("Token is invalid")
        except NotInTypeError as e:
            BadRequestMessage(e.message)
        except PyMongoError as e:
            InternalServerErrorMessage(e._message)
        except DefaultError as e:
            BadRequestMessage(e.message)
        except Exception as e:
            InternalServerErrorMessage(e)

    def change_password(self):
        try:
            formUser = request.form

            user_token = request.headers["Authorization"].replace(
                "Bearer ", ""
            ) or request.cookies.get("user_token")

            jwtUser = jwt.decode(
                user_token,
                str(os.getenv("JWT_SIGNATURE_SECRET")),
                algorithms=["HS256"],
            )

            verify_token = request.cookies.get("chg_pwd_token") or formUser["token"]

            try:
                decodeChangePassword = jwt.decode(
                    verify_token,
                    str(formUser["otp"]),
                    algorithms=["HS256"],
                )
            except jwt.ExpiredSignatureError as e:
                return {"isOTPExpired": True, "result": "OTP is expired"}
            except (
                jwt.exceptions.DecodeError,
                jwt.exceptions.InvalidSignatureError,
            ) as e:
                return {"isInvalidOTP": True, "result": "OTP is invalid"}

            is_alive = self.__jwtredis.set_prefix("chg_pwd_token").verify(verify_token)

            if is_alive == False:
                return {"success": False, "result": "Token is no longer active"}

            result = self.__db["accounts"].update_one(
                {
                    "id": jwtUser["id"],
                    "email": jwtUser["email"],
                    "auth_type": "email",
                },
                {
                    "$set": {
                        "password": decodeChangePassword["new_password"],
                    }
                },
            )

            if result.modified_count == 1:
                log_out_all_device = decodeChangePassword["logout_all_device"] == "true"

                response = make_response(
                    {
                        "success": True,
                        "logout_all_device": log_out_all_device,
                        "result": "Change password successfully",
                    }
                )

                response.delete_cookie(
                    "chg_pwd_token",
                    samesite="lax",
                    secure=True,
                    httponly=False,
                )

                if log_out_all_device == True:
                    self.__jwtredis.set_prefix("user_logout")

                    self.__jwtredis.sign(
                        user_token,
                        option={"exp": configs.JWT_EXP_OFFSET * 60 * 60},
                    )

                    self.__jwtredis.set_prefix("chg_pwd_token")

                    self.__jwtredis.sign(
                        verify_token,
                        option={"exp": configs.OTP_EXP_OFFSET * 60},
                    )

                    encoded = jwt.encode(
                        {
                            "id": jwtUser["id"],
                            "username": jwtUser["username"],
                            "full_name": jwtUser["full_name"],
                            "avatar": jwtUser["avatar"],
                            "role": jwtUser["role"],
                            "email": jwtUser["email"],
                            "auth_type": jwtUser["auth_type"],
                            "created_at": str(jwtUser["created_at"]),
                            "exp": (
                                datetime.now(tz=timezone.utc)
                                + timedelta(seconds=configs.JWT_EXP_OFFSET * 60 * 60)
                            ).timestamp(),
                        },
                        str(os.getenv("JWT_SIGNATURE_SECRET")),
                        algorithm="HS256",
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
                return {"success": False, "result": "Change password failed"}

        except jwt.ExpiredSignatureError as e:
            response.delete_cookie(
                "user_token", samesite="lax", secure=True, httponly=False
            )
            InternalServerErrorMessage("Token is expired")
        except (jwt.exceptions.DecodeError, jwt.exceptions.InvalidSignatureError) as e:
            response.delete_cookie(
                "user_token", samesite="lax", secure=True, httponly=False
            )
            InternalServerErrorMessage("Token is invalid")
        except PyMongoError as e:
            InternalServerErrorMessage(e._message)
        except Exception as e:
            InternalServerErrorMessage(e)

    def verify_email(self):
        try:
            formUser = request.form

            user_token = request.headers["Authorization"].replace(
                "Bearer ", ""
            ) or request.cookies.get("user_token")

            verify_token = request.cookies.get("vrf_email_token") or formUser["token"]

            formUser = request.form

            try:
                decoded = jwt.decode(
                    verify_token,
                    str(formUser["otp"]),
                    algorithms=["HS256"],
                )

                response = make_response({"success": True})

                response.delete_cookie(
                    "vrf_email_token", samesite="lax", secure=True, httponly=False
                )

                return response

            except jwt.ExpiredSignatureError as e:
                return {"isOTPExpired": True, "result": "OTP is expired"}
            except (
                jwt.exceptions.DecodeError,
                jwt.exceptions.InvalidSignatureError,
            ) as e:
                return {"isInvalidOTP": True, "result": "OTP is invalid"}

        except jwt.ExpiredSignatureError as e:
            InternalServerErrorMessage("Token is expired")
        except (jwt.exceptions.DecodeError, jwt.exceptions.InvalidSignatureError) as e:
            InternalServerErrorMessage("Token is invalid")
        except PyMongoError as e:
            InternalServerErrorMessage(e._message)
        except Exception as e:
            InternalServerErrorMessage(e)

    def change_email_retrieve_token(self):
        try:
            token = request.args.get("token", type=str) or request.cookies.get(
                "chg_email_token"
            )

            if token == None:
                return {"isInvalidToken": True, "result": "Token is invalid"}

            is_alive = self.__jwtredis.set_prefix("chg_email_token").verify(token)

            if is_alive == False:
                return {
                    "success": False,
                    "result": "Token is no longer active",
                }

            change_email_info = jwt.decode(
                token,
                str(os.getenv("JWT_SIGNATURE_SECRET")),
                algorithms=["HS256"],
            )

            account = self.__db["accounts"].find_one(
                {
                    "id": change_email_info["id"],
                    "email": change_email_info["email"],
                    "auth_type": change_email_info["auth_type"],
                }
            )

            if account != None:
                return {
                    "success": True,
                    "result": {
                        "old_email": change_email_info["email"],
                        "new_email": change_email_info["new_email"],
                    },
                }
            else:
                return {
                    "success": False,
                    "result": "Cant not find information",
                }

        except jwt.ExpiredSignatureError as e:
            return {"isTokenExpired": True, "result": "Token is expired"}
        except (jwt.exceptions.DecodeError, jwt.exceptions.InvalidSignatureError) as e:
            return {"isInvalidToken": True, "result": "Token is invalid"}
        except PyMongoError as e:
            InternalServerErrorMessage(e._message)
        except Exception as e:
            InternalServerErrorMessage(e)

    def change_email(self):
        try:
            token = request.cookies.get("chg_email_token") or request.form["token"]

            if token == None:
                return {"isInvalidToken": True, "result": "Token is invalid"}

            is_alive = self.__jwtredis.set_prefix("chg_email_token").verify(token)

            if is_alive == False:
                return {
                    "success": False,
                    "result": "Token is no longer active",
                }

            change_email_info = jwt.decode(
                token,
                str(os.getenv("JWT_SIGNATURE_SECRET")),
                algorithms=["HS256"],
            )

            account = self.__db["accounts"].find_one_and_update(
                {
                    "id": change_email_info["id"],
                    "email": change_email_info["email"],
                    "auth_type": change_email_info["auth_type"],
                },
                {
                    "$set": {
                        "email": change_email_info["new_email"],
                    },
                },
                return_document=ReturnDocument.AFTER,
            )

            if account != None:
                self.__jwtredis.set_prefix("chg_email_token")

                self.__jwtredis.sign(
                    token,
                    option={"exp": configs.CHANGE_EMAIL_EXP_OFFSET * 60},
                )

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
                        "success": True,
                        "result": "Change email successfully",
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

                response.delete_cookie(
                    "chg_email_token", samesite="lax", secure=True, httponly=False
                )

                response.headers.set("Authorization", encoded)

                return response
            else:
                return {
                    "success": False,
                    "result": "Cant not find information",
                }

        except jwt.ExpiredSignatureError as e:
            return {"isTokenExpired": True, "result": "Token is expired"}
        except (jwt.exceptions.DecodeError, jwt.exceptions.InvalidSignatureError) as e:
            return {"isInvalidToken": True, "result": "Token is invalid"}
        except DefaultError as e:
            BadRequestMessage(e.message)
        except PyMongoError as e:
            InternalServerErrorMessage(e._message)
        except Exception as e:
            InternalServerErrorMessage(e)

    def reset_password_retrieve_token(self):
        try:
            token = request.args.get("token", type=str) or request.cookies.get(
                "rst_pwd_token"
            )

            if token == None:
                return {"isInvalidToken": True, "result": "Token is invalid"}

            is_alive = self.__jwtredis.set_prefix("rst_pwd_token").verify(token)

            if is_alive == False:
                return {
                    "success": False,
                    "result": "Token is no longer active",
                }

            reset_password_info = jwt.decode(
                token,
                str(os.getenv("JWT_SIGNATURE_SECRET")),
                algorithms=["HS256"],
            )

            account = self.__db["accounts"].find_one(
                {
                    "id": reset_password_info["id"],
                    "email": reset_password_info["email"],
                    "auth_type": reset_password_info["auth_type"],
                }
            )

            if account != None:
                return {
                    "success": True,
                    "result": {
                        "username": account["username"],
                        "email": reset_password_info["email"],
                        "auth_type": reset_password_info["auth_type"],
                        "created_at": account["created_at"],
                    },
                }
            else:
                return {
                    "success": False,
                    "result": "Cant not find information",
                }

        except jwt.ExpiredSignatureError as e:
            return {"isTokenExpired": True, "result": "Token is expired"}
        except (jwt.exceptions.DecodeError, jwt.exceptions.InvalidSignatureError) as e:
            return {"isInvalidToken": True, "result": "Token is invalid"}
        except PyMongoError as e:
            InternalServerErrorMessage(e._message)
        except Exception as e:
            InternalServerErrorMessage(e)

    def reset_password(self):
        try:
            token = request.cookies.get("rst_pwd_token") or request.form["token"]

            if token == None:
                return {"isInvalidToken": True, "result": "Token is invalid"}

            is_alive = self.__jwtredis.set_prefix("rst_pwd_token").verify(token)

            if is_alive == False:
                return {
                    "success": False,
                    "result": "Token is no longer active",
                }

            reset_password_info = jwt.decode(
                token,
                str(os.getenv("JWT_SIGNATURE_SECRET")),
                algorithms=["HS256"],
            )

            account = self.__db["accounts"].find_one_and_update(
                {
                    "id": reset_password_info["id"],
                    "email": reset_password_info["email"],
                    "auth_type": reset_password_info["auth_type"],
                },
                {
                    "$set": {
                        "password": new_password_encrypted,
                    },
                },
                return_document=ReturnDocument.AFTER,
            )

            if account != None:
                self.__jwtredis.set_prefix("rst_pwd_token")

                self.__jwtredis.sign(
                    token,
                    option={"exp": configs.FORGOT_PASSWORD_EXP_OFFSET * 60},
                )

                response = make_response(
                    {
                        "success": True,
                        "result": "Reset password successfully",
                    }
                )

                response.delete_cookie(
                    "rst_pwd_token", samesite="lax", secure=True, httponly=False
                )

                return response
            else:
                return {
                    "success": False,
                    "result": "Cant not find information",
                }

        except jwt.ExpiredSignatureError as e:
            return {"isTokenExpired": True, "result": "Token is expired"}
        except (jwt.exceptions.DecodeError, jwt.exceptions.InvalidSignatureError) as e:
            return {"isInvalidToken": True, "result": "Token is invalid"}
        except DefaultError as e:
            BadRequestMessage(e.message)
        except PyMongoError as e:
            InternalServerErrorMessage(e._message)
        except Exception as e:
            InternalServerErrorMessage(e)
