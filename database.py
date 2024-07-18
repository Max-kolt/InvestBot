from peewee import *
from datetime import date
from config import DB_NAME, DEFAULT_DAY_SCHEDULE, DEFAULT_WEEK_SCHEDULE


db = SqliteDatabase(F"{DB_NAME}.db")


class BaseModel(Model):
    class Meta:
        database = db


class Investor(BaseModel):
    login = CharField(primary_key=True, max_length=60)
    chat_id = CharField()
    name = TextField()
    project_description = TextField()
    amount_of_income = CharField(max_length=100)
    required_amount = CharField(max_length=100)
    # amount_purpose = TextField(null=True)
    document = TextField()
    necessary_assistance = TextField()


class TimeTable(BaseModel):
    week_day = CharField(max_length=20)
    hours = IntegerField()


class ScheduleTime(BaseModel):
    week_time = ForeignKeyField(TimeTable, backref="scheduled")
    date = DateField()
    investor = ForeignKeyField(Investor, backref="scheduled_meet")


def main():
    db.connect()
    tables = db.get_tables()
    count = len(tables)
    if count > 0:
        print(F"В базе данных {count} таблиц: {tables}")
        drop = input("После этой операции все таблицы с данными сотруться.\n"
                     "Вы уверенны что хотите пересоздать базу данных?(y/N): ")
        if drop != "y":
            print("Операция отменена")
            return
    db.create_tables([Investor, TimeTable, ScheduleTime])

    for day in DEFAULT_WEEK_SCHEDULE:
        for hour in DEFAULT_DAY_SCHEDULE:
            TimeTable.create(week_day=day, hours=hour)


if __name__ == '__main__':
    main()
