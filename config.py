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

base_url = "https://sgo.edu-74.ru"
database_url = os.getenv('DATABASE_URL')
telegram_token = os.getenv("TELEGRAM_API_TOKEN")

admin_id = 401311369
login = os.getenv("SGO_LOGIN")
password = os.getenv("SGO_PASSWORD")
school_id = os.getenv("SCHOOL_ID")

you_have_not_power_here_gif = "CgACAgIAAxkBAAIB_GJnx90AAaCKoY1VyIimxr-tEfj4SAACrgsAAjCpCUibArTOkV6_lCQE"
