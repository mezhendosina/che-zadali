import hashlib


def password_hash(password: str, salt: str) -> str:
    password_md5 = hashlib.md5(password.encode("utf-8")).hexdigest()
    pre_password = salt + password_md5
    return hashlib.md5(pre_password.encode("utf-8")).hexdigest()


def setup_login_data(login, get_data_response, password) -> dict:
    return {
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


def cookies_to_header_str(cookies) -> str:
    out_s = ""
    for i in cookies.values():
        out_s += str(i).split(": ")[1] + ";"
    return out_s
