import string

class StringToPrefixes:
    def __init__(self, txt_string):
        self.txt_string = txt_string.lower()
        # 1.) Convert the string to words and save in a word list
        self.tokenize_string()
        # 2.) Create prefixes from each word and save in a prefix list
        self.create_prefixes()
    
    def tokenize_string(self):
        self.word_list = []
        words = [self.txt_string.strip(string.punctuation).lower() for self.txt_string in self.txt_string.split() ]
        for word in words:
            self.word_list.append(word)
    
    def create_prefixes(self):
        self.prefix_dict = {}
        for word in self.word_list:
            prefix_list = []
            running_prefix = ""
            for (counter, char) in enumerate(word):
                running_prefix = running_prefix + char
                if counter != 0:
                    prefix_list.append(running_prefix)
                
            prefix_list.reverse()
            self.prefix_dict[word] = prefix_list
    
    def get(self):
        return self.prefix_dict
    