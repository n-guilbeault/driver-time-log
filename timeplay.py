import datetime, csv

from Week import Day

date0 = datetime.datetime(1980, 3, 11)

print('my bday - ', date0, date0.weekday())

dateNow = datetime.datetime.now()

print('todays date - ', dateNow)

dif = dateNow - date0

print('i have been around this long -> ', dif)
'''
day = int(input('please enter day #: '))
month = int(input('please enter month #: '))
year = int(input('please enter year: '))
userDate = datetime.datetime(year, month, day)
print(userDate)
'''

tempDay = Day(dateNow)
print('\n' * 4)
print(tempDay)

