import json

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






pac = '2pac'
jayz = 'jayz'
kanye = 'kanye_west'
lil_wayne = 'lil_wayne'
eminem = 'eminem'


songs = getSongsForArtist(jayz)
for song in songs: 
	print songs[song]
	featureVector = makeFeatureVectorForSong(songs[song])
	print featureVector
	print ""
	print ""
