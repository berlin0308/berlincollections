import datetime
date = datetime.datetime(2010,3,2,12,15,0)
period = datetime.timedelta(days=145,hours=10,minutes=3)
result = date + period
print(result)