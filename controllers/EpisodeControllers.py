import pymongo
from pymongo.errors import PyMongoError
from utils.JsonResponse import ConvertJsonResponse as cvtJson
from utils.ErrorMessage import BadRequestMessage, InternalServerErrorMessage
from flask import *
from configs.database import Database
from utils.exceptions import DefaultError


class Episode(Database):
    def __init__(self):
        self.__db = self.ConnectMongoDB()

    def get_list(self, movieId, seasonId):
        try:
            episodes = cvtJson(
                self.__db["episodes"].find(
                    {
                        "movie_id": movieId,
                        "season_id": seasonId,
                        #  "season_number": seasonNumber,
                    },
                )
            )

            if len(cvtJson(episodes)) > 0:
                return cvtJson({"results": episodes})
            else:
                raise DefaultError("Episodes is not exist")

        except PyMongoError as e:
            InternalServerErrorMessage(e._message)
        except DefaultError as e:
            BadRequestMessage(e.message)
        except Exception as e:
            InternalServerErrorMessage(e)

    def get(self, movieId, seasonId, episodeNumber):
        try:
            episode = self.__db["episodes"].find_one(
                {
                    "movie_id": movieId,
                    "season_id": seasonId,
                    #  "season_number": seasonNumber,
                    "episode_number": int(episodeNumber),
                },
            )

            if episode != None:
                return cvtJson(episode)
            else:
                raise DefaultError("Episode is not exist")

        except PyMongoError as e:
            InternalServerErrorMessage(e._message)
        except DefaultError as e:
            BadRequestMessage(e.message)
        except Exception as e:
            InternalServerErrorMessage(e)
