import hashlib
import datetime
import requests
import time

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
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/100.0.4896.127 Safari/537.36 Edg/100.0.1185.50",
}


def new_sgo_login():
    session = requests.session()
    session.headers.update(headers)

    session.headers.update({"Origin": "https://sgo.edu-74.ru"})
    # get NSSESSIONID
    session.get("https://sgo.edu-74.ru/webapi/logindata")

    # get salt, ver and lt
    get_data = session.post("https://sgo.edu-74.ru/webapi/auth/getdata")
    get_data_response = get_data.json()

    # preparing password
    pre_password = get_data_response["salt"] + hashlib.md5("285639".encode("utf-8")).hexdigest()
    password = hashlib.md5(pre_password.encode("utf-8")).hexdigest()

    login_data = {
        "LoginType": "1",
        "cid": "2",
        'sid': "1",
        "pid": "-1",
        "cn": "1",
        "sft": "2",
        "scid": "89",
        "UN": "МеньшенинЕ1",
        "PW": password[:6],
        "lt": get_data_response["lt"],
        "pw2": password,
        "ver": get_data_response['ver']
    }
    login_request = session.post("https://sgo.edu-74.ru/webapi/login", headers=headers, data=login_data)

    # get at and user_id for homework request
    at = login_request.json()["at"]
    user_id = login_request.json()['accountInfo']["user"]["id"]
    session.headers.update({"at": at})

    # passing security warning
    if login_request.json()["entryPoint"] == "/asp/SecurityWarning.asp":
        session.post("https://sgo.edu-74.ru/asp/SecurityWarning.asp")

    start_week = (datetime.datetime.now() - datetime.timedelta(days=datetime.datetime.now().isoweekday() % 7 - 1))
    end_week = start_week + datetime.timedelta(days=6)

    # update header
    session.headers.update({"Referer": "https://sgo.edu-74.ru/angular/school/studentdiary/"})

    # get year_id
    year_list = session.get("https://sgo.edu-74.ru/webapi/mysettings/yearlist").json()
    year_id = 0
    for i in year_list:
        if i["name"].find("(*) ") == -1:
            year_id = i["id"]

    # # get homework
    # diary_request = session.get(
    #     f"https://sgo.edu-74.ru/webapi/student/diary?studentId={user_id}&weekEnd=2022-04-30&weekStart=2022-04-30&withLaAssigns=true&yearId={year_id}")

    print(session.post("https://sgo.edu-74.ru/angular/school/mysettings/").content)

    # logout
    session.post("https://sgo.edu-74.ru/asp/logout.asp", data={'at': login_request.json()['at']})
    session.close()

    # return diary_request.json()


new_sgo_login()