import pymongo
from pymongo.errors import PyMongoError
from utils.JsonResponse import ConvertJsonResponse as cvtJson
from utils.ErrorMessage import BadRequestMessage, InternalServerErrorMessage
from flask import *
from configs.database import Database
import jwt
import os


class Account(Database):
    def __init__(self):
        self.__db = self.ConnectMongoDB()

    def change_password(self):
        try:
            user_token = request.headers["Authorization"].replace("Bearer ", "")

            jwtUser = jwt.decode(
                user_token,
                str(os.getenv("JWT_TOKEN_SECRET")),
                algorithms=["HS256"],
            )

            formData = request.form

            resultUpdate = self.__db["accounts"].update_one(
                {
                    "id": jwtUser["id"],
                    "email": jwtUser["email"],
                    "auth_type": "email",
                    "password": formData["old_password"],
                },
                {
                    "$set": {
                        "password": formData["new_password"],
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
