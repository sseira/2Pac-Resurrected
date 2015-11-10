from songClustering import getSongsForArtist
from collections import Counter
import random
import re
class rapGenerator(): #nothing yet bitch but it was a search problem
	def __init__(self, songs, themeWords):
		self.songs = songs
		self.themeWords = themeWords
		self.n = 3 #can change this shit

	def startState(self):
		return []

	def isGoal(self, state): 
		return state.length >= 16 #right now only gets 16 longs

	def succAndCost(self, state):
		return


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
		# for i, word in enumerate(wrapAround):

		# for key in nGrams:
		# 	print (key, nGrams[key])
		return nGrams

	def generateAllGrams(self):
		totalNGrams = {}
		for title in self.songs:
			song = re.split(' |\n', self.songs[title])
			#relevance = getSongRelevance(song, self.themeWords)
			relevance = 1
			songNGrams = self.generateNGrams(song, relevance)
			for key in songNGrams:
				if key not in totalNGrams:
					totalNGrams[key] = songNGrams[key]
				else:
					totalNGrams[key] = dict(Counter(totalNGrams[key]) + Counter(songNGrams[key]))
			# for word in totalNGrams:
			# 	print (word, totalNGrams[word])
		return totalNGrams

	def generateRaps(self, nGrams):
		keyList = nGrams.keys()
		startKey = random.randrange(0, len(keyList))
		current = keyList[startKey]
		bars = []
		for word in current:
			bars.append(word)
		for i in range(16):
			# print i, current
			next = self.getNextWordFromKey(current, nGrams)
			bars.append(next[len(next) - 1])
			current = next
		print bars

	def getNextWordFromKey(self, key, nGrams):
		nGramSum = 0
		possibleEndings = nGrams[key]
		for localKey in possibleEndings:
			nGramSum += possibleEndings[localKey]
		randKey = random.randrange(0, nGramSum)
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
# themeWords = ["boat"]
# songs = getSongsForArtist('jayz')
# generator = rapGenerator(songs, themeWords)
# allWords = generator.generateAllGrams()
# generator.generateRaps(allWords)
