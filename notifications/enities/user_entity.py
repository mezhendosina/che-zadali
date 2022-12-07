class User:
    def __init__(self,
                 user_id: str,
                 firebase_token: str,
                 login: str,
                 password: str,
                 host: str,
                 country_id: int,
                 sid: int,
                 province_id: int,
                 city_id: int,
                 sft: int,
                 school_id: int,
                 send_grades: bool,
                 grades: str
                 ):
        self.user_id = user_id
        self.firebase_token = firebase_token
        self.login = login
        self.password = password
        self.host = host
        self.country_id = country_id
        self.sid = sid
        self.province_id = province_id
        self.city_id = city_id
        self.sft = sft
        self.school_id = school_id
        self.send_grades = bool(send_grades)
        self.grades = grades

