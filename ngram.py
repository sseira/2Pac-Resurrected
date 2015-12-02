import songClustering 
from collections import Counter
import random
import re
import util
class rapGenerator(util.SearchProblem): #nothing yet bitch but it was a search problem
	def __init__(self, songs, themeWords, songRelevances):
		self.songs = songs
		self.themeWords = themeWords.split(' ')
		self.n = 2 #can change this shit
		self.numLines = 16
		self.songRelevances = songRelevances
		self.nGrams = self.generateAllGrams()

	def getGrams(self):
		return self.nGrams

	def startState(self): #start with no words generated in your sentance 
		keyList = self.nGrams.keys()
		startKey = random.randrange(0, len(keyList))
		current = keyList[startKey]
		state = (current, 0)
		return state

	def isGoal(self, state): #you should end when you have enough lines
		return state[1] >= self.numLines #right now only gets 16 longs

	def succAndCost(self, state): #to implement, but will eventually determine best next choice to make
		cost = 0 #fix this when you have actual costs
		results = []
		nextWord = self.getNextWordFromKey(state[0])
		nextState = (nextWord, state[1] + 1)
		results.append((nextWord, nextState, cost))
		return results

	#Given a song and a relevance factor 
	#returns a dictionary of n-1 words to a list of possible completion words
	def generateNGrams(self, song, relevance):
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
							nGramDict[song[j]] = relevance
							nGrams[nGramTuple] = nGramDict
						else:
							currDict = nGrams[nGramTuple]
							if song[j] in currDict:
								currDict[song[j]] += relevance
							else:
								currDict[song[j]] = relevance
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
			relevance = self.songRelevances[title] #change this to change the relevance
			songNGrams = self.generateNGrams(song, relevance)
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

	def getNextWordFromKey(self, key):
		nGramSum = 0
		possibleEndings = self.nGrams[key]
		for localKey in possibleEndings:
			nGramSum += possibleEndings[localKey]
		randKey = random.uniform(0, nGramSum)
		nGramSum = 0
		for localKey in possibleEndings:
			nGramSum += possibleEndings[localKey]
			if(nGramSum > randKey):
				nextKey = []
				for i in range(1, len(key)):
					nextKey.append(key[i])
				nextKey.append(localKey)
				return tuple(nextKey)	

# This generates sentence 

keywords = 'money cars police gun jail'
songs = songClustering.getSongsForArtist('2pac')
songsFeatureVectors = songClustering.makeSongsFeatureVector(songs)
songRelevances = songClustering.makeSongRelevance(keywords, songs, songsFeatureVectors)
ucs = util.UniformCostSearch(verbose = 0)
ucs.solve(rapGenerator(songs, keywords, songRelevances))
for action in ucs.actions:
	print action[0],
 