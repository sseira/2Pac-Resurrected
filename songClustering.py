import json
import Queue 


def getSongsForArtist(artist):
	file_name = artist + '_lyrics.json'
	songs = {}
	with open(file_name) as data_file:    
    		data = json.load(data_file)
    	for song_obj in data:
    		# must take out 'lyrics' in song title
    		songs[song_obj['title']] = song_obj['lyrics']
    	return songs

def makeFeatureVectorForSong(song):
	featureVector = {}
	for word in song.split(" "):
		# clean up words a bit, make alpha only 
		if word in featureVector:
			featureVector[word] += 1
		else:
			featureVector[word] = 1
	return featureVector

def songDistance(featureVector1, featureVector2):
	dotProduct = 0.0
	for feature1 in featureVector1:
		for feature2 in featureVector2:
			if feature1 == feature2:
				dotProduct += featureVector1[feature1] * featureVector2[feature2]

	return dotProduct


def makeSongsFeatureVector(songs):
	songsFeatureVectors = {}
	for song in songs: 
		featureVector = makeFeatureVectorForSong(songs[song])
		songsFeatureVectors[song] = featureVector	
	return songsFeatureVectors



# how to do rank lowering? is it necessary?
# synonymy ?? best way to do that?
def makeDocumentTermMatrix(songs):
	docTermMatrix = {}
	songTitleList = []
	for title in songs:
		songTitleList.append(title)
		for word in songs[title].split(" "):
			if word not in docTermMatrix:
				docTermMatrix[word] = {} # every word in every song is a key in the docTermMatrix

			if title in docTermMatrix[word]: # appearances of word in song
				docTermMatrix[word][title] +=1
			else:
				docTermMatrix[word][title] = 1
	return docTermMatrix


#Now the dot product t_i, t_p between two term vectors gives the correlation between the terms over the documents. 
#The matrix product X X^T contains all these dot products. 
#Element (i,p) (which is equal to element (p,i)) contains the dot product t_i, t_p = t_p, t_i. 
def makeCorrelationValuesForKeyWord(songs, keywords):
	docTermMatrix = makeDocumentTermMatrix(songs)
	correlationMatrix = {}

	for keyword in keywords: # going down the rows 
		if keyword in docTermMatrix: # keyword appears in any song
			correlationMatrix[keyword] = {}
			termVec = docTermMatrix[keyword]
			for word in docTermMatrix:				
				termVec2 = docTermMatrix[word]
				correlationMatrix[keyword][word] = dotProduct(termVec, termVec2)

	return correlationMatrix
		#dot product with everyother word


def dotProduct(termVec, termVec2):
	dotProduct = 0
	for key in termVec:
		if key in termVec2:
			dotProduct+= termVec[key]*termVec2[key]
	return dotProduct

def makeSongRelevance(keywords, songs, songsFeatureVectors):
	keywordFeatureVector = makeFeatureVectorForSong(keywords)

	# return idealSongs which are the songs that best match with keywords
	# idealSongs will be used as a reference to rate other songs 
	def getIdealSongs(maxIdealSongs = 4):
		idealSongs = Queue.PriorityQueue()
		# minIdealDistance = None
		for song in songs:
			distance = songDistance(keywordFeatureVector, songsFeatureVectors[song])
			if idealSongs.qsize() < maxIdealSongs:
				idealSongs.put((distance, song))
			else:
				lowest = idealSongs.get()
				if lowest[0] < distance:
					idealSongs.put((distance, song))
				else:
					idealSongs.put(lowest)		

		#normalize weights
		minWeight = None
		maxWeight = None
		idealSongsDict = {}
		# print idealSongsDict
		while not idealSongs.empty():
				weight, song = idealSongs.get()
				if minWeight is None:
					minWeight = weight
				maxWeight = weight	
				idealSongsDict[song] = weight

		for song in idealSongsDict:
			normalizedWeight = (idealSongsDict[song] - minWeight)/(maxWeight - minWeight)
			idealSongsDict[song] = normalizedWeight + 2 # range [2:3]
		
		return idealSongsDict


	idealSongs = getIdealSongs()
	songRelevances = {}
	minRelevance = float('inf')
	maxRelevance = float('-inf')
	for title in songs:
		relevance = 0
		for idealTitle in idealSongs:
			distance = songDistance(songsFeatureVectors[idealTitle], songsFeatureVectors[title])
			relevance += distance*idealSongs[idealTitle]

		songRelevances[title] = relevance
		
		if relevance > maxRelevance:
			maxRelevance = relevance
		if relevance < minRelevance:
			minRelevance = relevance

	for title in songRelevances:
 		normalizedWeight = (songRelevances[title] - minRelevance)/(maxRelevance - minRelevance)
 		songRelevances[title] = normalizedWeight + 1 # range [1:2]

	return songRelevances



pac = '2pac'
jayz = 'jayz'
kanye = 'kanye_west'
lil_wayne = 'lil_wayne'
eminem = 'eminem'
keywords = ['police', 'guns', 'money', 'gun', 'bullet']

# songs = getSongsForArtist(jayz)
# values = makeCorrelationValuesForKeyWord(songs, keywords)

	
