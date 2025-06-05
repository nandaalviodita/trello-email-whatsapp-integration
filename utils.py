from datetime import datetime
import pytz

def convert_to_local_time(utc_time):
    local_tz = pytz.timezone('Asia/Jakarta')
    utc_time = datetime.strptime(utc_time, "%Y-%m-%dT%H:%M:%S.%fZ")
    utc_time = pytz.utc.localize(utc_time)
    return utc_time.astimezone(local_tz)

def format_date(iso_date):
    if not iso_date:
        return "Tidak ada tanggal"
    try:
        local_time = convert_to_local_time(iso_date)
        return local_time.strftime("%A, %d %B %Y Pk. %H:%M")
    except ValueError:
        return "Format tanggal salah"
