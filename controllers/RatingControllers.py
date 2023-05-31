import pymongo
from pymongo.errors import PyMongoError
from utils.JsonResponse import ConvertJsonResponse as cvtJson
from utils.ErrorMessage import BadRequestMessage, InternalServerErrorMessage
from flask import *
from pymongo import ReturnDocument
from configs.database import Database


class Rate(Database):
    def __init__(self):
        self.__db = self.ConnectMongoDB()

    def rating_movie_tv(self, type, id):
        try:
            rateValue = float(request.form["value"])
            if type == "movie":
                movie_dumps = self.__db["movies"].find_one({"id": int(id)})
                new_vote_average = (
                    movie_dumps["vote_count"] * movie_dumps["vote_average"] + rateValue
                ) / (movie_dumps["vote_count"] + 1)

                new_movie = self.__db["movies"].find_one_and_update(
                    {"id": int(id)},
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
                tv_dumps = self.__db["tvs"].find_one({"id": int(id)})
                new_vote_average = (
                    tv_dumps["vote_count"] * tv_dumps["vote_average"] + rateValue
                ) / (tv_dumps["vote_count"] + 1)

                new_tv = self.__db["tvs"].find_one_and_update(
                    {"id": int(id)},
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
        except PyMongoError as e:
            InternalServerErrorMessage(e._message)
        except Exception as e:
            InternalServerErrorMessage(e)
