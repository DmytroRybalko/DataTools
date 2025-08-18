# %%
from datetime import datetime, timedelta

#def gps_to_utc(gps_week, tow_ms):
# GPS epoch: January 6, 1980
# %%
gps_epoch = datetime(1980, 1, 6)

# %%
gps_week = 2374 #65535
tow_ms = 30300
#utc_datetime = gps_to_utc(gps_week, tow_ms)
# Total seconds = weeks * 7 days/week * 86400 sec/day + tow (converted from ms to sec)
total_seconds = gps_week * 7 * 86400 + tow_ms / 1000.0

# %%
# Final UTC datetime
utc_time = gps_epoch + timedelta(seconds=total_seconds)
#return utc_time

# Example:
#gps_week = 65535
#tow_ms = 30300
#utc_datetime = gps_to_utc(gps_week, tow_ms)

#print("UTC Time:", utc_datetime)