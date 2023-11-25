import pymongo
from pymongo.errors import PyMongoError
from utils.JsonResponse import ConvertJsonResponse as cvtJson
from utils.ErrorMessage import BadRequestMessage, InternalServerErrorMessage
from flask import *
from pymongo import ReturnDocument
from configs.database import Database
import os
import jwt


class TV(Database):
    def __init__(self):
        self.__db = self.ConnectMongoDB()

    def detail_tv(self, id):
        try:
            append_to_response = request.args.get(
                "append_to_response", default="", type=str
            )
            # exceptValue = {"images": 0, "credits": 0, "videos": 0}
            extraValue = {
                "images": [],
                "videos": [],
                "credits": [],
                "seasons": [],
                "episodes": [],
            }

            if append_to_response != "":
                if "images" in append_to_response.split(","):
                    # images = self.__db["images"].find_one(
                    #     {"movie_id": str(id)})
                    # extraValue["images"] = images["items"]

                    extraValue["images"] = [
                        {
                            "$lookup": {
                                "from": "images",
                                "localField": "id",
                                "foreignField": "movie_id",
                                "as": "images",
                            },
                        },
                        {"$unwind": "$images"},
                        {
                            "$addFields": {
                                "images": "$images.items",
                            },
                        },
                    ]

                if "videos" in append_to_response.split(","):
                    # videos = self.__db["videos"].find_one(
                    #     {"movie_id": str(id)})
                    # extraValue["videos"] = videos["items"]

                    extraValue["videos"] = [
                        {
                            "$lookup": {
                                "from": "videos",
                                "localField": "id",
                                "foreignField": "movie_id",
                                "as": "videos",
                            },
                        },
                        {"$unwind": "$videos"},
                        {
                            "$addFields": {
                                "videos": "$videos.items",
                            },
                        },
                    ]

                if "credits" in append_to_response.split(","):
                    # credits = self.__db["credits"].find_one(
                    #     {"movie_id": str(id)})
                    # extraValue["credits"] = credits["items"]

                    extraValue["credits"] = [
                        {
                            "$lookup": {
                                "from": "credits",
                                "localField": "id",
                                "foreignField": "movie_id",
                                "as": "credits",
                            },
                        },
                        {"$unwind": "$credits"},
                        {
                            "$addFields": {
                                "credits": "$credits.items",
                            },
                        },
                    ]

                if "seasons" in append_to_response.split(","):
                    # seasons = self.__db["seasons"].find({
                    #     "movie_id": id,
                    # })

                    # extraValue["seasons"] = seasons

                    extraValue["seasons"] = [
                        {
                            "$lookup": {
                                "from": "seasons",
                                "localField": "season_id",
                                "foreignField": "id",
                                "as": "season",
                            },
                        },
                        {"$unwind": "$season"},
                        {
                            "$lookup": {
                                "from": "seasons",
                                "localField": "series_id",
                                "foreignField": "series_id",
                                "as": "seasons",
                            },
                        },
                        {
                            "$addFields": {
                                "number_of_seasons": {"$size": "$seasons"},
                            },
                        },
                    ]

                if "episodes" in append_to_response.split(","):
                    # episodes = self.__db["episodes"].find({
                    #     "movie_id": id,
                    # })

                    # extraValue["episodes"] = episodes

                    extraValue["episodes"] = [
                        {
                            "$lookup": {
                                "from": "episodes",
                                "localField": "id",
                                "foreignField": "movie_id",
                                "as": "episodes",
                            },
                        },
                        {
                            "$lookup": {
                                "from": "episodes",
                                "localField": "season_id",
                                "foreignField": "season_id",
                                "as": "episodes",
                            },
                        },
                        # {
                        #     "$addFields": {
                        #         "number_of_episodes": {"$size": '$episodes'},
                        #     },
                        # },
                    ]

            headers = request.headers

            extraValue2 = {
                "list": [],
                "history": [],
                "rate": [],
            }

            if "Authorization" in headers or request.cookies.get("user_token") != None:
                user_token = request.headers["Authorization"].replace(
                    "Bearer ", ""
                ) or request.cookies.get("user_token")

                jwtUser = jwt.decode(
                    user_token,
                    str(os.getenv("JWT_SIGNATURE_SECRET")),
                    algorithms=["HS256"],
                )

                # item_list = self.__db["lists"].find_one(
                #     {
                #         "user_id": jwtUser["id"],
                #         "movie_id": id,
                #         "media_type": "tv",
                #     },
                # )

                # if item_list != None:
                #     extraValue2 = extraValue2 | {"in_list": True}

                extraValue2["list"] = [
                    {
                        "$lookup": {
                            "from": "lists",
                            "localField": "id",
                            "foreignField": "movie_id",
                            "pipeline": [
                                {
                                    "$match": {
                                        "$and": [
                                            {"$expr": {"$eq": ["$media_type", "tv"]}},
                                            {
                                                "$expr": {
                                                    "$eq": ["$user_id", jwtUser["id"]]
                                                }
                                            },
                                        ],
                                    },
                                },
                            ],
                            "as": "in_list",
                        },
                    },
                    {
                        "$addFields": {
                            "in_list": {
                                "$eq": [{"$size": "$in_list"}, 1],
                            },
                        },
                    },
                ]

                # item_history = self.__db["histories"].find_one(
                #     {
                #         "user_id": jwtUser["id"],
                #         "movie_id": id,
                #         "media_type": "tv",
                #     },
                # )

                # if item_history != None:
                #     extraValue2 = extraValue2 | {
                #         "history_progress": {
                #             "duration": item_history["duration"],
                #             "percent": item_history["percent"],
                #             "seconds": item_history["seconds"],
                #         },
                #     }

                extraValue2["history"] = [
                    {
                        "$lookup": {
                            "from": "histories",
                            "localField": "id",
                            "foreignField": "movie_id",
                            "pipeline": [
                                {
                                    "$match": {
                                        "$and": [
                                            {"$expr": {"$eq": ["$media_type", "tv"]}},
                                            {
                                                "$expr": {
                                                    "$eq": ["$user_id", jwtUser["id"]]
                                                }
                                            },
                                        ],
                                    },
                                },
                            ],
                            "as": "history_progress",
                        },
                    },
                    {
                        "$addFields": {
                            "history_progress": {
                                "$cond": [
                                    {
                                        "$eq": [
                                            {"$size": "$history_progress"},
                                            1,
                                        ],
                                    },
                                    {
                                        "duration": "$history_progress.duration",
                                        "percent": "$history_progress.percent",
                                        "seconds": "$history_progress.seconds",
                                    },
                                    "$$REMOVE",
                                ],
                            },
                        },
                    },
                ]

                # rates = self.__db["rates"].find_one(
                #     {
                #         "user_id": jwtUser["id"],
                #         "movie_id": str(id),
                #         "movie_type": "tv",
                #     }
                # )

                # if rates != None:
                #     extraValue2 = extraValue2 | {
                #         "rated_value": rates["rate_value"],
                #     }

                extraValue2["rate"] = [
                    {
                        "$lookup": {
                            "from": "rates",
                            "localField": "id",
                            "foreignField": "movie_id",
                            "pipeline": [
                                {
                                    "$match": {
                                        "$and": [
                                            {"$expr": {"$eq": ["$movie_type", "tv"]}},
                                            {
                                                "$expr": {
                                                    "$eq": ["$user_id", jwtUser["id"]]
                                                }
                                            },
                                        ],
                                    },
                                },
                            ],
                            "as": "rated_value",
                        },
                    },
                    {
                        "$unwind": {
                            "path": "$rated_value",
                            "preserveNullAndEmptyArrays": True,
                        },
                    },
                    {
                        "$addFields": {
                            "rated_value": "$rated_value.rate_value",
                        },
                    },
                ]

                # return cvtJson(tv[0] | extraValue2)

            tv = cvtJson(
                self.__db["tvs"].aggregate(
                    [
                        {
                            "$match": {"id": id},
                        },
                        *extraValue["images"],
                        *extraValue["videos"],
                        *extraValue["credits"],
                        *extraValue["seasons"],
                        *extraValue["episodes"],
                        *extraValue2["list"],
                        *extraValue2["history"],
                        *extraValue2["rate"],
                    ]
                )
            )

            if len(tv) == 0:
                return {"not_found": True, "result": "Can not find the tv"}

            return cvtJson(tv[0])
            # | extraValue

        except jwt.ExpiredSignatureError as e:
            make_response().delete_cookie(
                "user_token", samesite="lax", secure=True, httponly=False
            )
            InternalServerErrorMessage("Token is expired")
        except (jwt.exceptions.DecodeError, jwt.exceptions.InvalidSignatureError) as e:
            make_response().delete_cookie(
                "user_token", samesite="lax", secure=True, httponly=False
            )
            InternalServerErrorMessage("Token is invalid")
        except PyMongoError as e:
            InternalServerErrorMessage(e._message)
        except Exception as e:
            InternalServerErrorMessage(e)

    def add_tv(self):
        try:
            formMovie = request.form
            movie = self.__db["phimles"].find_one({"id": int(formMovie["id"])})
            tv = self.__db["phimbos"].find_one({"id": int(formMovie["id"])})
            if movie == None and tv == None:
                self.__db["phimbos"].insert_one(
                    {
                        "id": int(formMovie["id"]),
                        "name": formMovie["name"],
                        "original_name": formMovie["original_name"],
                        "original_language": formMovie["original_language"],
                        "poster_path": formMovie["poster_path"],
                        "backdrop_path": formMovie["backdrop_path"],
                        "first_air_date": formMovie["first_air_date"],
                        "last_air_date": formMovie["last_air_date"],
                        "genres": json.loads(formMovie["genres"]),
                        "overview": formMovie["overview"],
                        "episode_run_time": int(formMovie["episode_run_time"]),
                        "number_of_episodes": int(formMovie["number_of_episodes"]),
                        "status": formMovie["status"],
                        "views": 0,
                        "media_type": "tv",
                    },
                )
                return {"success": True, "result": "Add tv successfully"}
            else:
                return {
                    "success": False,
                    "already": True,
                    "result": "Tv is already exist",
                }

        except PyMongoError as e:
            InternalServerErrorMessage(e._message)
        except Exception as e:
            InternalServerErrorMessage(e)

    def edit_tv(self, id):
        try:
            formMovie = request.form

            tv = self.__db["phimbos"].find_one_and_update(
                {"id": str(id)},
                {
                    "$set": {
                        "name": formMovie["name"],
                        "original_name": formMovie["original_name"],
                        "original_language": formMovie["original_language"],
                        "first_air_date": formMovie["first_air_date"],
                        "last_air_date": formMovie["last_air_date"],
                        "genres": json.loads(formMovie["genres"]),
                        "overview": formMovie["overview"],
                        "episode_run_time": int(formMovie["episode_run_time"]),
                        "number_of_episodes": int(formMovie["number_of_episodes"]),
                        "views": int(formMovie["views"]),
                        "status": formMovie["status"],
                    },
                },
                return_document=ReturnDocument.AFTER,
            )
            return {
                "success": True,
                "result": cvtJson(tv),
                "message": "Edit tv successfully",
            }
        except PyMongoError as e:
            InternalServerErrorMessage(e._message)
        except Exception as e:
            InternalServerErrorMessage(e)

    def update_view(self, id):
        try:
            tv_dumps = self.__db["tvs"].find_one({"id": str(id)})
            new_views = int(tv_dumps["views"]) + 1

            self.__db["tvs"].update_one(
                {"id": str(id)},
                {
                    "$set": {
                        "views": new_views,
                    },
                },
            )
            return {"success": True, "result": "Update views of tv successfully"}
        except PyMongoError as e:
            InternalServerErrorMessage(e._message)
        except Exception as e:
            InternalServerErrorMessage(e)
