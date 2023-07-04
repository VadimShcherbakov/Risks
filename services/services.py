"""Вспомогательные скрипты"""

import json


def read_json(filename: str):
    """Функция для чтения файла json"""
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)


def get_num_axes(need_axes: int, end_axes) -> str:
    """
    :param need_axes: принимает на вход выбранную ось
    :param end_axes: принимает на вход последнюю ось для данного подразделения
    :return: если на вход принимается ось 23 (всего в цеху 34), то возвращает 23-24
    если на вход принимается ось 34 (всего в цеху 34), то возвращает 33-34
    """
    need_axes_1 = need_axes
    need_axes_2 = need_axes + 1
    if need_axes_2 > end_axes:
        need_axes_1 -= 1
        need_axes_2 -= 1
    return f'{need_axes_1}-{need_axes_2}'


def significance_level(val: int) -> str:
    """Возвращает классификатор риска согласно значению val"""
    if 1 <= val <= 5:
        return 'малый'
    if 6 <= val <= 16:
        return 'существенный (средний)'
    if 20 <= val <= 25:
        return 'высокий'


def get_region(axes: str, rows: str, description: str, *args: list) -> str:
    """
    :param axes: получает необходимые оси, например 1-2
    :param rows: получает необходимые ряды, например А-Б
    :param description: описание места возникновения риска
    :param args: принимает словарь допустимых осей для данного цеха, например [1,34]
    :return: возвращает f строку отформатированную под необходимый формат
    """
    if len(axes) and len(rows) > 0:
        return f"ряд {rows}, ось {get_num_axes(int(axes), args[-1])}, {description}"
    return description

def write_from_excel_to_sql_zone():
    """Вспомогательный скрипт для записи номера зоны из excel в sql"""
    from peewee import SqliteDatabase
    from model import Zone
    import pandas as pd

    db = SqliteDatabase('data/risks.db')
    Zone.create_table()
    df = pd.read_excel('data/dk_zone.xlsx')
    for i in df.index:
        print(i)
        Zone.create(
                num_zone=int(df.loc[i, 'num_zone']),
                description_zone=(df.loc[i, 'description_zone']).strip()
                )


def write_from_json_to_sql():
    """Вспомогательный скрипт для записи из json в sql"""
    from peewee import SqliteDatabase
    from model import TypeRisk
    class_dangerous = read_json('data/class.json')
    db = SqliteDatabase('data/risks.db')
    TypeRisk.create_table()
    for v in class_dangerous:
        for i in class_dangerous[v]:
            my_list = i.split()
            num = my_list[0]
            description = " ".join(my_list[1:])
            print(num, description)
            TypeRisk.create(
                            clas_dangerous_id=num.strip(),
                            description_clas_dangerous=description.strip()
                            )


def write_from_excel_to_sql_risk():
    """Вспомогательный скрипт для записи всех выявленных рисков из excel в sql"""
    from peewee import SqliteDatabase
    from model import Risk
    import pandas as pd

    db = SqliteDatabase('data/risks.db')
    Risk.create_table()
    df = pd.read_excel('data/dk_risk.xlsx')
    for i in df.index:
        print(i)
        Risk.create(
                num_zone = int(df.loc[i, 'num_zone']),
                region = df.loc[i, 'region'].strip(),
                rows = df.loc[i, 'rows'],
                axes = df.loc[i, 'axes'],
                level = int(df.loc[i, 'level']),
                clas_dangerous = df.loc[i, 'clas_dangerous'].strip(),
                date_of_detection =df.loc[i, 'date_of_detection'],
                owner_risk = df.loc[i, 'owner_risk'].strip(),
                description_risk = df.loc[i, 'description_risk'].strip(),
                before_severity_assessmentinput = int(df.loc[i, 'before_severity_assessmentinput']),
                before_probability_estimation = int(df.loc[i, 'before_probability_estimation']),
                before_grade = int(df.loc[i, 'before_grade']),
                before_significance_level = df.loc[i, 'before_significance_level'].strip(),
                photo_before = df.loc[i, 'photo_before'].strip(),
                count_entries = int(df.loc[i, 'count_entries'])
                )


def write_from_excel_to_sql_event():
    """Вспомогательный скрипт для записи всех выявленных рисков из excel в sql"""
    from peewee import SqliteDatabase
    from model import EventRisk
    import pandas as pd

    db = SqliteDatabase('data/risks.db')
    EventRisk.create_table()
    df = pd.read_excel('data/dk_event.xlsx')
    for i in df.index:
        print(i)
        EventRisk.create(
                unique_number_id=df.loc[i, 'unique_number_id'].strip(),
                num_risk=int(df.loc[i, 'num_risk']),
                elimination_measures=df.loc[i, 'elimination_measures'].strip(),
                expected_result=df.loc[i, 'expected_result'].strip(),
                period_of_execution=df.loc[i, 'period_of_execution'],
                responsible_for_implementation=df.loc[i, 'responsible_for_implementation'].strip(),
                num_event_number=int(df.loc[i, 'num_event_number']),
                weeks_eliminate=int(df.loc[i, 'weeks_eliminate'])
                )


def write_from_excel_to_sql_done():
    """Вспомогательный скрипт для записи только выполненных рисков из excel в sql"""
    from peewee import SqliteDatabase
    from model import DoneRisk
    import pandas as pd

    db = SqliteDatabase('data/risks.db')
    DoneRisk.create_table()
    df = pd.read_excel('data/dk_done.xlsx')
    for i in df.index:
        print(i)
        DoneRisk.create(
                unique_number_id=df.loc[i, 'unique_number'].strip(),
                num_risk=int(df.loc[i, 'num_risk']),
                status=df.loc[i, 'status'].strip(),
                explanations=df.loc[i, 'explanations'].strip(),
                after_severity_assessmentinput=int(df.loc[i, 'after_severity_assessmentinput']),
                after_probability_estimation=int(df.loc[i, 'after_probability_estimation']),
                after_grade=int(df.loc[i, 'after_grade']),
                after_significance_level=df.loc[i, 'after_significance_level'].strip(),
                photo_after=df.loc[i, 'photo_after'],
                date_elimination=df.loc[i, 'date_elimination']
                )


# write_from_excel_to_sql_zone()
# write_from_json_to_sql()
# write_from_excel_to_sql_risk()
# write_from_excel_to_sql_event()
# write_from_excel_to_sql_done()