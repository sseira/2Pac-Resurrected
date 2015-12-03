import rapScraper5000
import codecs, json

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
	
	rapScraper5000.writeFile("RhymingDict.json", rhymingDict)


def doTheseWordsRhyme(word, word2):
	with open("RhymingDict.json") as data_file:    
		rhymingDict = json.load(data_file)
		return rhymingDict[word.upper()] == rhymingDict[word2.upper()]


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


