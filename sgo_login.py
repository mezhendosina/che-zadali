import hashlib
from datetime import datetime, timedelta
import requests
import os

headers = {
    "Connection": "keep-alive",
    "Host": "sgo.edu-74.ru",
    "Referer": "https://sgo.edu-74.ru/",
    "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="100", "Microsoft Edge";v="100"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36 Edg/100.0.1185.50",
}


def extract_homework(homework: dict) -> str:
    # initialize return string and time at now
    time_now = datetime.now().strftime("%w")
    out = ""

    # choose correct timedelta
    if int(time_now) < 6:
        time_delta = 1
    else:
        time_delta = 2

    # time now + timedelta
    time = (datetime.now() + timedelta(days=time_delta)).strftime("%Y-%m-%dT00:00:00")

    # extract homework
    for week_day in homework["weekDays"]:
        if week_day["date"] == time:
            date = datetime.strptime(week_day["date"], "%Y-%m-%dT00:00:00")
            out = f"Домашнее задание на <i>{date.strftime('%d.%m.%y')}</i>:\n"
            for lessons in week_day["lessons"]:
                try:
                    homework = lessons["assignments"][0]["assignmentName"]
                    out += f"<b>{lessons['subjectName']}</b>: {homework}\n"
                except KeyError:
                    continue
    return out


def new_sgo_login():
    # init session
    session = requests.session()
    session.headers.update(headers)
    session.headers.update({"Origin": "https://sgo.edu-74.ru"})
    # import vars
    login = os.getenv("SGO_LOGIN")
    password = os.getenv("SGO_PASSWORD")

    # logindata request
    session.get("https://sgo.edu-74.ru/webapi/logindata")
    # getdata request
    get_data = session.post("https://sgo.edu-74.ru/webapi/auth/getdata")
    get_data_response = get_data.json()
    get_data_cookie = get_data.headers.get("set-cookie")

    # update cookies
    headers.update({"Cookie": get_data_cookie})
    session.cookies.update({"NSSESSIONID": get_data_cookie.split(";")[0][12:]})

    # password hashing
    pre_password = get_data_response["salt"] + hashlib.md5(password.encode("utf-8")).hexdigest()
    password = hashlib.md5(pre_password.encode("utf-8")).hexdigest()

    # prepare login data
    login_data = {
        "LoginType": "1",
        "cid": "2",
        'sid': "1",
        "pid": "-1",
        "cn": "1",
        "sft": "2",
        "scid": "89",
        "UN": login,
        "PW": password[:6],
        "lt": get_data_response["lt"],
        "pw2": password,
        "ver": get_data_response['ver']
    }
    # login request
    login_request = session.post("https://sgo.edu-74.ru/webapi/login", headers=headers, data=login_data)
    at = login_request.json()["at"]
    user_id = login_request.json()['accountInfo']["user"]["id"]
    session.headers.update({"at": at})

    # check security warning
    if login_request.json()["entryPoint"] == "/asp/SecurityWarning.asp":
        session.post("https://sgo.edu-74.ru/asp/SecurityWarning.asp")

    # calculate start/end week
    start_week = (datetime.now() - timedelta(days=datetime.now().isoweekday() % 7 - 1))
    end_week = start_week + timedelta(days=6)

    # update headers
    session.headers.update({"Referer": "https://sgo.edu-74.ru/angular/school/studentdiary/"})

    # find current year
    year_list = session.get("https://sgo.edu-74.ru/webapi/mysettings/yearlist").json()
    year_id = 0
    for i in year_list:
        if i["name"].find("(*) ") == -1:
            year_id = i["id"]

    # diary request
    diary_request = session.get(
        f"https://sgo.edu-74.ru/webapi/student/diary?studentId={user_id}&vers=1651144090014&weekEnd={end_week.strftime('%Y-%m-%d')}&weekStart={start_week.strftime('%Y-%m-%d')}&withLaAssigns=true&yearId={year_id}")

    session.post("https://sgo.edu-74.ru/asp/logout.asp", data={'at': login_request.json()['at']})
    session.close()
    return extract_homework(diary_request.json())
