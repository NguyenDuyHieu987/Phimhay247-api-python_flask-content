import pymongo
from pymongo.errors import PyMongoError
from utils.JsonResponse import ConvertJsonResponse as cvtJson
from utils.ErrorMessage import BadRequestMessage, InternalServerErrorMessage
from flask import *
from configs.database import Database
import jwt
import os
from utils.OTP_Generation import generateOTP
from datetime import datetime, timezone, timedelta
import configs


class Account(Database):
    def __init__(self):
        self.__db = self.ConnectMongoDB()

    def change_password(self):
        try:
            formUser = request.form

            user_token = request.headers["Authorization"].replace("Bearer ", "")

            jwtUser = jwt.decode(
                user_token,
                str(formUser["otp"]),
                algorithms=["HS256"],
            )

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
                return {"success": True}
            else:
                return {"success": False}

        except jwt.ExpiredSignatureError as e:
            InternalServerErrorMessage("Token is expired")
        except jwt.exceptions.DecodeError as e:
            InternalServerErrorMessage("Token is invalid")
        except PyMongoError as e:
            InternalServerErrorMessage(e._message)
        except Exception as e:
            InternalServerErrorMessage(e)

    def change_email(self):
        try:
            user_token = request.headers["Authorization"].replace("Bearer ", "")

            jwtUser = jwt.decode(
                user_token,
                str(os.getenv("JWT_SIGNATURE_SECRET")),
                algorithms=["HS256"],
            )

            formData = request.form

            resultUpdate = self.__db["accounts"].update_one(
                {
                    "id": jwtUser["id"],
                    "email": jwtUser["email"],
                    "auth_type": "email",
                },
                {
                    "$set": {
                        "email": formData["new_email"],
                    }
                },
            )

            if resultUpdate.modified_count == 1:
                return {"success": True}
            else:
                return {"success": False}

        except jwt.ExpiredSignatureError as e:
            InternalServerErrorMessage("Token is expired")
        except jwt.exceptions.DecodeError as e:
            InternalServerErrorMessage("Token is invalid")
        except PyMongoError as e:
            InternalServerErrorMessage(e._message)
        except Exception as e:
            InternalServerErrorMessage(e)

    def change_fullname(self):
        try:
            user_token = request.headers["Authorization"].replace("Bearer ", "")

            jwtUser = jwt.decode(
                user_token,
                str(os.getenv("JWT_SIGNATURE_SECRET")),
                algorithms=["HS256"],
            )

            formData = request.form

            resultUpdate = self.__db["accounts"].update_one(
                {
                    "id": jwtUser["id"],
                    "email": jwtUser["email"],
                    "auth_type": "email",
                    "full_name": jwtUser["full_name"],
                },
                {
                    "$set": {
                        "full_name": formData["new_full_name"],
                    }
                },
            )

            if resultUpdate.modified_count == 1:
                return {"success": True}
            else:
                return {"success": False}

        except jwt.ExpiredSignatureError as e:
            InternalServerErrorMessage("Token is expired")
        except jwt.exceptions.DecodeError as e:
            InternalServerErrorMessage("Token is invalid")
        except PyMongoError as e:
            InternalServerErrorMessage(e._message)
        except Exception as e:
            InternalServerErrorMessage(e)

    def verify_email(self, type):
        try:
            formUser = request.form

            user_token = request.headers["Authorization"].replace("Bearer ", "")

            jwtUser = jwt.decode(
                user_token,
                str(os.getenv("JWT_SIGNATURE_SECRET")),
                algorithms=["HS256"],
            )

            if type == "change-password":
                account = self.__db["accounts"].find_one(
                    {
                        "email": jwtUser["email"],
                        "auth_type": "email",
                        "password": formUser["old_password"],
                    }
                )

                if account != None:
                    OTP = generateOTP(length=6)

                    encoded = jwt.encode(
                        {
                            "id": formUser["id"],
                            "email": formUser["email"],
                            "auth_type": "email",
                            "old_password": formUser["old_password"],
                            "new_password": formUser["new_password"],
                            "exp": datetime.now(tz=timezone.utc)
                            + timedelta(seconds=configs.OTP_EXP_OFFSET),
                        },
                        str(OTP),
                        algorithm="HS256",
                    )

                    response = make_response(
                        {
                            "isVerify": True,
                            "exp_offset": configs.OTP_EXP_OFFSET,
                            "result": "Send otp email successfully",
                        }
                    )

                    response.headers.set(
                        "Access-Control-Expose-Headers", "Authorization"
                    )

                    response.headers.set("Authorization", encoded)
                    # email_response = Email_Verification(to=formUser["email"], otp=OTP)

                    # print(email_response)
                    # if "message_id" in dict(email_response):
                    return response
                    # else:
                    #     return {"isSendEmail": False, "result": "Send otp email failed"}

                else:
                    return {
                        "isWrongPassword": True,
                        "result": "Wrong password",
                    }

        except jwt.ExpiredSignatureError as e:
            InternalServerErrorMessage("Token is expired")
        except jwt.exceptions.DecodeError as e:
            InternalServerErrorMessage("Token is invalid")
        except PyMongoError as e:
            InternalServerErrorMessage(e._message)
        except Exception as e:
            InternalServerErrorMessage(e)
