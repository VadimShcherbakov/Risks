"""Описываем модель данных и структуру БД"""

from peewee import *
db = SqliteDatabase('data/risks.db')


class BaseModel(Model):
    """Создание базового класса от которого будут наследоваться остальные классы"""
    class Meta:
        """Указываем мета класс с моделью которая будет работать база данных"""
        database = db  # Указываем рабочую базу данных


class Risk(BaseModel):
    zone = CharField()
    num_zone = IntegerField()
    # order_num_risk = IntegerField()
    # unique_number = CharField(primary_key=True, unique=True)
    region = CharField(null=True)
    level = IntegerField()
    num_clas_dangerous = CharField()
    date_of_detection = DateField()
    owner_risk = CharField()
    description_risk = CharField()
    before_severity_assessmentinput = IntegerField()
    before_probability_estimation = IntegerField()
    before_grade = IntegerField()
    before_significance_level = IntegerField()
    choosing_response_method = CharField()
    source_of_funding = CharField()
    # # photo_before = CharField()
    elimination_measures = CharField()
    expected_result = CharField()
    # # name_division = CharField()
    rows = CharField(null=True)
    axes = CharField(null=True)
    # risk_id = CharField()
    num_event_number = IntegerField()
    count_entries = IntegerField()
    period_of_execution = DateField()
    responsible_for_implementation = CharField()
    weeks_eliminate = IntegerField()

    class Meta:
        db_table = 'risks'

