from datetime import datetime, date
from Week import Day, save_day_to_log, save_log
import csv
import os

SAVEFILE = 'TL_tester.txt'
dayLog = {}
d = date(1,1,1)
D = Day(d)
d2 = datetime(1,1,2)
D2 = Day(d2.date())

D['startTime'] = '9:00'
D['recordCheck'] = 'True'
#print(len(vars(D)))



#print(dikt)
save_day_to_log(D, dayLog)
save_day_to_log(D2, dayLog)
#print(dayLog)

def load_log(dayLog, SAVEFILE):
    with open(SAVEFILE, 'r') as f:
        reader = csv.reader(f)
        column_names = next(reader)
        for index, line in enumerate(reader):
            d = datetime.strptime(line[0], '%Y-%m-%d %H:%M:%S')
            D = Day(d)
            dayLog[d.strftime('%Y%m%d')] = D
            for i, value in enumerate(line):
                setattr(dayLog[d.strftime('%Y%m%d')], column_names[i], value)
                
    return dayLog
#load_log(dayLog)

#print(dayLog['20200226'])


#save_log(dayLog, 'time_log_save.txt')

d = list(dayLog.values())[0]
print(list(vars(d).keys()))
