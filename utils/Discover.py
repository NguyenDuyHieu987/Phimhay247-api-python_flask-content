from utils.JsonResponse import ConvertJsonResponse as cvtJson
from flask import *
from configs.database import Database


def discover_movie(db, release_date, genres, original_language, page, sort_by, limit):
    if sort_by != None:
        movie = cvtJson(
            db["movies"]
            .find(
                {
                    "$and": [
                        release_date,
                        genres,
                        original_language,
                    ]
                }
            )
            .skip(page * limit)
            .limit(limit)
            .sort(sort_by)
        )
        return movie
    else:
        movie = cvtJson(
            db["movies"]
            .find(
                {
                    "$and": [
                        release_date,
                        genres,
                        original_language,
                    ]
                }
            )
            .skip(page * limit)
            .limit(limit)
        )
        return movie


def discover_tv(db, first_air_date, genres, original_language, page, sort_by, limit):
    if sort_by != None:
        tv = cvtJson(
            db["tvs"]
            .find(
                {
                    "$and": [
                        first_air_date,
                        genres,
                        original_language,
                    ]
                }
            )
            .skip(page * limit)
            .limit(limit)
            .sort(sort_by)
        )
        return tv
    else:
        tv = cvtJson(
            db["tvs"]
            .find(
                {
                    "$and": [
                        first_air_date,
                        genres,
                        original_language,
                    ]
                }
            )
            .skip(page * limit)
            .limit(limit)
        )
        return tv
