import pymongo
from pymongo.errors import PyMongoError
from utils.JsonResponse import ConvertJsonResponse as cvtJson
from utils.ErrorMessage import BadRequestMessage, InternalServerErrorMessage
from flask import *
from configs.database import Database
from utils.exceptions import NotInTypeError
import jwt
import os
from utils.OTP_Generation import generateOTP
from datetime import datetime, timezone, timedelta
import configs
from utils.Sendinblue_Email_Verification import Email_Verification
from utils.JwtRedis import JwtRedis


class Account(Database):
    def __init__(self):
        self.__db = self.ConnectMongoDB()
        self.__jwtredis = JwtRedis("user_logout")

    def account_verify(self, type):
        try:
            formUser = request.form

            user_token = request.headers["Authorization"].replace("Bearer ", "")

            jwtUser = jwt.decode(
                user_token,
                str(os.getenv("JWT_SIGNATURE_SECRET")),
                algorithms=["HS256"],
            )

            isAlive = self.__jwtredis.verify(user_token)

            if isAlive == False:
                return {"isTokenAlive": False, "result": "Token is no longer active"}

            OTP = generateOTP(length=6)

            if type == "email":
                encoded = jwt.encode(
                    {
                        "id": jwtUser["id"],
                        "email": jwtUser["email"],
                        "auth_type": "email",
                        "description": "Verify your Email",
                        "exp": datetime.now(tz=timezone.utc)
                        + timedelta(seconds=configs.OTP_EXP_OFFSET),
                    },
                    str(OTP),
                    algorithm="HS256",
                )

                email_response = Email_Verification(
                    to=jwtUser["email"],
                    otp=OTP,
                    noteExp=os.getenv("OTP_EXP_OFFSET"),
                )

            elif type == "change-password":
                account = self.__db["accounts"].find_one(
                    {
                        "email": jwtUser["email"],
                        "auth_type": "email",
                        "password": formUser["old_password"],
                    }
                )

                if account != None:
                    encoded = jwt.encode(
                        {
                            "id": jwtUser["id"],
                            "email": jwtUser["email"],
                            "auth_type": "email",
                            "old_password": formUser["old_password"],
                            "new_password": formUser["new_password"],
                            "description": "Change your password",
                            "exp": datetime.now(tz=timezone.utc)
                            + timedelta(seconds=configs.OTP_EXP_OFFSET),
                        },
                        str(OTP),
                        algorithm="HS256",
                    )

                    email_response = Email_Verification(
                        to=jwtUser["email"],
                        otp=OTP,
                        title="Xác nhận thay đổi mật khẩu của bạn",
                        noteExp=os.getenv("OTP_EXP_OFFSET"),
                    )

                else:
                    return {
                        "isWrongPassword": True,
                        "result": "Wrong password",
                    }

            elif type == "change-email":
                encoded = jwt.encode(
                    {
                        "id": jwtUser["id"],
                        "email": jwtUser["email"],
                        "auth_type": "email",
                        "description": "Change your Email",
                        "exp": datetime.now(tz=timezone.utc)
                        + timedelta(seconds=configs.OTP_EXP_OFFSET),
                    },
                    str(OTP),
                    algorithm="HS256",
                )

                email_response = Email_Verification(
                    to=jwtUser["email"],
                    otp=OTP,
                    title="Xác nhận thay đổi Email của bạn",
                    noteExp=os.getenv("OTP_EXP_OFFSET"),
                )

            else:
                raise NotInTypeError("account service", type)

            response = make_response(
                {
                    "isSended": True,
                    "exp_offset": configs.OTP_EXP_OFFSET,
                    "result": "Send otp email successfully",
                }
            )

            response.headers.set("Access-Control-Expose-Headers", "Authorization")

            response.headers.set("Authorization", encoded)

            # print(email_response)
            # if "message_id" in dict(email_response):
            return response
            # else:
            #     return {"isSended": False, "result": "Send otp email failed"}
        except jwt.ExpiredSignatureError as e:
            InternalServerErrorMessage("Token is expired")
        except jwt.exceptions.DecodeError as e:
            InternalServerErrorMessage("Token is invalid")
        except NotInTypeError as e:
            BadRequestMessage(e.message)
        except PyMongoError as e:
            InternalServerErrorMessage(e._message)
        except Exception as e:
            InternalServerErrorMessage(e)

    def change_password(self):
        try:
            formUser = request.form

            user_token = request.headers["Authorization"].replace("Bearer ", "")

            jwtUser = jwt.decode(
                user_token,
                str(formUser["otp"]),
                algorithms=["HS256"],
            )

            isAlive = self.__jwtredis.verify(user_token)

            if isAlive == False:
                return {"isTokenAlive": False, "result": "Token is no longer active"}

            resultUpdate = self.__db["accounts"].update_one(
                {
                    "id": jwtUser["id"],
                    "email": jwtUser["email"],
                    "auth_type": "email",
                    "password": jwtUser["old_password"],
                },
                {
                    "$set": {
                        "password": jwtUser["new_password"],
                    }
                },
            )

            if resultUpdate.modified_count == 1:
                return {"success": True, "result": "Change password successfully"}
            else:
                return {"success": False, "result": "Change password failed"}

        except jwt.ExpiredSignatureError as e:
            return {"isOTPExpired": True, "result": "OTP is expired"}
        except jwt.exceptions.DecodeError as e:
            return {"isInvalidOTP": True, "result": "OTP is invalid"}
        except PyMongoError as e:
            InternalServerErrorMessage(e._message)
        except Exception as e:
            InternalServerErrorMessage(e)

    def change_email(self):
        try:
            user_token = request.headers["Authorization"].replace("Bearer ", "")
            formUser = request.form

            jwtUser = jwt.decode(
                user_token,
                str(formUser["otp"]),
                algorithms=["HS256"],
            )

            isAlive = self.__jwtredis.verify(user_token)

            if isAlive == False:
                return {"isTokenAlive": False, "result": "Token is no longer active"}

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
        except jwt.exceptions.DecodeError as e:
            return {"isInvalidOTP": True, "result": "OTP is invalid"}
        except PyMongoError as e:
            InternalServerErrorMessage(e._message)
        except Exception as e:
            InternalServerErrorMessage(e)
