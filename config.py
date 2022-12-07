import os

from notifications.enities.user_entity import User

user = User(
    "",
    "",
    os.getenv("SGO_LOGIN"),
    os.getenv("SGO_PASSWORD"),
    "https://sgo.edu-74.ru",
    2,
    1,
    -1,
    1,
    2,
    89,
    True,
    {}
)
headers = {
    "Connection": "keep-alive",
    # "Host": user.user_id.replace("https://", ""),
    "Referer": user.host + "/",
    # "Origin": user.host,
    "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="100", "Microsoft Edge";v="100"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36 Edg/100.0.1185.50",
}

bot_database_url = os.getenv("BOT_DATABASE")
notifications_database_url = os.getenv("NOTIFICATIONS_DATABASE")
telegram_token = os.getenv("TELEGRAM_API_TOKEN")

admin_id = 401311369
sgo_app_channel_id = -1001621609379

you_have_not_power_here_gif = "CgACAgIAAxkBAAIB_GJnx90AAaCKoY1VyIimxr-tEfj4SAACrgsAAjCpCUibArTOkV6_lCQE"
