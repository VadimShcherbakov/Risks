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
