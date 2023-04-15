import pymongo
from pymongo.errors import PyMongoError
from utils.JsonResponse import ConvertJsonResponse as cvtJson
from utils.ErrorMessage import errorMessage
from flask import *
from pymongo import ReturnDocument

myclient = pymongo.MongoClient(
    "mongodb+srv://admin:hieusen123@the-movie-database.fczrzon.mongodb.net/Phimhay247_DB"
)

db = myclient["Phimhay247_DB"]


def detail_tv(id):
    try:
        append_to_response = request.args.get(
            "append_to_response", default="", type=str
        )
        exceptValue = {"images": 0, "credits": 0, "videos": 0}

        if append_to_response != "":
            if "images" in append_to_response.split(","):
                exceptValue.pop("images")
            if "credits" in append_to_response.split(","):
                exceptValue.pop("credits")
            if "videos" in append_to_response.split(","):
                exceptValue.pop("videos")

        tv = db["tvs"].find_one({"id": int(id)}, exceptValue)
        if tv != None:
            return cvtJson(tv)
        else:
            return {"not_found": True}

    except:
        return {}


def add_tv():
    try:
        formMovie = request.form
        movie = db["phimles"].find_one({"id": int(formMovie["id"])})
        tv = db["phimbos"].find_one({"id": int(formMovie["id"])})
        if movie == None and tv == None:
            db["phimbos"].insert_one(
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

    except:
        return {"success": False, "result": "Add tv failed"}


def edit_tv(id):
    try:
        formMovie = request.form

        tv = db["hieus"].find_one_and_update(
            {"id": int(id)},
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
    except:
        return {"success": False, "message": "Edit tv failed"}


def update_view_tv(id):
    try:
        tv_dumps = db["tvs"].find_one({"id": int(id)})
        new_views = int(tv_dumps["views"]) + 1

        db["tvs"].update_one(
            {"id": int(id)},
            {
                "$set": {
                    "views": new_views,
                },
            },
        )
        return {"success": True, "result": "Update views of tv successfully"}
    except:
        return {"success": False, "result": "Update views of tv failed"}
