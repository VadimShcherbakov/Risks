"""Модуль для записи устранения рисков"""

import datetime
import tkinter as tk
from PIL import Image, ImageTk
from lexicon.lexicon_ru import LEXICON_RU
import os
import shutil
from services.model import *
from way.way import WAY
from services.services import significance_level


class TroubleshootingRisk:

    def __init__(self, unique_number, num_risk):
        self.unique_number = unique_number
        self.num_risk = num_risk

    def determination_probability(self):
        db = SqliteDatabase('services/data/risks.db')
        full_done_status = 0
        count_entries = db.execute_sql(f"""select count_entries from risks
                                 WHERE risk_id = {self.num_risk}""").fetchone()[0]
        if count_entries == 1:
            after_severity_assessmentinput = 1
            after_probability_estimation = 1
            full_done_status = 1
        else:
            list_done = [i[0] for i in db.execute_sql(f"""SELECT status from event_risks as er
                                    LEFT JOIN done_risks as dr USING (unique_number_id)
                                    where er.num_risk_id = {self.num_risk}""").fetchall()]
            if any(list_done):
                after_severity_assessmentinput = 1
                after_probability_estimation = 1
                full_done_status = 1
            else:
                after_severity_assessmentinput = db.execute_sql(f"""SELECT before_severity_assessmentinput from risks 
                                                                    where risk_id = {self.num_risk}""").fetchone()[0]
                before_probability_estimation = db.execute_sql(f"""SELECT before_probability_estimation from risks 
                                                                    where risk_id = {self.num_risk}""").fetchone()[0]
                if before_probability_estimation <= 2:
                    after_probability_estimation = before_probability_estimation
                else:
                    after_probability_estimation = before_probability_estimation - 1
        return after_severity_assessmentinput, after_probability_estimation, full_done_status

    def create_picture(self) -> None:
        """Создаёт интерфейс просмотра рисков до и после выполнения"""
        explanations = db.execute_sql(f"SELECT expected_result from event_risks where unique_number_id like '{self.unique_number}'").fetchone()[0]
        elimination_measures = db.execute_sql(f"SELECT elimination_measures from event_risks where unique_number_id like '{self.unique_number}'").fetchone()[0]
        way_photo_before = db.execute_sql(f"SELECT photo_before from risks where risk_id = {self.num_risk}").fetchone()[0]
        after_severity_assessmentinput, after_probability_estimation, full_done_status = self.determination_probability()
        after_grade = after_severity_assessmentinput*after_probability_estimation
        after_significance_level = significance_level(after_grade)
        photo_after = os.path.join(photo_record_risk_after, f'{self.unique_number}.JPG')
        date_elimination = datetime.datetime.now().date()

        def clic_button_accept() -> None:
            """Собирает и записывает данные если была нажата кнопка принять"""
            DoneRisk.create(
                unique_number_id=self.unique_number,
                num_risk=self.num_risk,
                explanations=explanations,
                after_severity_assessmentinput=after_severity_assessmentinput,
                after_probability_estimation=after_probability_estimation,
                after_grade=after_grade,
                after_significance_level=after_significance_level,
                photo_after=photo_after,
                date_elimination=date_elimination
            )
            shutil.move(os.path.join(photo_raw_risk_after, raw_photo_name), photo_after)
            if full_done_status ==1:
                FullDoneRISK.create(
                    risk_id=self.num_risk,
                    date_elimination=date_elimination

            )
            frame.destroy()

        def clic_button_reject() -> None:
            """Закрывает окно приложение если была нажата кнопка отклонить"""
            frame.destroy()

        img_1 = Image.open(way_photo_before)
        img_1 = img_1.resize((400, 400), Image.ANTIALIAS)
        img_1 = ImageTk.PhotoImage(img_1)
        panel_1 = tk.Label(frame, image=img_1)
        panel_1.image = img_1
        panel_1.grid(row=0, column=0)

        img_2 = Image.open(os.path.join(photo_raw_risk_after, raw_photo_name))
        img_2 = img_2.resize((400, 400), Image.ANTIALIAS)
        img_2 = ImageTk.PhotoImage(img_2)
        panel_2 = tk.Label(frame, image=img_2)
        panel_2.image = img_2
        panel_2.grid(row=0, column=1)

        tk.Label(frame, text=f"{unique_number} {elimination_measures} -> {explanations}").grid(row=1, column=0, columnspan=2)
        tk.Label(frame, text=LEXICON_RU['photo_before']).grid(row=2, column=0)
        tk.Label(frame, text=LEXICON_RU['photo_after']).grid(row=2, column=1)

        button_reject = tk.Button(frame, text=LEXICON_RU['button_reject'], command=clic_button_reject)
        button_reject.grid(row=3, column=0)

        button_accept = tk.Button(frame, text=LEXICON_RU['button_accept'], command=clic_button_accept)
        button_accept.grid(row=3, column=1)

    def start(self) -> None:
        """Запускает метод класса TroubleshootingRisk """
        self.create_picture()


if __name__ == '__main__':
    db = SqliteDatabase('services/data/risks.db')
    photo_raw_risk_after = WAY['photo_raw_risk_after']
    photo_record_risk_after = WAY['photo_record_risk_after']
    list_done_risks = [i[0] for i in db.execute_sql(f"SELECT unique_number_id from done_risks").fetchall()]
    for dirpath, subdirs, files in os.walk(photo_raw_risk_after):
        for raw_photo_name in files:
            unique_number = raw_photo_name.split('.')[0]
            num_risk = unique_number.split('-')[1]
            if unique_number not in list_done_risks:
                frame = tk.Tk()
                frame.geometry('900x500')
                for c in range(2): frame.columnconfigure(index=c, weight=1)
                for r in range(5): frame.rowconfigure(index=r, weight=1)
                TroubleshootingRisk(unique_number=unique_number, num_risk=num_risk).start()
                frame.mainloop()
            else:
                print(f"риск № {unique_number} - выполнен вносить не требуется")
                continue



