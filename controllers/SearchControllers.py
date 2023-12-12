import pymongo
from pymongo import ReturnDocument
from pymongo.errors import PyMongoError
from flask import *
import random
from configs.database import Database
import jwt
import os
import uuid
from datetime import datetime
from utils.JsonResponse import ConvertJsonResponse as cvtJson
from utils.ErrorMessage import BadRequestMessage, InternalServerErrorMessage
from utils.exceptions import NotInTypeError, DefaultError


class Search(Database):
    def __init__(self):
        self.__db = self.ConnectMongoDB()

    def search(self, type):
        try:
            query = request.args.get("query", default="", type=str)
            page = request.args.get("page", default=1, type=int) - 1
            limit = request.args.get("limit", default=20, type=int)

            # if len(query) == 0:
            #     return {
            #         "page": page + 1,
            #         "page_size": limit,
            #         "results": [],
            #         "total": 0,
            #     }

            if type == "all":
                movie = cvtJson(
                    self.__db["movies"]
                    .find(
                        {
                            "$or": [
                                {"name": {"$regex": query, "$options": "i"}},
                                {"original_name": {"$regex": query, "$options": "i"}},
                            ]
                        }
                    )
                    .skip(page * int(limit / 2))
                    .limit(int(limit / 2))
                    .sort([("views", pymongo.DESCENDING)])
                )

                tv = cvtJson(
                    self.__db["tvs"]
                    .find(
                        {
                            "$or": [
                                {"name": {"$regex": query, "$options": "i"}},
                                {"original_name": {"$regex": query, "$options": "i"}},
                            ]
                        }
                    )
                    .skip(page * int(limit / 2))
                    .limit(int(limit / 2))
                    .sort([("views", pymongo.DESCENDING)])
                )

                result = movie + tv

                # random.shuffle(result)

                total_movie = self.__db["movies"].count_documents(
                    {
                        "$or": [
                            {"name": {"$regex": query, "$options": "i"}},
                            {"original_name": {"$regex": query, "$options": "i"}},
                        ]
                    }
                )

                total_tv = self.__db["tvs"].count_documents(
                    {
                        "$or": [
                            {"name": {"$regex": query, "$options": "i"}},
                            {"original_name": {"$regex": query, "$options": "i"}},
                        ]
                    }
                )

                return {
                    "page": page + 1,
                    "results": result,
                    "movie": movie,
                    "tv": tv,
                    "total": total_movie + total_tv,
                    "total_movie": total_movie,
                    "total_tv": total_tv,
                    "page_size": limit,
                }

            elif type == "tv":
                tv = cvtJson(
                    self.__db["tvs"]
                    .find(
                        {
                            "$or": [
                                {"name": {"$regex": query, "$options": "i"}},
                                {"original_name": {"$regex": query, "$options": "i"}},
                            ]
                        }
                    )
                    .skip(page * limit)
                    .limit(limit)
                    .sort([("views", pymongo.DESCENDING)])
                )

                total = self.__db["tvs"].count_documents(
                    {
                        "$or": [
                            {"name": {"$regex": query, "$options": "i"}},
                            {"original_name": {"$regex": query, "$options": "i"}},
                        ]
                    }
                )

                return {
                    "page": page + 1,
                    "results": tv,
                    "total": total,
                    "page_size": limit,
                }
            elif type == "movie":
                movie = cvtJson(
                    self.__db["movies"]
                    .find(
                        {
                            "$or": [
                                {"name": {"$regex": query, "$options": "i"}},
                                {"original_name": {"$regex": query, "$options": "i"}},
                            ]
                        }
                    )
                    .skip(page * limit)
                    .limit(limit)
                    .sort([("views", pymongo.DESCENDING)])
                )

                total = self.__db["movies"].count_documents(
                    {
                        "$or": [
                            {"name": {"$regex": query, "$options": "i"}},
                            {"original_name": {"$regex": query, "$options": "i"}},
                        ]
                    }
                )

                return {
                    "page": page + 1,
                    "results": movie,
                    "total": total,
                    "page_size": limit,
                }
            else:
                raise NotInTypeError("search", type)
        except PyMongoError as e:
            InternalServerErrorMessage(e._message)
        except NotInTypeError as e:
            BadRequestMessage(e.message)
        except Exception as e:
            InternalServerErrorMessage(e)

    def top_search(self):
        try:
            page = request.args.get("page", default=1, type=int) - 1
            limit = request.args.get("limit", default=10, type=int)

            top_search = cvtJson(
                self.__db["searchs"]
                .find(
                    {
                        "type": "search",
                    }
                )
                .skip(page * limit)
                .limit(limit)
                .sort(
                    [
                        ("updated_at", pymongo.DESCENDING),
                        ("search_times", pymongo.DESCENDING),
                    ]
                )
            )

            total = self.__db["searchs"].count_documents(
                {
                    "type": "search",
                }
            )

            result = {
                "page": page,
                "results": top_search,
                "page_size": limit,
                "total": total,
            }

            return result
        except PyMongoError as e:
            InternalServerErrorMessage(e._message)
        except NotInTypeError as e:
            BadRequestMessage(e.message)
        except Exception as e:
            InternalServerErrorMessage(e)

    def searchin_top_search(self):
        try:
            query = request.args.get("query", default="", type=str)
            page = request.args.get("page", default=1, type=int) - 1
            limit = request.args.get("limit", default=10, type=int)

            top_search = cvtJson(
                self.__db["searchs"]
                .find(
                    {
                        "type": "search",
                        "$or": [
                            {"query": {"$regex": query, "$options": "i"}},
                            {"name": {"$regex": query, "$options": "i"}},
                            {"original_name": {"$regex": query, "$options": "i"}},
                        ],
                    }
                )
                .skip(page * limit)
                .limit(limit)
                .sort(
                    [
                        ("updated_at", pymongo.DESCENDING),
                        ("search_times", pymongo.DESCENDING),
                    ]
                )
            )

            total = self.__db["searchs"].count_documents(
                {
                    "type": "search",
                    "$or": [
                        {"query": {"$regex": query, "$options": "i"}},
                        {"name": {"$regex": query, "$options": "i"}},
                        {"original_name": {"$regex": query, "$options": "i"}},
                    ],
                }
            )

            result = {
                "page": page,
                "results": top_search,
                "page_size": limit,
                "total": total,
            }

            return result
        except PyMongoError as e:
            InternalServerErrorMessage(e._message)
        except NotInTypeError as e:
            BadRequestMessage(e.message)
        except Exception as e:
            InternalServerErrorMessage(e)

    def search_history(self):
        try:
            user_token = request.headers["Authorization"].replace(
                "Bearer ", ""
            ) or request.cookies.get("user_token")

            jwtUser = jwt.decode(
                user_token,
                str(os.getenv("JWT_SIGNATURE_SECRET")),
                algorithms=["HS256"],
            )

            page = request.args.get("page", default=1, type=int) - 1
            limit = request.args.get("limit", default=10, type=int)

            search_history = cvtJson(
                self.__db["searchs"]
                .find(
                    {
                        "user_id": jwtUser["id"],
                        "type": "history",
                    }
                )
                .skip(page * limit)
                .limit(limit)
                .sort(
                    [
                        ("updated_at", pymongo.DESCENDING),
                        ("search_times", pymongo.DESCENDING),
                    ]
                )
            )

            total = self.__db["searchs"].count_documents(
                {
                    "user_id": jwtUser["id"],
                    "type": "history",
                }
            )

            result = {
                "page": page,
                "results": search_history,
                "page_size": limit,
                "total": total,
            }

            return result

        except jwt.ExpiredSignatureError as e:
            InternalServerErrorMessage("Token is expired")
        except (jwt.exceptions.DecodeError, jwt.exceptions.InvalidSignatureError) as e:
            InternalServerErrorMessage("Token is invalid")
        except PyMongoError as e:
            InternalServerErrorMessage(e._message)
        except NotInTypeError as e:
            BadRequestMessage(e.message)
        except Exception as e:
            InternalServerErrorMessage(e)

    def searchin_history(self):
        try:
            user_token = request.headers["Authorization"].replace(
                "Bearer ", ""
            ) or request.cookies.get("user_token")

            jwtUser = jwt.decode(
                user_token,
                str(os.getenv("JWT_SIGNATURE_SECRET")),
                algorithms=["HS256"],
            )

            query = request.args.get("query", default="", type=str)
            page = request.args.get("page", default=1, type=int) - 1
            limit = request.args.get("limit", default=10, type=int)

            search_history = cvtJson(
                self.__db["searchs"]
                .find(
                    {
                        "user_id": jwtUser["id"],
                        "type": "history",
                        "query": {"$regex": query, "$options": "i"},
                    }
                )
                .skip(page * limit)
                .limit(limit)
                .sort(
                    [
                        ("updated_at", pymongo.DESCENDING),
                        ("search_times", pymongo.DESCENDING),
                    ]
                )
            )

            total = self.__db["searchs"].count_documents(
                {
                    "user_id": jwtUser["id"],
                    "type": "history",
                    "query": {"$regex": query, "$options": "i"},
                }
            )

            result = {
                "page": page,
                "results": search_history,
                "page_size": limit,
                "total": total,
            }

            return result
        except jwt.ExpiredSignatureError as e:
            InternalServerErrorMessage("Token is expired")
        except (jwt.exceptions.DecodeError, jwt.exceptions.InvalidSignatureError) as e:
            InternalServerErrorMessage("Token is invalid")
        except PyMongoError as e:
            InternalServerErrorMessage(e._message)
        except NotInTypeError as e:
            BadRequestMessage(e.message)
        except Exception as e:
            InternalServerErrorMessage(e)

    def add_search(self):
        try:
            movie_id = request.form["movie_id"]
            media_type = request.form["media_type"]
            search_query = request.args.get("query", default="", type=str)

            if movie_id != None and media_type != None:
                movie = None

                if media_type == "movie":
                    movie = self.__db["movies"].find_one({"id": str(movie_id)})
                elif media_type == "tv":
                    movie = self.__db["tvs"].find_one({"id": str(movie_id)})
                else:
                    raise NotInTypeError("movie", media_type)

                if movie != None:
                    item_search = self.__db["searchs"].find_one(
                        {
                            "movie_id": movie_id,
                            "media_type": media_type,
                            "type": "search",
                            #  "query": search_query,
                        }
                    )

                    if item_search != None:
                        result_updated = self.__db["searchs"].update_one(
                            {
                                "movie_id": movie_id,
                                "media_type": media_type,
                                "type": "search",
                            },
                            {
                                "$set": {
                                    "updated_at": datetime.now(),
                                },
                                "$inc": {"search_times": 1},
                            },
                        )

                        if result_updated.modified_count == 1:
                            return {
                                "updated": True,
                                "result": "Update search successfully",
                            }
                        else:
                            return {
                                "updated": False,
                                "result": "Update search failed",
                            }
                    else:
                        id_search = str(uuid.uuid4())

                        result_inserted = None

                        if movie["media_type"] == "movie":
                            result_inserted = self.__db["searchs"].insert_one(
                                {
                                    "id": id_search,
                                    "type": "search",
                                    "query": movie["name"],
                                    "search_times": 0,
                                    "movie_id": movie["id"],
                                    "media_type": movie["media_type"],
                                    "adult": movie["adult"],
                                    "backdrop_path": movie["backdrop_path"],
                                    "release_date": movie["release_date"],
                                    "name": movie["name"],
                                    "original_name": movie["original_name"],
                                    "overview": movie["overview"],
                                    "poster_path": movie["poster_path"],
                                    "genres": movie["genres"],
                                    "runtime": movie["runtime"],
                                    "created_at": datetime.now(),
                                    "updated_at": datetime.now(),
                                }
                            )
                        elif movie["media_type"] == "tv":
                            result_inserted = self.__db["searchs"].insert_one(
                                {
                                    "id": id_search,
                                    "type": "search",
                                    "query": movie["name"],
                                    "search_times": 0,
                                    "movie_id": movie["id"],
                                    "media_type": movie["media_type"],
                                    "adult": movie["adult"],
                                    "backdrop_path": movie["backdrop_path"],
                                    "first_air_date": movie["first_air_date"],
                                    "last_air_date": movie["last_air_date"],
                                    "name": movie["name"],
                                    "original_name": movie["original_name"],
                                    "overview": movie["overview"],
                                    "poster_path": movie["poster_path"],
                                    "genres": movie["genres"],
                                    "episode_run_time": movie["episode_run_time"],
                                    "created_at": datetime.now(),
                                    "updated_at": datetime.now(),
                                }
                            )

                        if result_inserted.inserted_id != None:
                            search_inserted = self.__db["searchs"].find_one(
                                {
                                    "id": id_search,
                                }
                            )

                            return {
                                "added": True,
                                "result": search_inserted,
                            }
                        else:
                            return {
                                "success": False,
                                "result": "Add search failed",
                            }
                else:
                    raise DefaultError("Movie is not exists")

            else:
                item_search = self.__db["searchs"].find_one(
                    {
                        "type": "search",
                        "query": search_query,
                    }
                )

                if item_search != None:
                    result_updated = self.__db["searchs"].update_one(
                        {
                            "type": "search",
                            "query": search_query,
                        },
                        {
                            "$set": {
                                "updated_at": datetime.now(),
                            },
                            "$inc": {"search_times": 1},
                        },
                    )

                    if result_updated.modified_count == 1:
                        return {
                            "updated": True,
                            "result": "Update search successfully",
                        }
                    else:
                        return {
                            "updated": False,
                            "result": "Update search failed",
                        }

                else:
                    movie1 = []

                    movie1 = cvtJson(
                        self.__db["movies"]
                        .find(
                            {
                                "$or": [
                                    {"name": {"$regex": search_query, "$options": "i"}},
                                    {
                                        "original_name": {
                                            "$regex": search_query,
                                            "$options": "i",
                                        }
                                    },
                                ],
                            }
                        )
                        .skip(0)
                        .limit(1)
                        .sort([("views", pymongo.DESCENDING)])
                    )

                    if len(movie1) == 0:
                        movie1 = cvtJson(
                            self.__db["tvs"]
                            .find(
                                {
                                    "$or": [
                                        {
                                            "name": {
                                                "$regex": search_query,
                                                "$options": "i",
                                            }
                                        },
                                        {
                                            "original_name": {
                                                "$regex": search_query,
                                                "$options": "i",
                                            }
                                        },
                                    ],
                                }
                            )
                            .skip(0)
                            .limit(1)
                            .sort([("views", pymongo.DESCENDING)])
                        )

                    if len(movie1) != 0:
                        item_search = self.__db["searchs"].find_one(
                            {
                                "movie_id": movie1["id"],
                                "media_type": movie1["media_type"],
                                "type": "search",
                            }
                        )

                        if item_search != None:
                            result_updated = self.__db["searchs"].update_one(
                                {
                                    "movie_id": movie1["id"],
                                    "media_type": movie1["media_type"],
                                    "type": "search",
                                },
                                {
                                    "$set": {
                                        "updated_at": datetime.now(),
                                    },
                                    "$inc": {"search_times": 1},
                                },
                            )

                            if result_updated.modified_count == 1:
                                return {
                                    "updated": True,
                                    "result": "Update search successfully",
                                }
                            else:
                                return {
                                    "updated": False,
                                    "result": "Update search failed",
                                }

                    else:
                        id_search = str(uuid.uuid4())

                        result_inserted = None

                        if movie1["media_type"] == "movie":
                            result_inserted = self.__db["searchs"].insert_one(
                                {
                                    "id": id_search,
                                    "type": "search",
                                    "query": movie1["name"],
                                    "search_times": 0,
                                    "movie_id": movie1["id"],
                                    "media_type": movie1["media_type"],
                                    "adult": movie1["adult"],
                                    "backdrop_path": movie1["backdrop_path"],
                                    "release_date": movie1["release_date"],
                                    "name": movie1["name"],
                                    "original_name": movie1["original_name"],
                                    "overview": movie1["overview"],
                                    "poster_path": movie1["poster_path"],
                                    "genres": movie1["genres"],
                                    "runtime": movie1["runtime"],
                                    "created_at": datetime.now(),
                                    "updated_at": datetime.now(),
                                }
                            )
                        elif movie1["media_type"] == "tv":
                            result_inserted = self.__db["searchs"].insert_one(
                                {
                                    "id": id_search,
                                    "type": "search",
                                    "query": movie1["name"],
                                    "search_times": 0,
                                    "movie_id": movie1["id"],
                                    "media_type": movie1["media_type"],
                                    "adult": movie1["adult"],
                                    "backdrop_path": movie1["backdrop_path"],
                                    "first_air_date": movie1["first_air_date"],
                                    "last_air_date": movie1["last_air_date"],
                                    "name": movie1["name"],
                                    "original_name": movie1["original_name"],
                                    "overview": movie1["overview"],
                                    "poster_path": movie1["poster_path"],
                                    "genres": movie1["genres"],
                                    "episode_run_time": movie1["episode_run_time"],
                                    "created_at": datetime.now(),
                                    "updated_at": datetime.now(),
                                }
                            )

                        if result_inserted.inserted_id != None:
                            search_inserted = self.__db["searchs"].find_one(
                                {
                                    "id": id_search,
                                }
                            )

                            return {
                                "added": True,
                                "result": search_inserted,
                            }
                        else:
                            return {
                                "success": False,
                                "result": "Add search failed",
                            }

        except PyMongoError as e:
            InternalServerErrorMessage(e._message)
        except NotInTypeError as e:
            BadRequestMessage(e.message)
        except DefaultError as e:
            BadRequestMessage(e.message)
        except Exception as e:
            InternalServerErrorMessage(e)

    def add_history(self):
        try:
            user_token = request.headers["Authorization"].replace(
                "Bearer ", ""
            ) or request.cookies.get("user_token")

            jwtUser = jwt.decode(
                user_token,
                str(os.getenv("JWT_SIGNATURE_SECRET")),
                algorithms=["HS256"],
            )

            search_query = request.form["query"]

            item_search_history = self.__db["searchs"].find_one(
                {
                    "user_id": jwtUser["id"],
                    "type": "history",
                    "query": search_query,
                }
            )

            # item_search_history_upserted = self.__db["searchs"].find_one_and_update(
            #     {
            #         "user_id": jwtUser["id"],
            #         "type": "history",
            #         "query": search_query,
            #     },
            #     {"$set": {"value": "new-value"}},
            #     upsert=True,
            #     return_document=ReturnDocument.AFTER,
            # )

            if item_search_history != None:
                result_updated = self.__db["searchs"].update_one(
                    {
                        "user_id": jwtUser["id"],
                        "type": "history",
                        "query": search_query,
                    },
                    {
                        "$set": {
                            "updated_at": datetime.now(),
                        },
                        "$inc": {"search_times": 1},
                    },
                )

                if result_updated.modified_count == 1:
                    return {
                        "updated": True,
                        "result": "Update search history successfully",
                    }
                else:
                    return {
                        "updated": False,
                        "result": "Update search history failed",
                    }
            else:
                id_search_history = str(uuid.uuid4())

                result_inserted = self.__db["searchs"].insert_one(
                    {
                        "id": id_search_history,
                        "user_id": jwtUser["id"],
                        "type": "history",
                        "query": search_query,
                        "search_times": 0,
                        "created_at": datetime.now(),
                        "updated_at": datetime.now(),
                    }
                )

                if result_inserted.inserted_id != None:
                    search_history_inserted = self.__db["searchs"].find_one(
                        {
                            "id": id_search_history,
                        }
                    )

                    return {
                        "added": True,
                        "result": search_history_inserted,
                    }
                else:
                    return {
                        "success": False,
                        "result": "Add search history failed",
                    }

        except jwt.ExpiredSignatureError as e:
            InternalServerErrorMessage("Token is expired")
        except (jwt.exceptions.DecodeError, jwt.exceptions.InvalidSignatureError) as e:
            InternalServerErrorMessage("Token is invalid")
        except PyMongoError as e:
            InternalServerErrorMessage(e._message)
        except DefaultError as e:
            BadRequestMessage(e.message)
        except Exception as e:
            InternalServerErrorMessage(e)

    def remove_history(self):
        try:
            user_token = request.headers["Authorization"].replace(
                "Bearer ", ""
            ) or request.cookies.get("user_token")

            jwtUser = jwt.decode(
                user_token,
                str(os.getenv("JWT_SIGNATURE_SECRET")),
                algorithms=["HS256"],
            )

            id = request.form["id"]

            item_search_history = self.__db["searchs"].find_one(
                {
                    "id": id,
                    "user_id": jwtUser["id"],
                    "type": "history",
                }
            )

            if item_search_history != None:
                result_deleted = self.__db["searchs"].delete_one(
                    {
                        "id": id,
                        "user_id": jwtUser["id"],
                        "type": "history",
                    }
                )

                if result_deleted.deleted_count == 1:
                    return {
                        "success": True,
                        "result": "Delete search history successfully",
                    }
                else:
                    return {
                        "success": False,
                        "result": "Delete search history failed",
                    }
            else:
                raise DefaultError(f"Search history with id: {id} is not found")

        except jwt.ExpiredSignatureError as e:
            InternalServerErrorMessage("Token is expired")
        except (jwt.exceptions.DecodeError, jwt.exceptions.InvalidSignatureError) as e:
            InternalServerErrorMessage("Token is invalid")
        except PyMongoError as e:
            InternalServerErrorMessage(e._message)
        except DefaultError as e:
            BadRequestMessage(e.message)
        except Exception as e:
            InternalServerErrorMessage(e)

    def clear_search(self):
        try:
            user_token = request.headers["Authorization"].replace(
                "Bearer ", ""
            ) or request.cookies.get("user_token")

            jwtUser = jwt.decode(
                user_token,
                str(os.getenv("JWT_SIGNATURE_SECRET")),
                algorithms=["HS256"],
            )

            result_deleted = self.__db["searchs"].delete_many(
                {
                    "user_id": jwtUser["id"],
                    "type": "history",
                }
            )

            if result_deleted.deleted_count >= 1:
                return {
                    "success": True,
                    "result": "Clear search history successfully",
                }
            else:
                return {
                    "success": False,
                    "result": "Clear search history failed",
                }

        except jwt.ExpiredSignatureError as e:
            InternalServerErrorMessage("Token is expired")
        except (jwt.exceptions.DecodeError, jwt.exceptions.InvalidSignatureError) as e:
            InternalServerErrorMessage("Token is invalid")
        except PyMongoError as e:
            InternalServerErrorMessage(e._message)
        except DefaultError as e:
            BadRequestMessage(e.message)
        except Exception as e:
            InternalServerErrorMessage(e)
