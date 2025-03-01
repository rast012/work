from datetime import datetime, timedelta

# 1. Subtract five days from the current date
def subtract_five_days():
    return datetime.now() - timedelta(days=5)
print(subtract_five_days().strftime("%Y-%m-%d"))

# 2. Print yesterday, today, and tomorrow
def print_dates():
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    tomorrow = today + timedelta(days=1)
    print("Yesterday:", yesterday)
    print("Today:", today)
    print("Tomorrow:", tomorrow)
print_dates()

# 3. Drop microseconds from datetime
def drop_microseconds():
    return datetime.now().replace(microsecond=0)
print(drop_microseconds())

# 4. Calculate difference between two dates in seconds
def date_difference_in_seconds(date1, date2):
    diff = date2 - date1
    return diff.total_seconds()
#ex:
date1 = datetime(2024, 3, 1, 12, 0, 0)
date2 = datetime(2024, 3, 2, 14, 30, 0)
print(date_difference_in_seconds(date1, date2))