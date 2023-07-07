"""Описываем модель данных и структуру БД"""

from peewee import *
db = SqliteDatabase('services/data/risks.db')


class BaseModel(Model):
    """Создание базового класса от которого будут наследоваться остальные классы"""
    class Meta:
        """Указываем мета класс с моделью которая будет работать база данных"""
        database = db  # Указываем рабочую базу данных


class Zone(BaseModel):
    """Создание класса модели номера цеха (основной таблицы)"""
    num_zone = IntegerField(primary_key=True, unique=True)
    description_zone = CharField()

    class Meta:
        """Указываем рабочую модель таблицу зоны"""
        db_table = 'zones'


class TypeRisk(BaseModel):
    """Создание класса модели типы рисков"""
    clas_dangerous_id = CharField(primary_key=True, unique=True)
    description_clas_dangerous = CharField()

    class Meta:
        """Указываем рабочую модель таблицу типы рисков"""
        db_table = 'type_risks'


class Risk(BaseModel):
    """Создание класса модели рисков (основной таблицы)"""
    risk_id = AutoField()
    num_zone = IntegerField()
    region = CharField(null=True)
    rows = CharField(null=True)
    axes = CharField(null=True)
    level = IntegerField()
    clas_dangerous = ForeignKeyField(TypeRisk, to_field='clas_dangerous_id')
    date_of_detection = DateField()
    owner_risk = CharField()
    description_risk = CharField()
    before_severity_assessmentinput = IntegerField()
    before_probability_estimation = IntegerField()
    before_grade = IntegerField()
    before_significance_level = CharField()
    photo_before = CharField()
    count_entries = IntegerField()

    class Meta:
        """Указываем рабочую модель таблицу риски"""
        db_table = 'risks'


class EventRisk(BaseModel):
    """Создание класса модели рисков (основной таблицы)"""
    unique_number_id = CharField(primary_key=True, unique=True)
    num_risk = ForeignKeyField(Risk, to_field='risk_id')
    choosing_response_method = CharField(default='Устранение риска', null=True)
    elimination_measures = CharField()
    expected_result = CharField()
    period_of_execution = DateField()
    responsible_for_implementation = CharField()
    source_of_funding = CharField(default='РП')
    num_event_number = IntegerField()
    weeks_eliminate = IntegerField()

    class Meta:
        """Указываем рабочую модель таблицу риски"""
        db_table = 'event_risks'


class DoneRisk(BaseModel):
    """Создание класса модели выполненных рисков """
    unique_number_id = CharField(primary_key=True, unique=True)
    num_risk = ForeignKeyField(Risk, to_field='risk_id')
    status = CharField(default='выполнено')
    explanations = CharField()
    after_severity_assessmentinput = IntegerField()
    after_probability_estimation = IntegerField()
    after_grade = IntegerField()
    after_significance_level = CharField()
    photo_after = CharField(null=True)
    date_elimination = DateField()

    class Meta:
        """Указываем рабочую модель таблицу риски"""
        db_table = 'done_risks'

