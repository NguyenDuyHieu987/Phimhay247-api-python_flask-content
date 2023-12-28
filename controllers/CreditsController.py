import pymongo
from pymongo.errors import PyMongoError
from utils.JsonResponse import ConvertJsonResponse as cvtJson
from utils.ErrorMessage import BadRequestMessage, InternalServerErrorMessage
from utils.exceptions import NotInTypeError
from flask import *
from configs.database import Database


class Credits(Database):
    def __init__(self):
        self.__db = self.ConnectMongoDB()

    def get(self, id):
        try:
            credits = self.__db["credits"].find_one({"movie_id": str(id)})
            return cvtJson(credits)
        except PyMongoError as e:
            InternalServerErrorMessage(e._message)
        except NotInTypeError as e:
            BadRequestMessage(e.message)
        except Exception as e:
            InternalServerErrorMessage(e)
