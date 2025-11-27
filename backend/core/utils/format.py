from datetime import datetime,timedelta

def format_slot_range(slot_time):
    start = datetime.combine(datetime.today(), slot_time)
    end = start + timedelta(hours=1)
    start_str = start.strftime("%I:%M%p").lstrip("0")
    end_str = end.strftime("%I:%M%p").lstrip("0")
    return f"{start_str} - {end_str}"