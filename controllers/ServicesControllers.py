import pymongo
from pymongo.errors import PyMongoError
from utils.JsonResponse import ConvertJsonResponse as cvtJson
from utils.ErrorMessage import BadRequestMessage, InternalServerErrorMessage
from utils.exceptions import NotInTypeError
from flask import *
from configs.database import Database


class Genre(Database):
    def __init__(self):
        self.__db = self.ConnectMongoDB()

    def genres(self, type):
        try:
            if type == "all":
                genres = cvtJson(self.__db["genres"].find())
                return {"result": genres}
            else:
                raise NotInTypeError("genre", type)
        except PyMongoError as e:
            InternalServerErrorMessage(e._message)
        except NotInTypeError as e:
            BadRequestMessage(e.message)
        except Exception as e:
            InternalServerErrorMessage(e)
