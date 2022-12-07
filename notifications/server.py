import logging
import os
import time

import requests
from flask import Flask, request, abort

import config
from notifications.api import Api

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)


@app.route("/register_user", methods=["POST"])
async def register_user():
    request_json = request.get_json()
    api = Api()

    user_data = request_json.get("user_id") is None or request_json.get("firebase_token") is None \
                or request_json.get("login") is None or request_json.get("password")
    sgo_data = request_json.get("country_id") is None or request_json.get("sid") is None \
               or request_json.get("sid") is None or request_json.get("province_id") \
               or request_json.get("city_id") is None or request_json.get("sft") is None \
               or request_json.get("school_id") is None

    if user_data or sgo_data:
        abort(400)
        return 400

    api.register_user(
        request_json["user_id"],
        request_json["firebase_token"],
        request_json["login"],
        request_json["password"],
        request_json["host"],
        request_json["country_id"],
        request_json["sid"],
        request_json["province_id"],
        request_json["city_id"],
        request_json["sft"],
        request_json["school_id"],
    )
    api.close()
    logging.info(f"server: register user {request_json['user_id']}")
    return 200


@app.route("/unregister_user", methods=["POST"])
async def unregister_user():
    api = Api()
    request_json = request.get_json()

    if request_json.get("user_id") is None or request_json.get("firebase_token") is None:
        abort(400)
        return 400

    api.unregister_user(request_json["user_id"], request_json["firebase_token"])
    api.close()
    logging.info(f"server: unregister user {request_json['user_id']}")
    return 200


@app.route('/new_release', methods=['POST'])
async def json_example():
    try:
        s_time = time.time()

        url, apk_name = "", ""
        request_json = request.get_json()

        if request_json["action"] == "published":

            for i in request_json["release"]["assets"]:
                if i["content_type"] == "application/vnd.android.package-archive":
                    url = i["browser_download_url"]
                    apk_name = i["name"]

            download_apk = requests.get(url, stream=True)

            with open(apk_name, "wb") as fb:
                for chunk in download_apk.iter_content(chunk_size=1024):
                    fb.write(chunk)

            release_notes = f'<b>Доступна новая версия приложения: </b><i>{request_json["release"]["tag_name"]}</i>\n\n{request_json["release"]["body"]}'
            requests.post(
                f"https://api.telegram.org/bot{config.telegram_token}/sendMessage",
                data={
                    "chat_id": config.sgo_app_channel_id,
                    "text": release_notes,
                    "parse_mode": "HTML"
                }
            )
            with open(apk_name, "rb") as f:
                requests.post(
                    f"https://api.telegram.org/bot{config.telegram_token}/sendDocument",
                    files={'document': (apk_name, f)},
                    data={'chat_id': config.sgo_app_channel_id, 'disable_notification': True}
                )
            os.remove(apk_name)

        return str(time.time() - s_time)
    except BaseException as e:
        return str(e)
