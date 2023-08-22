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

    def get_commemt_by_movieid(self, movieType, movieId):
        try:
            skip = request.args.get("skip", default=1, type=int) - 1
            limit = request.args.get("limit", default=20, type=int)

            comments = (
                self.__db["comments"]
                .find(
                    {
                        "movie_id": str(movieId),
                        "movie_type": str(movieType),
                        "type": "parent",
                    }
                )
                .sort(
                    [("created_at", pymongo.DESCENDING)],
                )
                .skip(skip * limit)
                .limit(limit)
            )

            total = self.__db["comments"].count_documents(
                {
                    "movie_id": str(movieId),
                    "movie_type": str(movieType),
                }
            )

            return {"results": cvtJson(comments), "total": total}
        except PyMongoError as e:
            InternalServerErrorMessage(e._message)
        except Exception as e:
            InternalServerErrorMessage(e)

    def get_commemt_by_movieid_parentid(self, movieType, movieId, parentId):
        try:
            skip = request.args.get("skip", default=1, type=int) - 1
            limit = request.args.get("limit", default=10, type=int)

            comments = (
                self.__db["comments"]
                .find(
                    {
                        "movie_id": str(movieId),
                        "parent_id": str(parentId),
                        "movie_type": str(movieType),
                        "type": "children",
                    }
                )
                .sort(
                    [("created_at", pymongo.ASCENDING)],
                )
                .skip(skip * limit)
                .limit(limit)
            )

            return {"results": cvtJson(comments)}
        except PyMongoError as e:
            InternalServerErrorMessage(e._message)
        except Exception as e:
            InternalServerErrorMessage(e)

    def post_comment(self, movieType, id):
        try:
            user_token = request.headers["Authorization"].replace("Bearer ", "")

            jwtUser = jwt.decode(
                user_token,
                str(os.getenv("JWT_SIGNATURE_SECRET")),
                algorithms=["HS256"],
            )

            isExistMovies = False

            if movieType == "movie":
                isExistMovies = self.__db["movies"].find_one({"id": str(id)}) != None
            elif movieType == "tv":
                isExistMovies = self.__db["tvs"].find_one({"id": str(id)}) != None

            if isExistMovies == True:
                commentForm = request.form

                if len(commentForm["content"]) == 0:
                    raise DefaultError("Content comment is not allowed empty")

                idComment = str(uuid.uuid4())

                if "parent_id" in commentForm:
                    if commentForm["parent_id"] != None:
                        resultInsert1 = self.__db["comments"].insert_one(
                            {
                                "id": idComment,
                                "content": commentForm["content"],
                                "user_id": str(jwtUser["id"]),
                                "username": jwtUser["username"],
                                "user_avatar": jwtUser["avatar"],
                                "movie_id": str(id),
                                "movie_type": str(movieType),
                                "parent_id": commentForm["parent_id"],
                                "type": "children",
                                "childrens": 0,
                                "created_at": str(datetime.now()),
                                "updated_at": str(datetime.now()),
                            }
                        )

                        if resultInsert1.acknowledged == True:
                            self.__db["comments"].update_one(
                                {
                                    "id": commentForm["parent_id"],
                                    "movie_id": str(id),
                                    "movie_type": str(movieType),
                                    "type": "parent",
                                },
                                {
                                    "$inc": {"childrens": 1},
                                },
                            )
                        else:
                            raise DefaultError("Post comment failed")

                else:
                    resultInsert2 = self.__db["comments"].insert_one(
                        {
                            "id": idComment,
                            "content": commentForm["content"],
                            "user_id": str(jwtUser["id"]),
                            "username": jwtUser["username"],
                            "user_avatar": jwtUser["avatar"],
                            "movie_id": str(id),
                            "movie_type": str(movieType),
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
                    if resultInsert2.acknowledged == False:
                        raise DefaultError("Post comment failed")

                return {
                    "success": True,
                    "result": {
                        "id": idComment,
                        "content": commentForm["content"],
                        "user_id": str(jwtUser["id"]),
                        "username": jwtUser["username"],
                        "user_avatar": jwtUser["avatar"],
                        "movie_id": str(id),
                        "movie_type": str(movieType),
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

    def edit_comment(self, movieType, id):
        try:
            user_token = request.headers["Authorization"].replace("Bearer ", "")

            jwtUser = jwt.decode(
                user_token,
                str(os.getenv("JWT_SIGNATURE_SECRET")),
                algorithms=["HS256"],
            )

            isExistMovies = False

            if movieType == "movie":
                isExistMovies = self.__db["movies"].find_one({"id": str(id)}) != None
            elif movieType == "tv":
                isExistMovies = self.__db["tvs"].find_one({"id": str(id)}) != None

            if isExistMovies == True:
                commentForm = request.form

                resultUpdate = self.__db["comments"].update_one(
                    {
                        "id": commentForm["id"],
                        "user_id": str(jwtUser["id"]),
                        "movie_id": str(id),
                        "movie_type": str(movieType),
                        # "type": commentForm["type"],
                    },
                    {
                        "$set": {
                            "content": commentForm["content"],
                            "updated": True,
                            "updated_at": str(datetime.now()),
                        },
                    },
                )

                if resultUpdate.modified_count == 1:
                    return {"success": True, "content": commentForm["content"]}
                else:
                    raise DefaultError("Update comment failed")
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

    def delete_comment(self, movieType, id):
        try:
            user_token = request.headers["Authorization"].replace("Bearer ", "")

            jwtUser = jwt.decode(
                user_token,
                str(os.getenv("JWT_SIGNATURE_SECRET")),
                algorithms=["HS256"],
            )

            isExistMovies = False

            if movieType == "movie":
                isExistMovies = self.__db["movies"].find_one({"id": str(id)}) != None
            elif movieType == "tv":
                isExistMovies = self.__db["tvs"].find_one({"id": str(id)}) != None

            if isExistMovies == True:
                commentForm = request.form

                if commentForm["type"] == "parent":
                    self.__db["comments"].delete_one(
                        {
                            "id": commentForm["id"],
                            "user_id": str(jwtUser["id"]),
                            "movie_id": str(id),
                            "movie_type": str(movieType),
                            "parent_id": None,
                            "type": "parent",
                        }
                    )

                    self.__db["comments"].delete_many(
                        {
                            "movie_id": str(id),
                            "movie_type": str(movieType),
                            "parent_id": commentForm["id"],
                            "type": "children",
                        }
                    )
                elif commentForm["type"] == "children":
                    resultDel1 = self.__db["comments"].delete_one(
                        {
                            "id": commentForm["id"],
                            "user_id": str(jwtUser["id"]),
                            "movie_id": str(id),
                            "movie_type": str(movieType),
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
                                "movie_type": str(movieType),
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
