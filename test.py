import datetime

def get_time():
    lesson_times = [
        "8:20", "10:00", "11:40", "13:45", "15:25", "17:05", "18:35"
    ]

    now = datetime.datetime.now().time()
    current_time = datetime.time(now.hour, now.minute)

    for lesson_time in lesson_times:
        start_time = datetime.datetime.strptime(lesson_time, "%H:%M").time()
        difference = datetime.datetime.combine(datetime.date.today(), start_time) - datetime.datetime.combine(datetime.date.today(), current_time)

        if difference.total_seconds() >= -900 and difference.total_seconds() <= 600:
            return start_time.strftime("%H:%M")
    return None


nearest_lesson_time = get_time()

if nearest_lesson_time:
    print(f"Ближайшее время начала занятий: {nearest_lesson_time}")
else:
    print("Сейчас у тебя занятий нет.")
