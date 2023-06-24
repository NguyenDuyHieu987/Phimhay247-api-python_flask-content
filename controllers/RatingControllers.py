import pymongo
from pymongo.errors import PyMongoError
from utils.JsonResponse import ConvertJsonResponse as cvtJson
from utils.ErrorMessage import BadRequestMessage, InternalServerErrorMessage
from flask import *
from pymongo import ReturnDocument
from configs.database import Database
import os
import jwt


class Rate(Database):
    def __init__(self):
        self.__db = self.ConnectMongoDB()

    def rating(self, type, id):
        try:
            user_token = request.headers["Authorization"].replace("Bearer ", "f")

            jwtUser = jwt.decode(
                user_token,
                str(os.getenv("JWT_TOKEN_SECRET")),
                algorithms=["HS256"],
            )

            rateValue = float(request.form["value"])
            if type == "movie":
                movie_dumps = self.__db["movies"].find_one({"id": str(id)})
                new_vote_average = (
                    movie_dumps["vote_count"] * movie_dumps["vote_average"] + rateValue
                ) / (movie_dumps["vote_count"] + 1)

                new_movie = self.__db["movies"].find_one_and_update(
                    {"id": str(id)},
                    {
                        "$set": {
                            "vote_average": new_vote_average,
                            "vote_count": movie_dumps["vote_count"] + 1,
                        },
                    },
                    return_document=ReturnDocument.AFTER,
                )

                return {
                    "success": True,
                    "vote_average": new_movie["vote_average"],
                    "vote_count": new_movie["vote_count"],
                }

            elif type == "tv":
                tv_dumps = self.__db["tvs"].find_one({"id": str(id)})
                new_vote_average = (
                    tv_dumps["vote_count"] * tv_dumps["vote_average"] + rateValue
                ) / (tv_dumps["vote_count"] + 1)

                new_tv = self.__db["tvs"].find_one_and_update(
                    {"id": str(id)},
                    {
                        "$set": {
                            "vote_average": new_vote_average,
                            "vote_count": tv_dumps["vote_count"] + 1,
                        },
                    },
                    return_document=ReturnDocument.AFTER,
                )

                return {
                    "success": True,
                    "vote_average": new_tv["vote_average"],
                    "vote_count": new_tv["vote_count"],
                }
        except jwt.ExpiredSignatureError as e:
            InternalServerErrorMessage("Token is expired")
        except jwt.exceptions.DecodeError as e:
            InternalServerErrorMessage("Token is invalid")
        except PyMongoError as e:
            InternalServerErrorMessage(e._message)
        except Exception as e:
            InternalServerErrorMessage(e)
