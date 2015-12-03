import codecs, json
from types import * 
import re, string, timeit
def writeFile(fileName, data):
	with open(fileName, 'w') as outfile:
    		json.dump(data, outfile)


def findRhymingPart(line):
	words = line.split(" ")
	stressIndex = None

	# find primary stress
	for index, word in reversed(list(enumerate(words))):
		if word.find('1') != -1:
			stressIndex = index
			break
	# find secondary stress if no primary found
	if stressIndex is None:
		for index, word in reversed(list(enumerate(words))):
			if word.find('2') != -1:
				stressIndex = index
				break

	# find no stress if no secondary found
	if stressIndex is None:
		for index, word in reversed(list(enumerate(words))):
			if word.find('0') != -1:
				stressIndex = index
				break

	return words[stressIndex:]

def readCMUPhoneticDictionary():
	file = open('cmudict-0.7b.txt', 'r')
	pastIntro = False
	rhymingDict = {}
	for line in file:
		if line[0] == 'A':
			pastIntro = True
		if pastIntro:
			word = line.split(" ")[0]
			try:
				word.decode('utf-8')
			except UnicodeError:
			    a = 3
			else:	
				rhymingDict[word] = findRhymingPart(line)
	
	writeFile("RhymingDict.json", rhymingDict)


def readRhymingDict():
	with open("RhymingDict.json") as data_file:    
		return json.load(data_file)


def doTheseWordsRhyme(word, word2, rhymingDict):
	
	try:
		word = str(word)
	except:
		#print "not even a unicode", word
		return False
	try:
		word2 = str(word2)
	except:
		#print "not even a unicode", word2
		return False

	exclude = set(string.punctuation)
	word = ''.join(ch for ch in word if ch not in exclude)	
	word2 = ''.join(ch for ch in word2 if ch not in exclude)
	if not word.isalpha() and not word2.isalpha():
		#print "not strings", word, word2
		return False

	if word.upper() not in rhymingDict:
		# print "not in dict", word
		suffix = word[-2:].upper()
		# print "suffix->", suffix
		foundWord = False
		for possibleWord in rhymingDict:
			# print "possibleWord->", possibleWord
			# print "pssible suffix->", possibleWord[-2:]
			if len(possibleWord)> 2 and possibleWord[-2:] == suffix:
				word = possibleWord
				# print "FOUND WORD->", possibleWord
				foundWord = True
				break
		if not foundWord:
			# print "word->", word
			return False

		# return False
	if word2.upper() not in rhymingDict:
		# print "not in dict", word2
		suffix = word2[-2:].upper()
		# print "suffix->", suffix
		foundWord = False
		for possibleWord in rhymingDict:
			# print "possibleWord->", possibleWord
			# print "pssible suffix->", possibleWord[-2:]
			if len(possibleWord)> 2 and possibleWord[-2:] == suffix:
				word2 = possibleWord
				# print "FOUND WORD!!!!->", possibleWord
				foundWord = True
				break
		if not foundWord:
			# print "word2->", word2
			return False
		# return False
		#word.upper()[-2:] == word.upper()[-2:]
	# if not isinstance(word, unicode) and not isinstance(word2, unicode):
	# 	print "not strings", word, word2

	# 	return False
	# with open("RhymingDict.json") as data_file:    
	# 	rhymingDict = json.load(data_file)
	#print "word ->", rhymingDict[word.upper()]
	#print "word2 ->", rhymingDict[word2.upper()]

	if rhymingDict[word.upper()] == rhymingDict[word2.upper()]:
		#print "rhyming ->", word, word2
		return True
	return False


# def findRhymes():
# 	phoneticsDict = readCMUPhoneticDictionary()
# 	rhymingDict = {}
# 	count = 0

# 	for (word, rhymingPart) in phoneticsDict:


# 	    for (word2, rhymingPart2) in phoneticsDict:

# 			try:
# 			    word.decode('utf-8')
# 			    word2.decode('utf-8')			    
# 			except UnicodeError:
# 			    a = 3
# 			else:
# 				if rhymingPart == rhymingPart2:
# 					if word in rhymingDict:
# 						rhymingDict[word].append(word2)
# 					else:
# 						rhymingDict[word] = [word2]

# 	with codecs.open('RhymingDictFull.json', 'w', 'utf8') as f:
#     		f.write(json.dumps(rhymingDict, sort_keys = True, ensure_ascii=False))				

# print doTheseWordsRhyme('box', 'rocks')


