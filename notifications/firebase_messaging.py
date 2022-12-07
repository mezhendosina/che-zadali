import sqlite3

import firebase_admin
from firebase_admin import credentials, messaging

import config

cred = credentials.Certificate("D:/Programming/Python/che-zadali/files/firebase.json")
firebase = firebase_admin.initialize_app(cred, name="che-zadali-app")


def send_message(token, lesson, grade):
    # android_config = messaging.AndroidConfig(
    #     priority=messaging.AndroidNotification.
    # )
    match grade:
        case "five":
            grade = 5
        case "four":
            grade = 4
        case "three":
            grade = 3
        case "two":
            grade = 2

    message = messaging.Message(
        notification=messaging.Notification(f"Новая оценка по предмету {lesson}",
                                            f"Замечена новая {grade} по премету {lesson}"),
        token=token
    )

    messaging.send(message, app=firebase)
