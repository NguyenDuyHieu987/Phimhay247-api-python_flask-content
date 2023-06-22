import pymongo
from pymongo.errors import PyMongoError
from utils.JsonResponse import ConvertJsonResponse as cvtJson
from utils.ErrorMessage import BadRequestMessage, InternalServerErrorMessage
from utils.exceptions import NotInTypeError
from flask import *
from configs.database import Database


class Videos(Database):
    def __init__(self):
        self.__db = self.ConnectMongoDB()

    def get_videos(self, id):
        try:
            videos = self.__db["videos"].find_one({"id": str(id)})
            return cvtJson(videos)
        except PyMongoError as e:
            InternalServerErrorMessage(e._message)
        except NotInTypeError as e:
            BadRequestMessage(e.message)
        except Exception as e:
            InternalServerErrorMessage(e)
