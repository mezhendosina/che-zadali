from datetime import datetime

import psycopg2
import pytz


class PToday:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()

    def set_prev_p(self):
        cursor = self.cursor
        connection = self.connection

        cursor.execute("SELECT * FROM current_duty")
        current_duty = cursor.fetchall()[0]
        if current_duty[0] == 0:
            a = 14
        else:
            a = current_duty[0] - 1
        cursor.execute(f"UPDATE current_duty SET id = {a}")
        connection.commit()

    def set_next_p(self):
        cursor = self.cursor
        connection = self.connection

        cursor.execute("SELECT * FROM current_duty")
        current_duty = cursor.fetchall()[0]
        if current_duty[0] > 14:
            a = 1
        else:
            a = current_duty[0] + 1
        cursor.execute(f"UPDATE current_duty SET id = {a}")
        connection.commit()

    def current_p(self) -> str:
        """Getting class attendants for today"""
        return "@mezhendosina потерял табличку с дежурными :(\nПомогите Жене найти табличку"
        # cursor = self.cursor
        # connection = self.connection
        #
        # cursor.execute("SELECT * FROM current_duty")
        # time_now = datetime.now(pytz.timezone('Asia/Yekaterinburg'))
        # current_duty = cursor.fetchall()[0]
        # if time_now.strftime("%d.%m.%Y") > current_duty[1] and 0 < int(time_now.strftime("%w")) < 6:
        #     # get attendant ID
        #     a = current_duty[0] + 1
        #
        #     if current_duty[0] >= 14:
        #         a = 1
        #
        #     cursor.execute(f"UPDATE current_duty SET id = {a}, date = '{time_now.strftime('%d.%m.%Y')}'")
        #     connection.commit()
        #     cursor.execute(f"SELECT people FROM duty WHERE id = {a}")
        # else:
        #     cursor.execute(f"SELECT people FROM duty WHERE id = {current_duty[0]}")
        # b = cursor.fetchall()[0][0].split(',')
        # return f'<b>{b[0]}\n{b[1]}</b>'
