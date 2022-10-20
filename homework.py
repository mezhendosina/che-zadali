"""
This file works with homework received from https://sgo.edu-74.ru/
"""
import os
from datetime import datetime, timedelta

import psycopg2
import pytz

# global variables
connection = psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require')
cursor = connection.cursor()  # connect to database


def select_homework() -> str:
    """This function collect homework """
    global homework_result

    def select(day, month, year) -> list:
        cursor.execute(
            'SELECT lesson, homework, postDate FROM homeworktable WHERE daynum=%s and daymonth=%s and dayYear=%s;',
            (day, month, year)
        )
        return cursor.fetchall()

    if datetime.now(pytz.timezone('Asia/Yekaterinburg')).strftime('%w') == '6':
        date = datetime.now(pytz.timezone('Asia/Yekaterinburg')) + timedelta(days=2)
    else:
        date = datetime.now(pytz.timezone('Asia/Yekaterinburg')) + timedelta(days=1)

    try:
        homework = select(
            int(date.strftime(' %d').replace(' 0', '')),
            int(date.strftime(' %m').replace(' 0' '')),
            date.strftime('%Y')
        )
    except TypeError:
        homework = select(date.strftime('%d'), date.strftime('%m'), date.strftime('%Y'))

    d = date.strftime('%d.%m.%Y')

    homework_result = f'Домашнее задание на <i>{d}</i>\n' + '\n'.join(
        map(lambda x: f'<b>{x[0]}</b>:  {x[1]}', homework))

    return homework_result


def extract_homework(homework: dict):
    # initialize time at now
    time_now = datetime.now().strftime("%w")

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
            day = datetime.strptime(week_day["date"], "%Y-%m-%dT00:00:00")
            for lessons in week_day["lessons"]:
                try:
                    lesson = lessons["subjectName"]
                    homework = lessons["assignments"][0]["assignmentName"]

                    dayNum = day.day
                    dayMonth = day.month
                    dayYear = day.year

                    cursor.execute('SELECT lesson, homework, dayNum, dayMonth, dayYear FROM homeworktable')
                    table = cursor.fetchall()
                    try:
                        assert (lesson, homework, dayNum, dayMonth, dayYear) in table
                    except AssertionError:
                        now = datetime.now(pytz.timezone('Asia/Yekaterinburg')).strftime('%Y.%m.%d %H:%M:%S')
                        cursor.execute(
                            f"INSERT INTO homeworktable VALUES('{now}', '{lesson}', '{homework}', {dayNum}, {dayMonth}, {dayYear}, '{day}') "
                        )
                        continue
                except KeyError:
                    continue
    connection.commit()
