from datetime import datetime

now = datetime.now()
Year = str(now.year)

if now.month == 1:
    Month = 'Jan'
elif now.month == 2:
    Month = 'Feb'
elif now.month == 3:
    Month = 'Mar'
elif now.month == 4:
    Month = 'Apr'
elif now.month == 5:
    Month = 'May'
elif now.month == 6:
    Month = 'Jun'
elif now.month == 7:
    Month = 'Jul'
elif now.month == 8:
    Month = 'Aug'
elif now.month == 9:
    Month = 'Sep'
elif now.month == 10:
    Month = 'Oct'
elif now.month == 11:
    Month = 'Nov'
elif now.month == 12:
    Month = 'Dec'

Day = str(now.day)

DATE = Month+'. '+Day+', '+Year 
