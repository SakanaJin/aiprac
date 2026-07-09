from datetime import datetime, timedelta

def round_nearest_min(time: datetime) -> datetime:
    return (time.replace(second=0, microsecond=0, minute=time.minute, hour=time.hour) + timedelta(minutes=time.second//30))