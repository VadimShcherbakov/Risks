"""Создание основного окна приложения для записи риска"""

import tkinter as tk
from tkinter import ttk
from lexicon.lexicon_ru import LEXICON_RU
from services.services import read_json, significance_level, get_region
from services.model import *
import datetime
from pandas.tseries.offsets import DateOffset

guide = read_json('data/guide.json')
class_dangerous = read_json('data/class_risk.json')

Risk.create_table()


def check_input(key_value, check_value):
    """Проверяет не пустой пользовательский ввод"""
    if len(check_value) > 0 and check_value[-1]:
        return check_value
    raise InputDataError(LEXICON_RU[key_value])


class InputDataError(Exception):
    """Класс для создания собственных ошибок"""
    def __init__(self, data):
        self.data = data

    def __str__(self):
        return repr(self.data)


class WriteNewRisk:
    """Создаём окно приложения для ввода описания риска"""
    frame = tk.Tk()
    frame.title(LEXICON_RU['name_table'])
    frame.geometry('720x600')

    def __init__(self):
        for c in range(3): WriteNewRisk.frame.columnconfigure(index=c, weight=1)
        for r in range(21): WriteNewRisk.frame.rowconfigure(index=r, weight=1)

    def create_another(self, class_risk: str, division: str, before_severity_assessmentinput: int,
                       before_probability_estimation: int) -> None:
        """ Функция, для создания оставшейся части окна приложения на основании выбора подразделения"""
        def get_all_date():
            """ Функция, которая забирает все данные после нажатия кнопки записать"""
            count_entries = 1 if before_grade < 6 else 2
            for i in range(count_entries):
                if i == 0:
                    elimination_measures = entry_elimination_measures_1.get()
                    period_of_execution = datetime.datetime.now().date() + \
                                          DateOffset(weeks=int(combo_period_of_execution_1.get()))
                    responsible_for_implementation = combo_responsible_for_implementation_1.get()
                    weeks_eliminate = combo_period_of_execution_1.get()
                    expected_result = entry_expected_result_1.get()
                else:
                    elimination_measures = entry_elimination_measures_2.get()
                    period_of_execution = datetime.datetime.now().date() + \
                                          DateOffset(weeks=int(combo_period_of_execution_2.get()))
                    responsible_for_implementation = combo_responsible_for_implementation_2.get()
                    weeks_eliminate = int(combo_period_of_execution_2.get())
                    expected_result = entry_expected_result_2.get()
                Risk(
                zone=division,
                num_zone=int(dict_division['num_division']),
                # order_num_risk = 2,
                # unique_number = 'CharField'
                region=get_region(
                                    combo_change_axes.get(),
                                    combo_change_rows.get(),
                                    entry_description.get(),
                                    *dict_division['axes']
                                    ),
                level=int(scale_level.get()),
                num_clas_dangerous=class_risk.split()[0],
                date_of_detection=datetime.datetime.now().date(),
                owner_risk=combo_change_owner_risk.get(),
                description_risk=entry_description.get(),
                before_severity_assessmentinput =before_severity_assessmentinput,
                before_probability_estimation =before_probability_estimation,
                before_grade=before_grade,
                before_significance_level=significance_level(before_grade),
                choosing_response_method='Устранение риска',
                source_of_funding='РП',
                # photo_before = 'CharField',
                expected_result=expected_result,
                # name_division='CharField',
                rows=combo_change_rows.get(),
                axes=combo_change_axes.get(),
                # risk_id = 'CharField',
                num_event_number=i+1,
                count_entries=count_entries,
                elimination_measures=elimination_measures,
                period_of_execution=period_of_execution,
                responsible_for_implementation=responsible_for_implementation,
                weeks_eliminate=weeks_eliminate
                ).save()

        dict_division = guide[division]
        before_grade = before_severity_assessmentinput * before_probability_estimation
        # ----------Создаём блок выбора рядов----------
        tk.Label(WriteNewRisk.frame, text=LEXICON_RU['change_rows']).grid(row=7, column=0, sticky='w')
        combo_change_rows = ttk.Combobox(WriteNewRisk.frame, values=(dict_division['rows']))
        combo_change_rows.grid(row=7, column=1, sticky='w')
        # ----------Создаём блок выбора осей----------
        tk.Label(WriteNewRisk.frame, text=LEXICON_RU['change_axes']).grid(row=8, column=0, sticky='w')
        combo_change_axes = ttk.Combobox(WriteNewRisk.frame, values=[i for i in range(dict_division['axes'][0], dict_division['axes'][1]+1)] if dict_division['axes'] else [])
        combo_change_axes.grid(row=8, column=1, sticky='w')
        # ----------Создаём блок описания места риска----------
        tk.Label(WriteNewRisk.frame, text=LEXICON_RU['region']).grid(row=9, column=0, sticky='w')
        entry_region = ttk.Entry(width=50)
        entry_region.grid(row=9, column=1, sticky='w')
        # ----------Создаём блок выбора отметки----------
        tk.Label(WriteNewRisk.frame, text=LEXICON_RU['level']).grid(row=10, column=0, sticky='w')
        scale_level = tk.Scale(from_=-4, to=46, orient=tk.HORIZONTAL)
        scale_level.grid(row=10, column=1, sticky='w')
        # ----------Создаём блок описания риска----------
        tk.Label(WriteNewRisk.frame, text=LEXICON_RU['description']).grid(row=11, column=0, sticky='w')
        entry_description = ttk.Entry(width=50)
        entry_description.grid(row=11, column=1, sticky='w')
        # ----------Создаём блок выбора владельца риска----------
        tk.Label(WriteNewRisk.frame, text=LEXICON_RU['change_owner']).grid(row=12, column=0, sticky='w')
        combo_change_owner_risk = ttk.Combobox(WriteNewRisk.frame, values=dict_division['owner_risk'])
        combo_change_owner_risk.grid(row=12, column=1, sticky='w')
        combo_change_owner_risk.current(0)
        # ----------Создаём блок мероприятия по устранению риска----------
        tk.Label(WriteNewRisk.frame, text=LEXICON_RU['elimination_measures']).grid(row=13, column=0, sticky='w')
        entry_elimination_measures_1 = ttk.Entry(width=50)
        entry_elimination_measures_1.grid(row=13, column=1, sticky='w')
        # ----------Создаём блок выбора ответственного за устранение----------
        tk.Label(WriteNewRisk.frame, text=LEXICON_RU['responsible_for_implementation']).grid(row=14, column=0, sticky='w')
        combo_responsible_for_implementation_1 = ttk.Combobox(WriteNewRisk.frame, values=dict_division["managers"])
        combo_responsible_for_implementation_1.grid(row=14, column=1, sticky='w')
        # ----------Создаём блок выбора срока устранения----------
        tk.Label(WriteNewRisk.frame, text=LEXICON_RU['period_of_execution']).grid(row=15, column=0, sticky='w')
        combo_period_of_execution_1 = ttk.Combobox(WriteNewRisk.frame, values=[0, 1, 2, 4, 8, 26, 52])
        combo_period_of_execution_1.grid(row=15, column=1, sticky='w')
        # ----------Создаём блок для написания ожидаемого результата----------
        tk.Label(WriteNewRisk.frame, text=LEXICON_RU['expected_result']).grid(row=16, column=0, sticky='w')
        entry_expected_result_1 = ttk.Entry(width=50)
        entry_expected_result_1.grid(row=16, column=1, sticky='w')

        # добавляет дополнительное поле ввода если уровень риска больше или равно 6
        if before_grade >= 6:
            tk.Label(WriteNewRisk.frame, text=LEXICON_RU['event_second']).grid(row=17, column=0, columnspan=3)
            # ----------Создаём блок мероприятия по устранению риска----------
            tk.Label(WriteNewRisk.frame, text=LEXICON_RU['elimination_measures']).grid(row=18, column=0, sticky='w')
            entry_elimination_measures_2 = ttk.Entry(width=50)
            entry_elimination_measures_2.grid(row=18, column=1, sticky='w')
            # ----------Создаём блок выбора ответственного за устранение----------
            tk.Label(WriteNewRisk.frame, text=LEXICON_RU['responsible_for_implementation']).grid(row=19, column=0,
                                                                                                 sticky='w')
            combo_responsible_for_implementation_2 = ttk.Combobox(WriteNewRisk.frame, values=dict_division["managers"])
            combo_responsible_for_implementation_2.grid(row=19, column=1, sticky='w')
            # ----------Создаём блок выбора срока устранения----------
            tk.Label(WriteNewRisk.frame, text=LEXICON_RU['period_of_execution']).grid(row=20, column=0, sticky='w')
            combo_period_of_execution_2 = ttk.Combobox(WriteNewRisk.frame, values=[0, 1, 2, 4, 8, 26, 52])
            combo_period_of_execution_2.grid(row=20, column=1, sticky='w')
            # ----------Создаём блок для написания ожидаемого результата----------
            tk.Label(WriteNewRisk.frame, text=LEXICON_RU['expected_result']).grid(row=21, column=0, sticky='w')
            entry_expected_result_2 = ttk.Entry(width=50)
            entry_expected_result_2.grid(row=21, column=1, sticky='w')
            # ----------Создаём кнопку заполнить----------
            button_fin = tk.Button(WriteNewRisk.frame, text=LEXICON_RU['fin_button'], command=get_all_date)
            button_fin.grid(row=21, column=2, sticky='w')
        else:
            # ----------Создаём кнопку заполнить----------
            button_fin = tk.Button(WriteNewRisk.frame, text=LEXICON_RU['fin_button'], command=get_all_date)
            button_fin.grid(row=16, column=2, sticky='w')

    def create_division(self, classificator: str) -> None:
        """Создание блоков выбора классификатора риска и подразделения"""
        # ----------Создаём блок выбора точного типа опасности----------
        tk.Label(WriteNewRisk.frame, text=LEXICON_RU['change_num_type_dangerous']).grid(row=3, column=0, sticky='w')
        combo_change_class_risk = ttk.Combobox(WriteNewRisk.frame, width=95,
                                               values=class_dangerous[classificator])
        combo_change_class_risk.grid(row=3, column=1, columnspan=2, sticky='w')
        # ----------Создаём блок выбора оценки тяжести----------
        tk.Label(WriteNewRisk.frame, text=LEXICON_RU['before_severity_assessmentinput']).grid(row=4, column=0,
                                                                                              sticky='w')
        combo_change_before_severity_assessmentinput = ttk.Combobox(WriteNewRisk.frame, values=[i for i in range(2, 6)])
        combo_change_before_severity_assessmentinput.grid(row=4, column=1, sticky='w')
        combo_change_before_severity_assessmentinput.current(0)
        # ----------Создаём блок выбора оценки вероятности----------
        tk.Label(WriteNewRisk.frame, text=LEXICON_RU['before_probability_estimation']).grid(row=5, column=0,
                                                                                            sticky='w')
        combo_change_before_probability_estimation = ttk.Combobox(WriteNewRisk.frame, values=[i for i in range(2, 6)])
        combo_change_before_probability_estimation.grid(row=5, column=1, sticky='w')
        combo_change_before_probability_estimation.current(0)
        # ----------Создаём блок выбора подразделения----------
        tk.Label(WriteNewRisk.frame, text=LEXICON_RU['change_division']).grid(row=6, column=0, sticky='w')
        combo_change_division = ttk.Combobox(WriteNewRisk.frame, values=(guide['name_division']))
        combo_change_division.grid(row=6, column=1, sticky='w')
        button_change_division = tk.Button(WriteNewRisk.frame, text=LEXICON_RU['select_button'],
                                           command=lambda: self.create_another(combo_change_class_risk.get(),
                                                                               combo_change_division.get(),
                                                                               int(combo_change_before_severity_assessmentinput.get()),
                                                                               int(combo_change_before_probability_estimation.get())
                                                                               )
                                           )
        button_change_division.grid(row=6, column=2, sticky='w')

    def change_dangerous(self):
        """Создаём блок выбора типа опасности"""
        tk.Label(WriteNewRisk.frame, text=LEXICON_RU['num_clas_dangerous']).grid(row=1, column=0, sticky='w')
        combo_change_type_risk = ttk.Combobox(WriteNewRisk.frame, width=50, values=class_dangerous["class_dangerous"])
        combo_change_type_risk.grid(row=1, column=1, sticky='w')
        button_change_dangerous = tk.Button(WriteNewRisk.frame, text=LEXICON_RU['select_button'],
                                            command=lambda: self.create_division(combo_change_type_risk.get().split()[0]))
        button_change_dangerous.grid(row=1, column=2, sticky='w')

    def start(self):
        """Для запуска методов данного класса"""
        self.change_dangerous()
        WriteNewRisk.frame.mainloop()


if __name__ == '__main__':
    WriteNewRisk().start()
