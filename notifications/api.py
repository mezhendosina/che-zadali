import sqlite3

from firebase_admin import messaging

import config
from notifications.enities.user_entity import User


def tuple_to_user(user_tuple) -> User:
    return User(
        user_tuple[0],
        user_tuple[1],
        user_tuple[2],
        user_tuple[3],
        user_tuple[4],
        user_tuple[5],
        user_tuple[6],
        user_tuple[7],
        user_tuple[8],
        user_tuple[9],
        user_tuple[10],
        user_tuple[11],
        user_tuple[12]
    )


class Api:
    def __init__(self):
        self.connection = sqlite3.Connection(config.notifications_database_url)
        self.cursor = self.connection.cursor()

    def register_user(self,
                      user_id,
                      firebase_token,
                      login,
                      password,
                      host,
                      country_id,
                      sid,
                      province_id,
                      city_id,
                      sft,
                      school_id
                      ):
        self.cursor.execute(
            """INSERT INTO users (user_id, firebase_token, login, password, host, country_id, sid, province_id, city_id, sft, school_id, send_grades)"""
            f"""VALUES('{user_id}', '{firebase_token}', '{login}', '{password}','{host}', {country_id}, {sid}, {province_id}, {city_id}, {sft}, {school_id}, 1 );"""
        )

        self.connection.commit()

    def get_user(self, user_id) -> User:
        self.cursor.execute(f"SELECT * FROM users WHERE user_id={user_id}")
        out = self.cursor.fetchall()[0]
        return tuple_to_user(out)

    def get_all_users(self) -> list[User]:
        self.cursor.execute("SELECT * FROM users")
        user_list = self.cursor.fetchall()
        mapped_user_list = map(tuple_to_user, user_list)
        return list(mapped_user_list)

    def change_grades(self, user_id, grades):
        self.cursor.execute(f"UPDATE users SET grades = '{grades}' WHERE user_id= {user_id} ")
        self.connection.commit()

    def unregister_user(self, user_id, firebase_token):
        # TODO check user_id and firebase_token
        self.cursor.execute(f"DELETE FROM users WHERE user_id={user_id}")

    def close(self):
        self.connection.close()
