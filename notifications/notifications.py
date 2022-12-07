import asyncio
import json

from notifications.firebase_messaging import send_message
from notifications.grades import extract_grades
from sgo import SGO


def find_element(l: list, find: str):
    for i in l:
        if i["filterId"] == find:
            return i


def find_grade_change(old_grades, new_grades):
    for old_grade in old_grades:
        for new_grade in new_grades:
            if new_grade != old_grade:
                lesson = new_grade["lesson_name"]
                for grade in "five", "four", "three", "two":
                    if new_grade[f"count_{grade}"] > old_grade[f"count_{grade}"]:
                        return [lesson, grade, new_grade[f"count_{grade}"] - old_grade[f"count_{grade}"]]


async def check_grades(user) -> dict | None:
    sgo = SGO(user)

    get_parent_inf_letter = await sgo.get_parent_info_letter()
    if get_parent_inf_letter is None:
        return

    pclid = find_element(get_parent_inf_letter["filterSources"], "PCLID")["defaultValue"]
    term_id = find_element(get_parent_inf_letter["filterSources"], "TERMID")["defaultValue"]
    sid = find_element(get_parent_inf_letter["filterSources"], "SID")["defaultValue"]
    get_grades = await sgo.get_grades(
        pclid,
        "1",
        term_id,
        sid,
    )

    return extract_grades(get_grades)


async def scan_new_grades(api, user):
    new_grades = await check_grades(user)

    if user.grades is None:
        api.change_grades(user.user_id, json.dumps(new_grades))
        return

    old_grades = json.loads(user.grades)
    if new_grades != old_grades and new_grades is not None and user.grades is not None:
        get_changed_grade = find_grade_change(old_grades, new_grades)
        send_message(user.firebase_token, get_changed_grade[0], get_changed_grade[1])
        api.change_grades(user.user_id, new_grades)
