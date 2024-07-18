from datetime import date, timedelta


def week_schedule_generate():
    now = date.today()
    days = list()
    for i in range(1, 7):
        next_day = now+timedelta(days=i)
        if next_day.weekday() == 5:
            now += timedelta(days=2)
            next_day = now+timedelta(days=i)
        days.append(next_day.strftime("%d.%m"))
    return days