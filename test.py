def pref(string):
	if string.__len__() == 2:
		return [string]
	else:
		return pref(string[:-1]) + [string]