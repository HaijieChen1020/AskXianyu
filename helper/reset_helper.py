from datetime import datetime, timedelta

def get_reset_remains():
    current_time = datetime.utcnow()
    reset_time = datetime(current_time.year, current_time.month, current_time.day, 0)
    if reset_time < current_time:
        reset_time += timedelta(hours=24)
    time_delta = reset_time - current_time
    total_sec = time_delta.total_seconds()
    hours = total_sec/3600
    minutes = (total_sec % 3600) / 60
    secs = total_sec % 60
    return f'There are {int(hours)} hours {int(minutes)} minutes and {int(secs)} seconds to reset'