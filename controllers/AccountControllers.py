import pymongo
from pymongo.errors import PyMongoError
from utils.JsonResponse import ConvertJsonResponse as cvtJson
from utils.ErrorMessage import BadRequestMessage, InternalServerErrorMessage
from flask import *
import jwt
import os
from datetime import datetime, timezone, timedelta
import configs
from utils.SendinblueEmail import SendiblueEmail
from utils.JwtRedis import JwtRedis
from utils.OTPGeneration import generateOTP
from configs.database import Database
from utils.exceptions import NotInTypeError
from utils.exceptions import DefaultError
from utils.encryptPassword import encryptPassword, verifyPassword


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
                    key="verify_your_email",
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
                            key="verify_change_password_token",
                            value=encoded,
                            max_age=configs.OTP_EXP_OFFSET * 60,
                            samesite="lax",
                            secure=True,
                            httponly=False,
                        )

                    else:
                        return {
                            "isWrongPassword": True,
                            "result": "Wrong password",
                        }
                else:
                    raise DefaultError("Account is not found")

            elif type == "change-email":
                encoded = jwt.encode(
                    {
                        "id": jwtUser["id"],
                        "email": jwtUser["email"],
                        "auth_type": "email",
                        "description": "Change your Email",
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
                    title="Xác nhận thay đổi Email của bạn",
                    noteExp=os.getenv("OTP_EXP_OFFSET"),
                )

            else:
                raise NotInTypeError("account service", type)

            response.headers.set("Access-Control-Expose-Headers", "Authorization")

            response.headers.set("Authorization", encoded)

            if len(encoded) == 0:
                return {"isSended": False, "result": "Send otp email failed"}
            else:
                return response

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

            # verify_token = request.headers["Authorization"].replace("Bearer ", "")
            verify_token = request.cookies.get("verify_change_password_token")

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

            is_alive = self.__jwtredis.set_prefix(
                "verify_change_password_token"
            ).verify(verify_token)

            if is_alive == False:
                return {"success": False, "result": "Token is no longer active"}

            resultUpdate = self.__db["accounts"].update_one(
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

            if resultUpdate.modified_count == 1:
                response = make_response(
                    {
                        "success": True,
                        "logout_all_device": log_out_all_device,
                        "result": "Change password successfully",
                    }
                )

                response.delete_cookie(
                    "verify_change_password_token",
                    samesite="lax",
                    secure=True,
                    httponly=False,
                )

                log_out_all_device = decodeChangePassword["logout_all_device"] == "true"

                if log_out_all_device == True:
                    self.__jwtredis.set_prefix("user_logout")

                    self.__jwtredis.sign(
                        user_token,
                        option={"exp": configs.JWT_EXP_OFFSET * 60 * 60},
                    )

                    self.__jwtredis.set_prefix("verify_change_password_token")

                    self.__jwtredis.sign(
                        verify_token,
                        exp=configs.OTP_EXP_OFFSET * 60,
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
            verify_token = request.headers["Authorization"].replace("Bearer ", "")

            formUser = request.form

            jwtUser = jwt.decode(
                verify_token,
                str(formUser["otp"]),
                algorithms=["HS256"],
            )

            resultUpdate = self.__db["accounts"].update_one(
                {
                    "id": jwtUser["id"],
                    "email": jwtUser["email"],
                    "auth_type": "email",
                },
                {
                    "$set": {
                        "email": formUser["new_email"],
                    }
                },
            )

            if resultUpdate.modified_count == 1:
                return {"success": True}
            else:
                return {"success": False}

        except jwt.ExpiredSignatureError as e:
            return {"isOTPExpired": True, "result": "OTP is expired"}
        except (jwt.exceptions.DecodeError, jwt.exceptions.InvalidSignatureError) as e:
            return {"isInvalidOTP": True, "result": "OTP is invalid"}
        except PyMongoError as e:
            InternalServerErrorMessage(e._message)
        except Exception as e:
            InternalServerErrorMessage(e)

    def change_email(self):
        try:
            verify_token = request.headers["Authorization"].replace("Bearer ", "")

            formUser = request.form

            jwtUser = jwt.decode(
                verify_token,
                str(formUser["otp"]),
                algorithms=["HS256"],
            )

            resultUpdate = self.__db["accounts"].update_one(
                {
                    "id": jwtUser["id"],
                    "email": jwtUser["email"],
                    "auth_type": "email",
                },
                {
                    "$set": {
                        "email": formUser["new_email"],
                    }
                },
            )

            if resultUpdate.modified_count == 1:
                return {"success": True}
            else:
                return {"success": False}

        except jwt.ExpiredSignatureError as e:
            return {"isOTPExpired": True, "result": "OTP is expired"}
        except (jwt.exceptions.DecodeError, jwt.exceptions.InvalidSignatureError) as e:
            return {"isInvalidOTP": True, "result": "OTP is invalid"}
        except PyMongoError as e:
            InternalServerErrorMessage(e._message)
        except Exception as e:
            InternalServerErrorMessage(e)
