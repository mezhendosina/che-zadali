import logging
from datetime import timedelta, datetime

import aiohttp
import psycopg2
from yarl import URL

import config as config
from bot.homework import Homework
from notifications.enities.user_entity import User
from sgo_utils import setup_login_data, password_hash, cookies_to_header_str


class SGO:
    def __init__(self, user: User = config.user):
        self.connection = psycopg2.connect(config.bot_database_url)  # init sql database
        self.lg = user.login
        self.password = user.password
        self.user_id = user.user_id
        self.base_url = user.host
        self.session = aiohttp.ClientSession(base_url=user.host, headers=config.headers)
        self.homework = Homework(self.connection)

    async def login(self):
        self.session = aiohttp.ClientSession(base_url=self.base_url, headers=config.headers)
        s = self.session
        logging.debug("login_data")
        await s.get("/webapi/logindata")
        logging.debug("get_data")
        async with s.post("/webapi/auth/getdata") as r:
            # save result
            get_data_resp = await r.json()

            # update cookies
            logging.debug("set_cookies")
            get_cookies = r.headers.get("set-cookie")
            s.headers.update({"Cookie": get_cookies})
            s.cookie_jar.update_cookies({"NSSESSIONID": get_cookies.split(";")[0][12:]})

        if get_data_resp is not None:
            logging.debug("hash_password")
            hash_password = password_hash(self.password, get_data_resp.get("salt"))
            login_data = setup_login_data(self.lg, get_data_resp, hash_password)

            logging.debug("logging")
            logging.debug(s.headers)
            async with s.post("/webapi/login", data=login_data) as r:
                json_response = await r.json()
                logging.debug(await r.text())
                at = json_response["at"]
                s.headers.update({"at": at})
                cookies = s.cookie_jar.filter_cookies(URL(config.user.host))
                self.session.headers.update({"Cookie": cookies_to_header_str(cookies)})

                self.user_id = json_response["accountInfo"]["user"]["id"]
                logging.debug("Logged in")
                return

    async def get_homework(self):
        if self.session is None:
            return
        await self.login()

        # calculate start/end week
        logging.debug("Calculate weeks")
        datetime_now = datetime.now()
        start_week = (datetime_now - timedelta(days=datetime.now().isoweekday() % 7 - 1))

        if datetime_now.isoweekday() == 6:
            start_week = datetime_now + timedelta(days=2)
        elif datetime_now.isoweekday() == 7:
            start_week = datetime_now + timedelta(days=1)

        end_week = start_week + timedelta(days=6)

        logging.debug("prepare request")
        s = self.session
        # find current year
        logging.debug("year request")
        async with s.get("/webapi/mysettings/yearlist") as r:
            year_list = await r.json()

            year_id = 0
            for i in year_list:
                if i["name"].find("(*) ") == -1:
                    year_id = i["id"]

        logging.debug("hoemework request")
        if self.user_id is not None:
            diary_request = await s.get(
                f"/webapi/student/diary?studentId={self.user_id}&vers=1651144090014&weekEnd={end_week.strftime('%Y-%m-%d')}&weekStart={start_week.strftime('%Y-%m-%d')}&withLaAssigns=true&yearId={year_id}")
            await self.logout()
            json_response = await diary_request.json()

            self.homework.extract_homework(json_response)
        else:
            await self.logout()

    async def get_parent_info_letter(self):
        await self.login()

        if self.session is None:
            return
        else:
            s = self.session
        headers = s.headers
        headers.update({"Referer": f"{self.base_url}/angular/school/reports/"})
        form_data = {
            "at": s.headers.get("at"),
            "RPNAME": "Информационное письмо для родителей",
            "RPTID": "ParentInfoLetter"
        }

        await s.post("/asp/Reports/ReportParentInfoLetter.asp", headers=headers, data=form_data)
        async with s.get("/webapi/reports/parentinfoletter") as r:
            return await r.json()

    async def get_grades(
            self,
            pclid,
            report_type,
            term_id,
            sid,
            login_type="0",
            pp="/asp/Reports/ReportParentInfoLetter.asp",
            back="/asp/Reports/ReportParentInfoLetter.asp",
            thm_id="",
            rptid="ParentInfoLetter",
            a="",
            na="",
            ta="",
            rt="",
            rp="",
            dt_week="",
    ) -> str | None:
        if self.session is None:
            return
        else:
            s = self.session

        at = self.session.headers.get("at")
        form_data = {
            "LoginType": login_type,
            "AT": at,
            "PP": pp,
            "BACK": back,
            "ThmID": thm_id,
            "RPTID": rptid,
            "A": a,
            "NA": na,
            "RP": rp,
            "TA": ta,
            "RT": rt,
            "dtWeek": dt_week,
            "PCLID": pclid,
            "ReportType": report_type,
            "TERMID": term_id,
            "SID": sid
        }
        async with s.post("/asp/Reports/ParentInfoLetter.asp", data=form_data) as r:
            await self.logout()
            return await r.text()

    async def logout(self):
        if self.session is None:
            return
        at = self.session.headers.get("at")
        await self.session.post("/asp/logout.asp", data={"at": at})

    async def close(self):
        await self.session.close()
        self.connection.close()
