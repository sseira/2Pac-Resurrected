import songClustering 
from collections import Counter
import random
import string, timeit
import util
import copy
import rhymingSauce
import re
class rapGenerator(util.SearchProblem): #nothing yet bitch but it was a search problem
	def __init__(self, songs, themeWords, correlationMatrix):
		print "start initializing"
		self.songs = songs
		self.themeWords = themeWords
		self.n = 3 #can change this shit
		self.numLines = 2
		self.maxLineLength = lineLength #eventually be the average number of words in a line
		self.nGrams = self.generateAllGrams()
		self.rhymingDict = rhymingSauce.readRhymingDict()
		self.correlationMatrix = correlationMatrix
		print "Done initializing"
	def getGrams(self):
		return self.nGrams

	#state is represented by:
	#the previous n-1 words
	#the total number of lines
	#whether we're in the second line or not (boolean)
	#how many words we have in the current line
	#word to rhyme
	def startState(self): #start with no words generated in your sentance
		keyList = self.nGrams.keys()
		startKey = random.randrange(0, len(keyList))
		current = keyList[startKey]
		state = (current, 0, 0, None)

		return state


	def isGoal(self, state): #you should end when you have enough lines
		return state[1] >= self.numLines #right now only gets 16 longs

	#Given a current state (which consists of the previous n-1 words, total num lines, whether we're in the second line, and num words in current line)
	#Looks at all possible successor words 
	def succAndCost(self, state): #to implement, but will eventually determine best next choice to make
		#print state[3]
		currentWords = state[0]
		currentNumLines = state[1]
		currentLineLength = state[2]
		wordToRhyme = state[3]

		atLastWord = False
		rhymingCost = 0
		coherentCost = 0
		shouldCheckRhyme = False

		heuristic = (self.maxLineLength*self.numLines - (currentNumLines*self.maxLineLength + currentLineLength))


		if currentLineLength == self.maxLineLength - 2 : #is the last word in the line ... 5 words ->{1,2,3,4, ...}
			atLastWord = True
			if currentNumLines%2 == 0: # were in line 0,2,4,6 (i.e. we should CHOOSE the rhyming word here)
				shouldCheckRhyme = False
			else: #i.e. we should CHECK the word we have with the rhyming Word we chose last line
				shouldCheckRhyme = True # we just chose a word 


		if currentLineLength == self.maxLineLength - 1 : #we're at the end of the line and want to reset lineLength
			currentLineLength = 0
			currentNumLines = currentNumLines + 1
		else: #we just want to add one word
			currentLineLength = currentLineLength + 1

		cost = 0 #fix this when you have actual costs
		results = []
		wordsAndWeights = self.getNextWordFromKey(currentWords) #shifts the next window

		for wordAndWeight in wordsAndWeights:
			nextWord = wordAndWeight[0]
			cost = wordAndWeight[1]
			#print cost
			if(atLastWord):
				if(not shouldCheckRhyme): #we're setting the word to rhyme to be the word we're about to choose
					wordToRhyme = nextWord[self.n - 2]
				else: #we're checking whether the two words rhyme
					#print "checking words?"
					if not rhymingSauce.doTheseWordsRhyme(wordToRhyme, nextWord[self.n - 2], self.rhymingDict):
						#print "not rhyme"
						cost += 1000
						# nextState = (nextWord, currentNumLines, currentLineLength, wordToRhyme) #change this to update the line bool etc.
						# results.append((nextWord, nextState, cost))
			nextState = (nextWord, currentNumLines, currentLineLength, wordToRhyme) #change this to update the line bool etc.
			results.append((nextWord, nextState, cost))

		return results

	def relevanceWeight(self, newWord):
		relevance = 1
		found = False
		for keyword in self.correlationMatrix:
			if newWord in self.correlationMatrix[keyword]:
				# print "relevance->",newWord ,self.correlationMatrix[keyword][newWord]
				relevance+=self.correlationMatrix[keyword][newWord]
				found = True
		if not found:
			print "not found->", newWord
		return relevance

	def normalizeDenominatorValue(self, possibleEndings, nGramSum):
		totalSum = 0
		for localKey in possibleEndings:
			cost = float(possibleEndings[localKey]) / nGramSum
			cost *= self.relevanceWeight(localKey)
			totalSum += cost
		return totalSum

	def normalizeRelevanceCost(self, cost, newWord, normalizeDenominator):
		return cost*self.relevanceWeight(newWord)/normalizeDenominator

	def getNextWordFromKey(self, key):
		nGramSum = 0
		endingsAndWeights = []
		possibleEndings = self.nGrams[key]
		nextKey = []
		finalKey = key[-1]
		for localKey in possibleEndings:
			nGramSum += possibleEndings[localKey]

		normalizeDenominator = self.normalizeDenominatorValue(possibleEndings, nGramSum)

		for i in range(1, len(key)):
			nextKey.append(key[i])
		for localKey in possibleEndings:
			#cost = float(possibleEndings[localKey]) / nGramSum
			cost = 1
			cost = self.normalizeRelevanceCost(cost, localKey, normalizeDenominator)
			tempKey = copy.deepcopy(nextKey)
			tempKey.append(localKey)
			if(tuple(tempKey) in self.nGrams):
				endingsAndWeights.append((tuple(tempKey), cost))
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
			# word = re.sub(ur"\p{P}+", "", word)
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
lineLength = 8
keywords = ['money']
songs = {}
songs.update(songClustering.getSongsForArtist(pac))
# songs.update(songClustering.getSongsForArtist(jayz))
# songs.update(songClustering.getSongsForArtist(kanye))
# songs.update(songClustering.getSongsForArtist(lil_wayne))
# songs.update(songClustering.getSongsForArtist(eminem))
correlationMatrix = songClustering.makeCorrelationValuesForKeyWord(songs, keywords)
# f = open("correlationMatrix.txt",'r+')
# f.write(str(correlationMatrix))
ucs = util.UniformCostSearch(verbose = 0)
ucs.solve(rapGenerator(songs, keywords, correlationMatrix))
for i, action in enumerate(ucs.actions):
	print action[0],
	if((i + 1) % (lineLength) == 0):
		print "\n"
 # 