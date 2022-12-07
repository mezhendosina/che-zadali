from datetime import datetime, timedelta

import pytz


class Homework:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = self.connection.cursor()

    def select_homework(self) -> str:
        """This function collect homework """

        def select(day, month, year) -> list:
            self.cursor.execute(
                f'SELECT lesson, homework FROM homework_table WHERE date_num={day} and date_month={month} and date_year={year};',

            )
            return self.cursor.fetchall()

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

    def extract_homework(self, homework: dict):
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

                        day_num = day.day
                        day_month = day.month
                        day_year = day.year

                        self.cursor.execute(
                            'SELECT lesson, homework, date_num, date_month, date_year FROM homework_table')
                        table = self.cursor.fetchall()
                        try:
                            assert (lesson, homework, day_num, day_month, day_year) in table
                        except AssertionError:
                            now = datetime.now(pytz.timezone('Asia/Yekaterinburg')).strftime('%Y.%m.%d %H:%M:%S')
                            self.cursor.execute(
                                f"INSERT INTO homework_table VALUES('{now}', '{lesson}', '{homework}', {day_num}, {day_month}, {day_year}) "
                            )
                            continue
                    except KeyError:
                        continue
        self.connection.commit()
