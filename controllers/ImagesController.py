import pymongo
from pymongo.errors import PyMongoError
from utils.JsonResponse import ConvertJsonResponse as cvtJson
from utils.ErrorMessage import BadRequestMessage, InternalServerErrorMessage
from utils.exceptions import NotInTypeError
from flask import *
from configs.database import Database


class Images(Database):
    def __init__(self):
        self.__db = self.ConnectMongoDB()

    def get_images(self, id):
        try:
            images = self.__db["images"].find_one({"movie_id": str(id)})
            return cvtJson(images)
        except PyMongoError as e:
            InternalServerErrorMessage(e._message)
        except NotInTypeError as e:
            BadRequestMessage(e.message)
        except Exception as e:
            InternalServerErrorMessage(e)
