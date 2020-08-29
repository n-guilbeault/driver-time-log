from datetime import datetime

def string_to_bool(string):
	if string in ('f', 'F', 'false', 'False', 0):
		return bool(False)
	elif string in ('t', 'T', 'true', 'True', 1):
		return bool(true)
	else:
		print("Please use true or false values.")

class TestClass:
	""" test class to show effect of change attribute method """
	def __init__(self):
		self.a = 1
		self.b = False
		self.c = 'string'
		self.d = 4.2
		
	def setAtrib(self, index, value):
		""" from the dict keys of attributes gained from vars() creates a list for an indexable way to set attributes"""
		keys = list(vars(self).keys()) # creates list of keys
		key = keys[index] # with index gain key value
		vars(self)[key] = value # with key value set attribute to arguement value
		
	def change_attribute_enhanced(self, index, value):
		keys = list(vars(self).keys())
		key = keys[index]
		
		if type(vars(self)[key]) == type(int()):
			vars(self)[key] = int(value)
		elif type(vars(self)[key]) == type(bool()):	
			vars(self)[key] = string_to_bool(value)
		elif type(vars(self)[key]) == type(datetime(1,1,1)):
			try:
				tempDatetime = datetime.strptime(value, '%m/%d/%Y %H:%M')
				vars(self)[key] = tempDatetime
			except Exception as err:
				print("There is an issue: {}".format(err))
		elif type(vars(self)[key]) == type(str()):
			if type(value) == type(str()):
				vars(self)[key] = value
		else:
			print("What are you try to do? Don't recognize that variable type.")
				
classObj = TestClass()

print(vars(classObj))



print(classObj.d)

#classObjKeys = list(vars(classObj).keys())
#key = classObjKeys[2]
#vars(classObj)[key] = 20
classObj.change_attribute_enhanced(3, '8/20/2020 9:38')

print(classObj.d)

print(vars(classObj))

