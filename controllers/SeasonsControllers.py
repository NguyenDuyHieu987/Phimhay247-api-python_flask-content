import pymongo
from pymongo.errors import PyMongoError
from utils.JsonResponse import ConvertJsonResponse as cvtJson
from utils.ErrorMessage import BadRequestMessage, InternalServerErrorMessage
from flask import *
from configs.database import Database
from utils.exceptions import DefaultError


class Season(Database):
    def __init__(self):
        self.__db = self.ConnectMongoDB()

    def get_list(self, seriesId):
        try:
            seasons = cvtJson(
                self.__db["seasons"].find(
                    {"series_id": seriesId},
                )
            )

            if len(seasons) > 0:
                return {"results": seasons}
            else:
                raise DefaultError("Seasons is not exist")

        except PyMongoError as e:
            InternalServerErrorMessage(e._message)
        except DefaultError as e:
            BadRequestMessage(e.message)
        except Exception as e:
            InternalServerErrorMessage(e)

    def get(self, movieId, seasonId):
        try:
            season = cvtJson(
                self.__db["seasons"].aggregate(
                    [
                        {
                            "$match": {
                                "id": seasonId,
                                "movie_id": movieId,
                                # "season_number": seasonNumber,
                            }
                        },
                        {
                            "$lookup": {
                                "from": "episodes",
                                "localField": "id",
                                "foreignField": "season_id",
                                "as": "episodes",
                                "let": {"id": "$id", "movieId": "$movie_id"},
                                "pipeline": [
                                    {
                                        "$match": {
                                            "$expr": {
                                                "$and": [
                                                    {"$eq": ["$season_id", "$$id"]},
                                                    {"$eq": ["$movie_id", "$$movieId"]},
                                                ],
                                            },
                                        },
                                    },
                                ],
                            }
                        },
                    ]
                )
            )

            if len(season) > 0:
                return season[0]
            else:
                raise DefaultError("Season is not exist")

        except PyMongoError as e:
            InternalServerErrorMessage(e._message)
        except DefaultError as e:
            BadRequestMessage(e.message)
        except Exception as e:
            InternalServerErrorMessage(e)
