from peewee import *
from playhouse.migrate import PostgresqlMigrator, migrate
from datetime import date
from config import DB_NAME, DB_USER, DB_USER_PASSWORD, DB_HOST, DB_PORT, DEFAULT_DAY_SCHEDULE, DEFAULT_WEEK_SCHEDULE

db = PostgresqlDatabase(DB_NAME, user=DB_USER, password=DB_USER_PASSWORD, host=DB_HOST, port=DB_PORT)
migrator = PostgresqlMigrator(db)


class BaseModel(Model):
    class Meta:
        database = db


class Investor(BaseModel):
    login = CharField(primary_key=True, max_length=60)
    chat_id = CharField()
    name = TextField(null=True)
    project_description = TextField(null=True)
    amount_of_income = CharField(max_length=100, null=True)
    required_amount = CharField(max_length=100, null=True)
    # amount_purpose = TextField(null=True)
    document = TextField(null=True)
    necessary_assistance = TextField(null=True)
    get_gift = BooleanField(null=True)
    utm_metka = CharField()


class TimeTable(BaseModel):
    week_day = CharField(max_length=20)
    hours = IntegerField()


class ScheduleTime(BaseModel):
    week_time = ForeignKeyField(TimeTable, backref="scheduled")
    date = DateField()
    investor = ForeignKeyField(Investor, backref="scheduled_meet", on_delete="CASCADE")


def main():
    db.connect()
    tables = db.get_tables()
    count = len(tables)
    # if count > 0:
    #     print(F"В базе данных {count} таблиц: {tables}. Удалите базу данных и потом запустите скрипт снова.")
    #     return

    db.create_tables([Investor, TimeTable, ScheduleTime])

    for day in DEFAULT_WEEK_SCHEDULE:
        for hour in DEFAULT_DAY_SCHEDULE:
            TimeTable.create(week_day=day, hours=hour)


if __name__ == '__main__':
    migrate(
        migrator.add_column(Investor._meta.table_name, "utm_metka", CharField(default='other'))
    )

