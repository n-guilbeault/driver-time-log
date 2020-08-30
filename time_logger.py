from Week import Day, Week, save_log, load_log, save_day_to_log
from datetime import date, datetime

SAVEFILE = 'time_log_save.txt'  #'time_log_save.txt'


def string_to_date(string):
	return datetime.strptime(string, '%m/%d/%Y %H:%M')
	
def string_to_bool(string):
	if string in ('f', 'F', 'false', 'False'):
		return bool(False)
	elif string in ('t', 'T', 'true', 'True'):
		return bool(True)
	else:
		print("Please use true or false values.")

today = date.today()
d = Day(today)

bdDate = date(1980, 3, 11)
bd = Day(bdDate)
dayLogs = {'19800311': bd}
w = Week(d)

'''
print(dayLogs)
for day in w.days:
	save_day_to_log(day, dayLogs)
print(dayLogs)
for day in dayLogs.values():
	print(day)
'''


print('\n\n')

print("Welcome to TimeLogger")
print("Todays date: {:%m/%d/%Y}\n".format(today))

w.displayWeek()

print('\n\n')
while True:
	dayChoice = input("Select day (in format m/d/y, enter nothing for today): ")
	if dayChoice == '':
		tempDay = Day(today)
		break
	else:
		try:
			dayChoice = dayChoice.strip()
			tempDay = Day(datetime.strptime(dayChoice,"%m/%d/%Y"))
			break
		except ValueError as err:
			print(err)
			print('Please try again...')


while True:
	testStr = str(tempDay)
	for i, line in enumerate(testStr.splitlines()):
		if i == 0:
			i = ' '
		print('{} {}'.format(i, line))
	editDay = input('Would you like to edit this day? (y/n)')
	if editDay == 'y':
		while True:
			VariableIndex = int(input("Please select number next to thing you wish to edit: "))
			if VariableIndex > 0 and VariableIndex < len(testStr):
				break
			else:
				print("Please enter a number between 0 and ")
				continue
		tempDay[VariableIndex] = input('Please enter value: ')
		save_day_to_log(tempDay, dayLogs)
		continue
	elif editDay == 'n':
		if tempDay.recordCheck == True:
			save_day_to_log(tempDay, dayLogs)
		break
	else:
		save_day_to_log(tempDay, dayLogs)
		continue

save_log(dayLogs, SAVEFILE)
