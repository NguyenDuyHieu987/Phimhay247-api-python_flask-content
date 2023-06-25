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
            extraValue = {}

            if append_to_response != "":
                if "images" in append_to_response.split(","):
                    # exceptValue.pop("images")
                    images = self.__db["images"].find_one({"id": str(id)})
                    extraValue["images"] = images["items"]
                if "credits" in append_to_response.split(","):
                    # exceptValue.pop("credits")
                    credits = self.__db["credits"].find_one({"id": str(id)})
                    extraValue["credits"] = credits["items"]
                if "videos" in append_to_response.split(","):
                    # exceptValue.pop("videos")
                    videos = self.__db["videos"].find_one({"id": str(id)})
                    extraValue["videos"] = videos["items"]

            # tv = self.__db["tvs"].find_one({"id": str(id)}, exceptValue)

            tv = self.__db["tvs"].find_one({"id": str(id)}) | extraValue

            headers = request.headers

            if "Authorization" not in headers:
                if tv != None:
                    return cvtJson(tv)
                else:
                    return {"not_found": True, "result": "Can not find the tv"}
            else:
                user_token = request.headers["Authorization"].replace("Bearer ", "")

                jwtUser = jwt.decode(
                    user_token,
                    str(os.getenv("JWT_TOKEN_SECRET")),
                    algorithms=["HS256"],
                )
                item_lists = self.__db["lists"].find_one(
                    {"id": jwtUser["id"]}, {"items": {"$elemMatch": {"id": str(id)}}}
                )

                if "items" in item_lists:
                    tv = tv | {"in_list": True}
                else:
                    tv = tv | {"in_list": False}

                item_watchlists = self.__db["watchlists"].find_one(
                    {"id": jwtUser["id"]}, {"items": {"$elemMatch": {"id": str(id)}}}
                )

                if "items" in item_watchlists:
                    tv = tv | {
                        "in_history": True,
                        "history_progress": {
                            "duration": item_watchlists["items"][0]["duration"],
                            "percent": item_watchlists["items"][0]["percent"],
                            "seconds": item_watchlists["items"][0]["seconds"],
                        },
                    }
                else:
                    tv = tv | {"in_history": False}

                rates = self.__db["rates"].find_one(
                    {
                        "user_id": jwtUser["id"],
                        "movie_id": str(id),
                        "movie_type": "tv",
                    }
                )

                if rates != None:
                    tv = tv | {
                        "is_rated": True,
                        "rated_value": rates["rate_value"],
                    }
                else:
                    tv = tv | {
                        "is_rated": False,
                    }

                return cvtJson(tv)

        except jwt.ExpiredSignatureError as e:
            InternalServerErrorMessage("Token is expired")
        except jwt.exceptions.DecodeError as e:
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
