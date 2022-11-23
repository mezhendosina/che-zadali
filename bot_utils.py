from datetime import datetime

import psycopg2
import pytz
from telebot.async_telebot import AsyncTeleBot
from p_today import PToday


class BotUtils:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.p_today = PToday(connection)

    def report_activity(self, message):
        """Log user activity into database"""
        cursor = self.cursor
        connection = self.connection

        date = datetime.now(pytz.timezone('Asia/Yekaterinburg')).strftime('%Y.%m.%d %H:%M:%S')
        cursor.execute(
            f"INSERT INTO stats VALUES({message.from_user.id}, '{message.from_user.username}', '{message.text}', '{date}')")
        connection.commit()
