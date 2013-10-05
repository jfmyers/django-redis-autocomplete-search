import string

class StringToPrefixes:
	def __init__(self, txt_string):
		# 1.) Convert the string to words and save in a word list
		self.words = [txt_string.strip(string.punctuation).lower() for txt_string in txt_string.split() ]
		# 2.) Create prefixes from each word and save in a prefix list
		self.create_prefix_dict()
    
	def create_prefix_dict(self):
		self.prefix_dict = {}
		for word in self.words:
			list = self.prefix(word)
			list.reverse()
			self.prefix_dict[word] = list

	def prefix(self, word):
		if word.__len__() == 2:
			return [word]
		else:
			return self.prefix(word[:-1]) + [word]

	def get(self):
		return self.prefix_dict