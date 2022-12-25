import datetime
import time

n_days_ago = datetime.datetime.now() - datetime.timedelta(days=3)
print(time.mktime(time.strptime("2022-12-14 09:00:00", '%Y-%m-%d %H:%M:%S')))
print(n_days_ago.timestamp())
print(time.mktime(time.strptime("2022-12-14 09:00:00", '%Y-%m-%d %H:%M:%S')) < n_days_ago.timestamp())