from datetime import datetime
import pytz


def current_time(self):
    return datetime.now().replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Asia/Shanghai')).isoformat()
