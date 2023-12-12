import pymongo
from pymongo.errors import PyMongoError
from flask import *
import requests
import os
from datetime import datetime, timezone, timedelta
import jwt
import uuid
from urllib.parse import urlencode
from configs.database import Database
from utils.JsonResponse import ConvertJsonResponse as cvtJson
from utils.ErrorMessage import BadRequestMessage, InternalServerErrorMessage


class Plan(Database):
    def __init__(self):
        self.__db = self.ConnectMongoDB()

    def plans(self):
        try:
            plans = cvtJson(
                self.__db["plans"].find().sort([("order", pymongo.ASCENDING)])
            )

            return {"results": plans}
        except PyMongoError as e:
            InternalServerErrorMessage(e._message)
        except Exception as e:
            InternalServerErrorMessage(e)

    def register(self, id):
        try:
            formUser = request.form

            user_token = request.headers["Authorization"].replace(
                "Bearer ", ""
            ) or request.cookies.get("user_token")

            jwtUser = jwt.decode(
                user_token,
                str(os.getenv("JWT_SIGNATURE_SECRET")),
                algorithms=["HS256"],
            )

            plan = self.__db["plans"].find_one({"id": id})

            method = request.form.get("method").upper()

            order_id = str(uuid.uuid4())

            if method == "MOMO":
                pass
            elif method == "ZALOPAY":
                pass
            elif method == "VNPAY":
                params = {
                    "vnp_Version": "2.1.0",
                    "vnp_Command": "pay",
                    "vnp_TmnCode": str(os.getenv("VNP_TMNCODE")),
                    "vnp_Amount": plan["price"] * 100,
                    "vnp_CurrCode": "VND",
                    "vnp_TxnRef": order_id,
                    "vnp_OrderInfo": f"Register subscription {plan['order']}: {plan['name']}",
                    "vnp_OrderType": formUser["order_type"]
                    if "order_type" in formUser
                    else "190003",
                    "vnp_Locale": formUser["language"]
                    if "language" in formUser
                    else "vn",
                    # "vnp_BankCode": formUser["bank_code"],
                    "vnp_CreateDate": datetime.now().strftime("%Y%m%d%H%M%S"),
                    "vnp_IpAddr": request.remote_addr,
                    "vnp_ReturnUrl": "https://phimhay247z.org",
                }

                encoded_params = urlencode(params)

                vnpay_payment_url = str(os.getenv("VNP_URL")) + "?" + encoded_params

                print(vnpay_payment_url)
                # return redirect(vnpay_payment_url)

                return {"url": vnpay_payment_url}

            elif method == "STRIPE":
                pass
            else:
                pass

            return {"results": plan}
        except PyMongoError as e:
            InternalServerErrorMessage(e._message)
        except Exception as e:
            InternalServerErrorMessage(e)

    def retrieve(self, method, id):
        try:
            plans = cvtJson(
                self.__db["plans"].find().sort([("order", pymongo.ASCENDING)])
            )

            return {"results": plans}
        except PyMongoError as e:
            InternalServerErrorMessage(e._message)
        except Exception as e:
            InternalServerErrorMessage(e)
