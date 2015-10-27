from bs4 import BeautifulSoup
from lxml import html
import json

import requests


def getSoupFromURL(url):
	page = requests.get(url)

	data = page.text

	return BeautifulSoup(data,'lxml')

def writeFile(fileName, data):
	with open(fileName, 'w') as outfile:
    		json.dump(data, outfile)



def scrapeArtist(baseUrl, artist):
	soup = getSoupFromURL(baseUrl+ '/lyrics/' +artist)
	# print soup
	song_links = []

	songs = soup.select('.lyrics-list-item')
	for song in songs:
		link  = song.find_all('a')
		href = link[0]['href']

		new_url = baseUrl+href
		song_links.append(new_url)


	links_title = artist + '_links.json'
	writeFile(links_title, song_links)

	song_list = []
	for url in song_links:
		song_obj = {}
		soup = getSoupFromURL(url)
		title = soup.find('h1').string
		song_obj['title'] = title

		album_div = soup.select('.content-text-album')
		song_div = soup.select('.content-text-inner')

		if album_div:
			album = album_div[0].string
			song_obj['album'] = album
		
		if song_div:
			song_paragraphs = song_div[0]
			song = ""
			for p in song_paragraphs.strings:
				song+= p
			song_obj['lyrics'] = song

		song_list.append(song_obj)
		print title
	lyrics_title = artist + '_lyrics.json'

	writeFile(lyrics_title, song_list)






url = 'http://www.allthelyrics.com'
pac = '2pac'
jayz = 'jayz'
kanye = 'kanye_west'
lil_wayne = 'lil_wayne'
eminem = 'eminem'
scrapeArtist(url, eminem)




# soup.find_all(id='link2')