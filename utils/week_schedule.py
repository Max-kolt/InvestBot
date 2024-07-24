from datetime import date, timedelta
from peewee import DateField

from database import ScheduleTime, TimeTable
from config import DEFAULT_DAY_SCHEDULE

ADDITION_DAYS = {
    5: 2,
    6: 1,
}


def week_schedule_generate():
    now = date.today()
    scheduled_days: list[DateField] = ScheduleTime.select().where(ScheduleTime.date > now)
    days = list()
    for i in range(1, 6):
        current_day = now + timedelta(days=i)
        current_weekday = current_day.weekday()
        if current_weekday in ADDITION_DAYS.keys():
            now += timedelta(days=ADDITION_DAYS[current_weekday])
            current_day = now + timedelta(days=i)

        count_time = list(filter(lambda day: day.date == current_day, scheduled_days))
        if len(count_time) == len(DEFAULT_DAY_SCHEDULE):
            continue
        days.append(current_day.strftime('%d.%m'))

    return days


def day_schedule_generate(day: str):
    query = ScheduleTime.select(ScheduleTime, TimeTable).join(TimeTable)\
        .where(ScheduleTime.date.day == day)
    scheduled_hours = [sched.week_time.hours for sched in query]
    hours = list()
    for hour in DEFAULT_DAY_SCHEDULE:
        if hour in scheduled_hours:
            continue
        hours.append(hour)

    return hours

