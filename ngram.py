import songClustering 
from collections import Counter
import random
import re
import util
import copy
class rapGenerator(util.SearchProblem): #nothing yet bitch but it was a search problem
	def __init__(self, songs, themeWords):
		self.songs = songs
		self.themeWords = themeWords.split(' ')
		self.n = 3 #can change this shit
		self.numLines = 2
		self.lineLength = 10 #eventually be the average number of words in a line
		self.nGrams = self.generateAllGrams()

	def getGrams(self):
		return self.nGrams

	#state is represented by:
	#the previous n-1 words
	#the total number of lines
	#whether we're in the first line or not (boolean)
	#how many words we have in the current line
	def startState(self): #start with no words generated in your sentance 
		keyList = self.nGrams.keys()
		startKey = random.randrange(0, len(keyList))
		current = keyList[startKey]
		state = (current, 0, False, 0)
		return state


	def isGoal(self, state): #you should end when you have enough lines
		return state[1] >= self.numLines #right now only gets 16 longs

	#Given a current state (which consists of the previous n-1 words, total num lines, whether we're in the first line, and num words in current line)
	#Looks at all possible successor words 
	def succAndCost(self, state): #to implement, but will eventually determine best next choice to make
		if(state[3] == self.lineLength):
			currentLineLength = 0
			numLines = state[1] + 1
			secondLine = not state[2]
		else: 
			currentLineLength = state[3] + 1
			numLines = state[1]
			secondLine = False
		cost = 0 #fix this when you have actual costs
		results = []
		wordsAndWeights = self.getNextWordFromKey(state[0]) #shifts the next window
		for wordAndWeight in wordsAndWeights:
			nextWord = wordAndWeight[0]
			cost = wordAndWeight[1]
			if(not self.wordsRhyme(state[self.n - 2], nextWord[self.n - 2])):
				cost += 100000
			nextState = (nextWord, numLines, secondLine, currentLineLength) #change this to update the line bool etc.
			results.append((nextWord, nextState, cost))

		return results

	def wordsRhyme(self, word1, word2):
		return True

	def getNextWordFromKey(self, key):
		nGramSum = 0
		endingsAndWeights = []
		possibleEndings = self.nGrams[key]
		nextKey = []
		for localKey in possibleEndings:
			nGramSum += possibleEndings[localKey]
		for i in range(1, len(key)):
			nextKey.append(key[i])
		for localKey in possibleEndings:
			weight = float(possibleEndings[localKey]) / nGramSum
			tempKey = copy.deepcopy(nextKey)
			tempKey.append(localKey)
			if(tuple(tempKey) in self.nGrams):
				endingsAndWeights.append((tuple(tempKey), weight))
		return endingsAndWeights
		# 	nGramSum += possibleEndings[localKey]
		# randKey = random.uniform(0, nGramSum)
		# nGramSum = 0
		# for localKey in possibleEndings:
		# 	nGramSum += possibleEndings[localKey]
		# 	if(nGramSum > randKey):
		# 		nextKey = []
		# 		for i in range(1, len(key)):
		# 			nextKey.append(key[i])
		# 		nextKey.append(localKey)
		# 		return tuple(nextKey)	
	#Given a song and a relevance factor 
	#returns a dictionary of n-1 words to a list of possible completion words
	def generateNGrams(self, song):
		nGrams = {}
		length = len(song)
		wrapAround = []
		for i, word in enumerate(song):
			if(i < self.n):
				wrapAround.append(word) # YO FIX THIS OTHERWISE SMALL BUG
			nGram = []
			for j in range(i, i + self.n):
				if(j < length):
					if(j == i + self.n - 1):
						nGramTuple = tuple(nGram)
						if(nGramTuple not in nGrams):
							nGramDict = {}
							nGramDict[song[j]] = 1
							nGrams[nGramTuple] = nGramDict
						else:
							currDict = nGrams[nGramTuple]
							if song[j] in currDict:
								currDict[song[j]] += 1
							else:
								currDict[song[j]] = 1
							nGrams[nGramTuple] = currDict
					else:
						nGram.append(song[j])
		return nGrams

    #Given all the songs, goes through each, generates ngrams for each
    #Then adds all ngrams to each other to generate a total ngram model
	def generateAllGrams(self):
		totalNGrams = {}
		for title in self.songs:
			song = re.split(' |\n', self.songs[title])
			# relevance = getSongRelevance(song, self.themeWords)
			# relevance = self.songRelevances[title] #change this to change the relevance
			songNGrams = self.generateNGrams(song)
			for key in songNGrams:
				if key not in totalNGrams:
					totalNGrams[key] = songNGrams[key]
				else:
					totalNGrams[key] = dict(Counter(totalNGrams[key]) + Counter(songNGrams[key]))
		return totalNGrams

	#Generates raps (out)
	def generateRaps(self, nGrams):
		keyList = nGrams.keys()
		startKey = random.randrange(0, len(keyList))
		current = keyList[startKey]
		bars = []
		for word in current:
			bars.append(word)
		for _ in range(self.numLines):
			next = self.getNextWordFromKey(current, nGrams)
			bars.append(next[len(next) - 1])
			current = next
		print " ".join(bars)

pac = '2pac'
jayz = 'jayz'
kanye = 'kanye_west'
lil_wayne = 'lil_wayne'
eminem = 'eminem'

# This generates sentence 
lineLength = 10
keywords = 'money cars police gun jail'
songs = {}
songs.update(songClustering.getSongsForArtist(pac))
# songs.update(songClustering.getSongsForArtist(jayz))
# songs.update(songClustering.getSongsForArtist(kanye))
# songs.update(songClustering.getSongsForArtist(lil_wayne))
# songs.update(songClustering.getSongsForArtist(eminem))
correlationMatrix = songClustering.makeCorrelationValuesForKeyWord(songs, keywords)
#print correlationMatrix
ucs = util.UniformCostSearch(verbose = 0)
ucs.solve(rapGenerator(songs, keywords))
for i, action in enumerate(ucs.actions):
	print action[0],
	# if((i + 1) % lineLength == 0):
	# 	print "\n"
 # 