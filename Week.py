import datetime
from datetime import datetime, timedelta, date
from ast import literal_eval
import calendar
import csv

SAVEFILE = 'time_log_save.txt'


class Day:
    '''stores all information relavant to a drivers day'''
    DEFAULTDATE = datetime(1111, 11, 11)

    def __init__(self,
                 dateObj,
                 sickOpersonal=False,
                 startTime=DEFAULTDATE,
                 endTime=DEFAULTDATE,
                 break1=DEFAULTDATE,
                 break2=DEFAULTDATE,
                 lunchStart=DEFAULTDATE,
                 lunchEnd=DEFAULTDATE,
                 numStops=-1,
                 numAir=-1,
                 notes='',
                 tags=[]):
        self.date = dateObj
        self.sickOpersonal = sickOpersonal
        self.startTime = startTime
        self.endTime = endTime
        
        try: # defining total time
            if startTime != DEFAULTDATE and endTime != DEFAULTDATE:
                self.totalTime = endTime - startTime
            elif self.sickOpersonal == True:
                self.totalTime = timedelta(hours=8)
            else:
                self.totalTime = timedelta(0)
        except TypeError as err:
            print(err)
            self.totalTime = timedelta(0)
        
        self.lunchStart = lunchStart
        self.lunchEnd = lunchEnd
        self.break1 = break1
        self.break2 = break2
        self.numStops = numStops
        self.numAir = numAir
        self.notes = notes
        self.tags = tags
        self.recordCheck = bool(self)
        self.weekDayName = dateObj.strftime('%A')
        #self.attribList = vars(self).keys()

    #Methods

    def calcTotalTime(self):
        total_hours = self.endTime - self.startTime
        total_lunch = self.lunchEnd - self.lunchStart
        hours_worked = total_hours - total_lunch
        if hours_worked > timedelta(hours=9, minutes=30):
            hours_worked += timedelta(minutes=33)
        self.totalTime = hours_worked

    # set vars

    def setAtrib(self, index, value):
        """ from the dict keys of attributes gained from vars() creates a list for an indexable way to set attributes"""

        keys = list(vars(self).keys())  # creates list of keys
        key = keys[index]  # with index gain key value
        vars(self)[
            key] = value  # with key value set attribute to arguement value

    def setStartTime(self, startTime):
        self.startTime = startTime
        if startTime == DEFAULTDATE:
            self.recordCheck = False
        else:
            self.recordCheck = True

    def setEndTime(self, endTime):
        self.endTime = endTime
        self.calcTotalTime()

    def addTag(self, tags):
        for tag in tags:
            self.tags.append(tag)

    def removeTag(self, tag):
        for i, t in enumerate(self.tags):
            if t == tag:
                self.tags.pop(i)

    def save_day(self):
        '''returns the data in a csv format to be written out to a file. each field is seperated by ~ to avoid issues from commas while reading in lists stored in file.'''
        return '''{}~{}~{}~{}~{}~{}~{}~{}~{}~{}~{}\n'''.format(
            self.date, self.startTime, self.endTime, self.break1, self.break2,
            self.lunchStart, self.lunchEnd, self.numStops, self.numAir,
            self.notes, self.tags)

    def check_if_default_date(self, dateChecked):
        '''to check if default date and if so then return an empty string to make Day class print out look cleaner'''
        if dateChecked == datetime(1111, 11, 11):
            return ''
        else:
            return dateChecked

    def check_if_default_num(self, numChecked):
        '''to check for fields such as Stop Count to set to defualt to make print out cleaner'''
        if numChecked == -1:
            return ''
        else:
            return numChecked

    def string_to_bool(self, string):
        if string in ('f', 'F', 'false', 'False'):
            return bool(False)
        elif string in ('t', 'T', 'true', 'True'):
            return bool(True)
        else:
            print("Please use true or false values.")

            #	def __repr__(self):
            #		keys = list(vars(self).keys())
            #		values = list(vars(self).values())
            #		returnStr = ''
            #		for num, attrib in enumerate(vars(self).keys()):
            returnStr += '{:2}  {}: {}\n'.format(num, keys[num], values[num])
        return returnStr

    def __str__(self):
        return """		Date: 				{}
		Sick/Personal:   {}
		Start Time: 		{}
		End Time: 		{}
		Total Time: 					 {}
		Lunch Start: 		{}
		End Start: 		{}
		Break 1: 			{}
		Break 2: 			{}
		Number of stops: 	{}
		Number of air: 		{}
		Notes: 			{}
		Tags: 				{}
		Record Check: 	{}
		Week Day Name: 	{}""".format(
            self.date, self.sickOpersonal,
            self.check_if_default_date(self.startTime),
            self.check_if_default_date(self.endTime), self.totalTime,
            self.check_if_default_date(self.lunchStart),
            self.check_if_default_date(self.lunchEnd),
            self.check_if_default_date(self.break1),
            self.check_if_default_date(self.break2),
            self.check_if_default_num(self.numStops),
            self.check_if_default_num(self.numAir), self.notes, self.tags,
            self.recordCheck, self.weekDayName) + '\n' * 2

    def __getitem__(self, key):
        if type(key) == type(str()):
            return vars(self)[key]
        elif type(key) == type(int()):
            return list(vars(self))[key]

    def __setitem__(self, key, value):

        if type(key) == type(str()):
            attrib = key
        elif type(key) == type(int()):
            attribList = list(vars(self))
            attrib = attribList[key]

        if type(vars(self)[attrib]) == type(datetime(1, 1, 1)):
            try:
                dateANDtime = str(self.date) + ' ' + value
                value = datetime.strptime(dateANDtime, '%Y-%m-%d %H:%M')
            except ValueError as e:
                print("***Incorrect formatting: {}***\n".format(e))
                return None
        elif type(vars(self)[attrib]) == type(int()):
            try:
                value = int(value)
            except ValueError as e:
                print("***Incorrect formatting: {}***\n".format(e))
                return None
        elif type(vars(self)[attrib]) == type(bool()):
            try:
                value = self.string_to_bool(value)
            except ValueError as e:
                print(f'***Error: {e}***')
                return None
        elif type(vars(self)[attrib] == type(str())):
            pass
        elif type(vars(self)[attrib] == type(timedelta())):
            print(
                'Total time is not editable, it will be calculated off other time entries.'
            )
            return None
        vars(self)[attrib] = value

        if attrib == 'startTime':
            self.recordCheck = True

        if attrib in ('endTime', 'lunchEnd'):
            self.calcTotalTime()

    def __bool__(self):
        return (self.startTime != datetime(1111, 11, 11))


class Week:
    '''holds Day objects to organize a standard work week'''

    def create_week(self):
        '''creates a new blank set of Day objects based on the weeks start date'''
        for i in range(7):
            D = Day(self.startDate + timedelta(i))
            self.days.append(D)

    def __init__(self, keyDate=None):
        wd = keyDate.date.weekday()
        self.startDate = keyDate.date - timedelta(wd + 1)
        self.endDate = self.startDate + timedelta(6)
        self.days = []
        self.create_week()

    def __str__(self):
        daysRecorded = []
        for i, day in enumerate(self.days):
            if day.recordCheck:
                daysRecorded.append(i)
        return """Week: {} to {}
Indeces of recorded days: {}
		""".format(self.startDate, self.endDate, daysRecorded)

        def displayWeek(Week):
	print()
	for day in Week.days:
		print(day.date.strftime('| %m/%d'), end = ' ')
	print()
	calendar.setfirstweekday(6)
	print(calendar.weekheader(7))

	for day in Week.days:
		if day.recordCheck:
			rc = 'X'
		else:
			rc = ' '
		print('  [{}]  '.format(rc), end = ' ')


def save_log(logDict, fileName):
    with open(SAVEFILE, 'w') as f:
        d = list(logDict.values())[0]
        list_of_dict_values = list(vars(d).keys())
        fieldnames = list_of_dict_values[0]
        writer = csv.writer(f)
        writer.writerow(fieldnames)
        for day in list(logDict.values()):
            writer.writerow(list(vars(day).values()))


def load_log(SAVEFILE, dayLog):
    with open(SAVEFILE, 'r') as f:
        reader = csv.reader(f)
        column_names = next(reader)
        for index, line in enumerate(reader):
            d = datetime.strptime(line[0], '%Y-%m-%d')
            D = Day(d)
            dayLog[d.strftime('%Y%m%d')] = D
            for i, value in enumerate(line, start=0):
                if i <= (len(column_names) - 1):
                    setattr(dayLog[d.strftime('%Y%m%d')], column_names[i],
                            value)
    return dayLog


def save_day_to_log(Day, dayLogs):
    '''save Day object to dictionary of recorded days and returns updated dictionary'''
    dayLogs['{}{}{}'.format(Day.date.year, Day.date.month, Day.date.day)] = Day
    return dayLogs


def main():
    '''Test examples'''
    # creation of Day objects
    d = date(2020, 2, 29)
    D = Day(d)
    print(D)

    # creation of Week objects
    w = Week(D)

    # using setters to update Day objects inside Week object
    w.days[1].setStartTime(datetime(2020, 2, 24, 9, 00))
    w.days[3].setStartTime(datetime(2020, 2, 25, 9, 00))
    w.days[5].setStartTime(datetime(2020, 2, 28, 9, 00))

    w.days[1].setEndTime(datetime(2020, 2, 24, 21, 00))
    w.days[3].setEndTime(datetime(2020, 2, 25, 17, 00))
    w.days[5].setEndTime(datetime(2020, 2, 28, 18, 31))

    w.days[1].LunchStart = datetime(2020, 2, 24, 13, 15)
    w.days[1].LunchEnd = datetime(2020, 2, 24, 14, 21)
    w.days[1].LunchStart = datetime(2020, 2, 24, 13, 15)
    w.days[1].Break1 = datetime(2020, 2, 24, 13, 15)
    w.days[1].Break2 = datetime(2020, 2, 24, 13, 15)
    w.days[1].Notes = 'This day was the best ever. They even bought me lunch.'
    w.days[1].NumStops = 120
    w.days[1].NumAir = 1
    #	w.days[1].addTag('amazing', 'homeby5')
    #	w.days[1].addTag('repeat')

    # check Week class string method
    print(w)

    # day object output to be used for saving to file
    print("Raw Week Data")
    for day in w.days:
        print(day.save_day(), end='')

    # testing data structure to be used in final program
    print("\nDays Saved to Log Dictionary")
    dayLogs = {}
    date2 = date(1980, 3, 11)
    d2 = Day(date2)
    save_day_to_log(d2, dayLogs)
    print(dayLogs)
    for day in w.days:
        if day.recordCheck:
            save_day_to_log(day, dayLogs)
            #dayLogs['{}{}{}'.format(day.date.year, day.date.month, day.date.day)] = day
    print('Day Logs - ')
    print(dayLogs)

    # checking output from dictionary for saving to file
    printSpool = []
    for day in dayLogs.values():
        printSpool.append(day.save_day())
    print(*printSpool)

    save_log(dayLogs, 'time_log_save.txt')

    dayLogs.clear()
    print('Day logs = ', end='')
    print(dayLogs)

    dayLogs = load_log(SAVEFILE, dayLogs)

    print(dayLogs['20200224'])
    print(dayLogs)

    d2.date = "No date here"

    print('\nThe Date is ', end='')
    print(d2['date'])

    with open(SAVEFILE, 'w') as f:
        fieldnames = list(vars(d2).keys())
        writer = csv.writer(f)
        writer.writerow(fieldnames)
        for day in list(dayLogs.values()):
            writer.writerow(list(vars(day).values()))


if __name__ == '__main__':
    main()
'''	
d = date.today()
D = Day(d)
'''

