from collections import Counter
class rapGenerator(): #nothing yet bitch
	def __init__(self, songs, themeWords):
		self.songs = songs
		self.themeWords = themeWords
		self.n = 2 #can change this shit

	def startState(self):
		return []

	def isGoal(self, state): 
		return state.length >= 16 #right now only gets 16 longs

	def succAndCost(self, state):
		return


	def generateNGrams(self, song, relevance):
		nGrams = {}
		length = len(self.song)
		for i, word in enumerate(self.song):
			nGram = []
			for j in range(i + 1, i + 1 + self.n):
				if(i < length):
					nGram.append(self.song[j])
			if(nGrams[word] == None):
				nGrams[word] = {nGram: relevance}
			else:
				tempDict = nGrams[word]
				print tempDict
		return nGrams

	def generateAllGrams(self):
		totalGrams = {}
		for song in self.song:
			#relevance = getSongRelevance(song, self.themeWords)
			relevance = 1
			songNGram = generateNGrams(song, relevance)
			#totalGrams = dict(Counter(totalGrams) + Counter(songNGram)) #gonna chance with relevance 
		return totalNGrams

themeWords = ["boat"]
generator = rapGenerator(themeWords)
