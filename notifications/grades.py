from bs4 import BeautifulSoup


def extract_grades(html: str) -> list | None:
    soup = BeautifulSoup(html, features="lxml")
    grades = []

    if html is None:
        return

    get_table_tag = soup.find_all("table", class_="table-print")[0]

    tr_tags = get_table_tag.find_all("tr")[2:-1]
    for i in tr_tags:
        td_tags = i.find_all("td")

        lesson_name = td_tags[0].string
        if td_tags[1].text == "\xa0":
            five_grade = 0
        else:
            five_grade = int(td_tags[1].text)

        if td_tags[2].text == "\xa0":
            four_grade = 0
        else:
            four_grade = int(td_tags[2].text)

        if td_tags[3].text == "\xa0":
            three_grade = 0
        else:
            three_grade = int(td_tags[3].text)

        if td_tags[4].text == "\xa0":
            two_grade = 0
        else:
            two_grade = int(td_tags[4].text)

        grades.append({"lesson_name": lesson_name,
                       "count_five": five_grade,
                       "count_four": four_grade,
                       "count_three": three_grade,
                       "count_two": two_grade
                       })
    return grades
