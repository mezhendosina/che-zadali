"""
This file works with homework received from https://sgo.edu-74.ru/
"""
from datetime import datetime, timedelta
from typing import Union, Any

import os
import psycopg2
import pytz
from bs4 import BeautifulSoup
from isoweek import Week

# global variables
connection = psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require')
cursor = connection.cursor()  # connect to database


def months(month: int):
    """This function compare month name with his number"""
    return {
        'дек.': 12, 'янв.': 1, 'февр.': 2,
        'мар.': 3, 'апр.': 4, 'мая': 5,
        'июн.': 6, 'июл.': 7, 'авг.': 8,
        'сент.': 9, 'окт.': 10, 'нояб.': 11
    }[month]


def new_old() -> list:
    date = datetime.now(pytz.timezone('Asia/Yekaterinburg'))
    cursor.execute(
        f"SELECT * FROM homeworktable WHERE daynum={date.strftime('%d')} AND daymonth={date.strftime('%m')} AND dayyear={date.strftime('%Y')};")
    return cursor.fetchall()


def extract_homework(code: str) -> bool:
    """This function parses code in search homework and delete old homework"""

    soup, old_list = BeautifulSoup(code, features='lxml'), new_old()
    schoolJournal = soup.find('div', 'schooljournal_content column')
    dayTable = schoolJournal.find_all('div', class_='day_table')
    for i in dayTable:
        day = i.find('span', 'ng-binding').get_text()
        dayNum = int(day.split(' ')[1])
        dayMonth = months(day.split(' ')[2])
        dayYear = int(day.split(' ')[3])

        for a in i.find_all('tr', class_='ng-scope'):
            try:
                lesson = a.find('a', class_='subject ng-binding ng-scope').get_text()
                try:
                    homework = a.find('a', class_='ng-binding ng-scope').get_text()
                except AttributeError:
                    continue
                cursor.execute('SELECT day, lesson, homework, dayNum, dayMonth, dayYear FROM homeworktable')
                table = cursor.fetchall()
                try:
                    assert (day, lesson, homework, dayNum, dayMonth, dayYear) in table
                except AssertionError:
                    date = datetime.now(pytz.timezone('Asia/Yekaterinburg')).strftime('%Y.%m.%d %H:%M:%S')
                    cursor.execute(
                        f"INSERT INTO homeworktable VALUES('{day}', '{lesson}', '{homework}', {dayNum}, {dayMonth}, {dayYear}, '{date}') "
                    )
                    continue
            except AttributeError as e:
                continue
    connection.commit()

    true_false = new_old()
    if old_list != true_false:
        return True
    else:
        return False


def select_homework(day=1, new: bool = False, channel=False) -> Union[str, list[Union[str, list[Any]]]]:
    """This function collect homework day(1 - tommorow, 0 - today, -1 - yesterday, 'all_week' - homework on week) """
    global homework_result

    def select(day, month, year) -> list:
        cursor.execute(
            'SELECT lesson, homework, postDate FROM homeworktable WHERE daynum=%s and daymonth=%s and dayYear=%s;',
            (day, month, year)
        )
        return cursor.fetchall()

    if day == 'all_week':
        homework, r, date = '', '', datetime.now(pytz.timezone('Asia/Yekaterinburg'))

        if date.strftime('%w') == '0':
            date = datetime.now(pytz.timezone('Asia/Yekaterinburg')) + timedelta(days=1)
        week = date.isocalendar()[1]
        mon, sun = Week(date.year, week).monday(), Week(date.year, week).sunday()
        cursor.execute(
            f'SELECT dayNum, lesson, homework, postDate FROM homeworktable WHERE dayNum >={mon.strftime("%d")} AND dayNum <={sun.strftime("%d")} AND dayMonth >= {mon.strftime("%m")} AND dayMonth <= {sun.strftime("%m")} AND dayyear BETWEEN {mon.strftime("%Y")} AND {sun.strftime("%Y")};'
        )
        result = cursor.fetchall()
        cursor.execute(
            f'SELECT day, dayNum FROM homeworktable WHERE dayNum >={mon.strftime("%d")} AND dayNum <={sun.strftime("%d")} AND dayMonth >= {mon.strftime("%m")} AND dayMonth <= {sun.strftime("%m")} AND dayyear BETWEEN {mon.strftime("%Y")} AND {sun.strftime("%Y")};'
        )
        day = cursor.fetchall()
        for i in day:
            homework = homework + f'<i>{i[0]}</i>\n'
            for a in result:
                if a[0] == i[1]:
                    homework = homework + f'<b>{a[1]}</b><i>(добавлено {datetime.strptime(a[3], "%Y.%m.%d %H:%M:%S").strftime("%H:%M %d.%m.%Y")})</i>: {a[2]}\n'
        return homework

    if datetime.now(pytz.timezone('Asia/Yekaterinburg')).strftime('%w') == '6':
        date = datetime.now(pytz.timezone('Asia/Yekaterinburg')) + timedelta(days=2)
    else:
        date = datetime.now(pytz.timezone('Asia/Yekaterinburg')) + timedelta(days=int(day))

    try:
        homework = select(
            int(date.strftime(' %d').replace(' 0', '')),
            int(date.strftime(' %m').replace(' 0' '')),
            date.strftime('%Y')
        )
    except TypeError:
        homework = select(date.strftime('%d'), date.strftime('%m'), date.strftime('%Y'))

    d = date.strftime('%d.%m.%Y')
    if new:
        homework_result = f'Появилась новое д\з на <i>{d}</i>:\n' + '\n'.join(
            map(lambda
                    x: f'<b>{x[0]}</b> <i>(добавлено в {datetime.strptime(x[2], "%Y.%m.%d %H:%M:%S").strftime("%H:%M %d.%m.%Y")})</i>:  {x[1]}',
                homework))
    else:
        homework_result = f'Домашнее задание на <i>{d}</i>\n' + '\n'.join(
            map(lambda
                    x: f'<b>{x[0]}</b> <i>(добавлено в {datetime.strptime(x[2], "%Y.%m.%d %H:%M:%S").strftime("%H:%M %d.%m.%Y")})</i>:  {x[1]}',
                homework))

    if channel:
        homework_result = f'Домашнее задание на <i>{d}</i>:\n' + '\n'.join(
            map(lambda
                    x: f'<b>{x[0]}</b> <i>(добавлено в {datetime.strptime(x[2], "%Y.%m.%d %H:%M:%S").strftime("%H:%M %d.%m.%Y")})</i>:  {x[1]}',
                homework))

    return homework_result
    # attachment, date = [], datetime.now() + timedelta(days=-7)
    # headers = {'Accept': 'application/json', 'Authorization': f'OAuth {os.getenv("YDISK_TOKEN")}'}
    # r = requests.get('https://cloud-api.yandex.net/v1/disk/resources?path=%2Fche-zadali_files', headers=headers).json()
    #
    # for i in r['_embedded']['items']:
    #     if i['name'] == d:
    #         for a in \
    #                 requests.get(
    #                     f'https://cloud-api.yandex.net/v1/disk/resources?path=%2Fche-zadali_files%2F{i["name"]}',
    #                     headers=headers).json()['_embedded']['items']:
    #             l = y.get_download_link(f'/che-zadali_files/{i["name"]}/{a["name"]}')
    #             attachment.append(l)
    #     elif int(i['name'].split('.')[0]) < int(date.strftime('%d')) and int(i['name'].split('.')[1]) < int(
    #             date.strftime('%m')):
    #         y.remove(f'/che-zadali_files/{i["name"]}')
