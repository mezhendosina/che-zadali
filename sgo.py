import hashlib
import json
import logging
from datetime import timedelta, datetime

import aiohttp
import psycopg2

import config
from homework import Homework


class SGO:
    def __init__(self):
        connection = psycopg2.connect(config.database_url, sslmode='require')  # init sql database

        self.lg = config.login
        self.password = config.password
        self.user_id = None
        self.session = None
        self.homework = Homework(connection)

    async def login(self):
        self.session = aiohttp.ClientSession(base_url=config.base_url, headers=config.headers)
        s = self.session
        get_data_resp = None
        logging.info("login_data")
        await s.get("/webapi/logindata")
        logging.info("get_data")
        async with s.post("/webapi/auth/getdata") as r:
            # save result
            get_data_resp = await r.json()

            # update cookies
            logging.info("set_cookies")
            get_cookies = r.headers.get("set-cookie")
            s.headers.update({"Cookie": get_cookies})
            s.cookie_jar.update_cookies({"NSSESSIONID": get_cookies.split(";")[0][12:]})

        if get_data_resp is not None:
            logging.info("hash_password")
            hash_password = self.hash_password(get_data_resp.get("salt"))
            login_data = self.setup_login_data(get_data_resp, hash_password)

            logging.info("logging")
            async with s.post("/webapi/login", data=login_data) as r:
                json_response = await r.json()

                at = json_response["at"]
                s.headers.update({"at": at})
                self.user_id = json_response["accountInfo"]["user"]["id"]

    async def get_homework(self):
        if self.session is None:
            return
        await self.login()

        # calculate start/end week
        datetime_now = datetime.now()
        start_week = (datetime_now - timedelta(days=datetime.now().isoweekday() % 7 - 1))

        if datetime_now.isoweekday() == 6:
            start_week = datetime_now + timedelta(days=2)
        elif datetime_now.isoweekday() == 7:
            start_week = datetime_now + timedelta(days=1)

        end_week = start_week + timedelta(days=6)

        s = self.session
        s.headers.update({"Referer": "angular/school/studentdiary/"})
        # find current year
        async with s.get("/webapi/mysettings/yearlist") as r:
            year_list = await r.json()

            year_id = 0
            for i in year_list:
                if i["name"].find("(*) ") == -1:
                    year_id = i["id"]

        if self.user_id is not None:
            diary_request = await s.get(
                f"/webapi/student/diary?studentId={self.user_id}&vers=1651144090014&weekEnd={end_week.strftime('%Y-%m-%d')}&weekStart={start_week.strftime('%Y-%m-%d')}&withLaAssigns=true&yearId={year_id}")
            await self.logout()
            json_response = await diary_request.json()

            self.homework.extract_homework(json_response)
        else:
            await self.logout()

    async def logout(self):
        if self.session is None:
            return
        at = self.session.headers.get("at")
        await self.session.post("/asp/logout.asp", data={"at": at})
        await self.session.close()

    def hash_password(self, salt: str) -> str:
        password_md5 = hashlib.md5(self.password.encode("utf-8")).hexdigest()
        pre_password = salt + password_md5
        return hashlib.md5(pre_password.encode("utf-8")).hexdigest()

    def setup_login_data(self, get_data_response, hash_password) -> dict:
        return {
            "LoginType": "1",
            "cid": "2",
            'sid': "1",
            "pid": "-1",
            "cn": "1",
            "sft": "2",
            "scid": "89",
            "UN": self.lg,
            "PW": hash_password[:6],
            "lt": get_data_response["lt"],
            "pw2": hash_password,
            "ver": get_data_response['ver']
        }
