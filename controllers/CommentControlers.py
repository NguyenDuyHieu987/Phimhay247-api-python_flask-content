import pymongo
from pymongo.errors import PyMongoError
from utils.JsonResponse import ConvertJsonResponse as cvtJson
from utils.ErrorMessage import BadRequestMessage, InternalServerErrorMessage
from utils.exceptions import DefaultError
from flask import *
from configs.database import Database
import uuid
import os
import jwt
from datetime import datetime


class Comment(Database):
    def __init__(self):
        self.__db = self.ConnectMongoDB()

    def get_commemt_by_movieid(self, movieId):
        try:
            comments = (
                self.__db["comments"]
                .find(
                    {
                        "movie_id": str(movieId),
                        "type": "parent",
                    }
                )
                .sort(
                    [("created_at", pymongo.DESCENDING)],
                )
                .skip(0)
                .limit(20)
            )

            return {"results": cvtJson(comments)}
        except PyMongoError as e:
            InternalServerErrorMessage(e._message)
        except Exception as e:
            InternalServerErrorMessage(e)

    def get_commemt_by_movieid_parentid(self, movieId, parentId):
        try:
            comments = (
                self.__db["comments"]
                .find(
                    {
                        "movie_id": str(movieId),
                        "parent_id": str(parentId),
                        "type": "children",
                    }
                )
                .sort(
                    [("created_at", pymongo.ASCENDING)],
                )
                .skip(0)
                .limit(20)
            )

            return {"results": cvtJson(comments)}
        except PyMongoError as e:
            InternalServerErrorMessage(e._message)
        except Exception as e:
            InternalServerErrorMessage(e)

    def post_comment(self, type, id):
        try:
            user_token = request.headers["Authorization"].replace("Bearer ", "")

            jwtUser = jwt.decode(
                user_token,
                str(os.getenv("JWT_TOKEN_SECRET")),
                algorithms=["HS256"],
            )

            isExistMovies = False

            if type == "movie":
                isExistMovies = self.__db["movies"].find_one({"id": str(id)}) != None
            elif type == "tv":
                isExistMovies = self.__db["tvs"].find_one({"id": str(id)}) != None

            if isExistMovies == True:
                commentForm = request.form

                if len(commentForm["content"]) == 0:
                    raise DefaultError("Content comment is not allowed empty")

                idComment = str(uuid.uuid4())

                if "parent_id" in commentForm:
                    if commentForm["parent_id"] != None:
                        resultUpdate1 = self.__db["comments"].insert_one(
                            {
                                "id": idComment,
                                "content": commentForm["content"],
                                "user_id": jwtUser["id"],
                                "username": jwtUser["username"],
                                "user_avatar": jwtUser["avatar"],
                                "movie_id": str(id),
                                "parent_id": commentForm["parent_id"],
                                "type": "children",
                                "childrens": 0,
                                "created_at": str(datetime.now()),
                                "updated_at": str(datetime.now()),
                            }
                        )

                        if resultUpdate1.acknowledged == True:
                            self.__db["comments"].update_one(
                                {
                                    "id": commentForm["parent_id"],
                                    "movie_id": str(id),
                                    "type": "parent",
                                },
                                {
                                    "$inc": {"childrens": 1},
                                },
                            )
                        else:
                            raise DefaultError("Post comment failed")

                else:
                    self.__db["comments"].insert_one(
                        {
                            "id": idComment,
                            "content": commentForm["content"],
                            "user_id": jwtUser["id"],
                            "username": jwtUser["username"],
                            "user_avatar": jwtUser["avatar"],
                            "movie_id": str(id),
                            "parent_id": commentForm["parent_id"]
                            if "parent_id" in commentForm
                            else None,
                            "type": commentForm["type"]
                            if "type" in commentForm
                            else "parent",
                            "childrens": 0,
                            "created_at": str(datetime.now()),
                            "updated_at": str(datetime.now()),
                        }
                    )

                return {
                    "success": True,
                    "result": {
                        "id": idComment,
                        "content": commentForm["content"],
                        "user_id": jwtUser["id"],
                        "username": jwtUser["username"],
                        "user_avatar": jwtUser["avatar"],
                        "movie_id": str(id),
                        "parent_id": commentForm["parent_id"]
                        if "parent_id" in commentForm
                        else None,
                        "type": commentForm["type"]
                        if "type" in commentForm
                        else "parent",
                        "childrens": 0,
                        "created_at": str(datetime.now()),
                        "updated_at": str(datetime.now()),
                    },
                }
            else:
                raise DefaultError("Movie is not exists")

        except jwt.ExpiredSignatureError as e:
            InternalServerErrorMessage("Token is expired")
        except jwt.exceptions.DecodeError as e:
            InternalServerErrorMessage("Token is invalid")
        except PyMongoError as e:
            InternalServerErrorMessage(e._message)
        except DefaultError as e:
            BadRequestMessage(e.message)
        except Exception as e:
            InternalServerErrorMessage(e)

    def delete_comment(self, type, id):
        try:
            user_token = request.headers["Authorization"].replace("Bearer ", "")

            jwtUser = jwt.decode(
                user_token,
                str(os.getenv("JWT_TOKEN_SECRET")),
                algorithms=["HS256"],
            )

            isExistMovies = False

            if type == "movie":
                isExistMovies = self.__db["movies"].find_one({"id": str(id)}) != None
            elif type == "tv":
                isExistMovies = self.__db["tvs"].find_one({"id": str(id)}) != None

            if isExistMovies == True:
                commentForm = request.form

                if commentForm["type"] == "parent":
                    self.__db["comments"].delete_one(
                        {
                            "id": commentForm["id"],
                            "user_id": jwtUser["id"],
                            "movie_id": str(id),
                            "parent_id": None,
                            "type": "parent",
                        }
                    )

                    self.__db["comments"].delete_many(
                        {
                            "movie_id": str(id),
                            "parent_id": commentForm["id"],
                            "type": "children",
                        }
                    )
                else:
                    resultDel1 = self.__db["comments"].delete_one(
                        {
                            "id": commentForm["id"],
                            "user_id": jwtUser["id"],
                            "movie_id": str(id),
                            "parent_id": commentForm["parent_id"]
                            if "parent_id" in commentForm
                            else None,
                            "type": commentForm["type"]
                            if "type" in commentForm
                            else "parent",
                        }
                    )

                    if resultDel1.deleted_count > 0:
                        self.__db["comments"].update_one(
                            {
                                "id": commentForm["parent_id"],
                                "movie_id": str(id),
                                "type": "parent",
                            },
                            {
                                "$inc": {"childrens": -1},
                            },
                        )
                    else:
                        raise DefaultError("Delete comment failed")
                return {
                    "success": True,
                }
            else:
                raise DefaultError("Movie is not exists")

        except jwt.ExpiredSignatureError as e:
            InternalServerErrorMessage("Token is expired")
        except jwt.exceptions.DecodeError as e:
            InternalServerErrorMessage("Token is invalid")
        except PyMongoError as e:
            InternalServerErrorMessage(e._message)
        except DefaultError as e:
            BadRequestMessage(e.message)
        except Exception as e:
            InternalServerErrorMessage(e)
