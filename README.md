# 2Pac-Resurrected

###File Structure




<b>ngram.py</b> -> main file that generates raps using an n-gram model influenced by song relevance according to keywords
<b>rapScraper5000.py</b> -> scrapes song lyrics for chosen artists from allthelyrics.com and stores them as json files
<b>songClustering.py</b> -> calculates song relevance for every song based on keywords by creating feature vectors based on the frequency of word occurences for songs and taking the dot product of the feature vectors of 2 songs to calculate distance/relvance between 2 songs

<b>xx_lyrics.json</b> -> stores the song objects for every song for artist xx (song title - album name - lyrics)
<b>xx_links.json</b> -> stores the urls for the artist xx song lyrics (not used, but could be useful in future)





####Explain the code you wrote, plans for next steps, random ideas here:
  
  Step 1) Get data    **** Done **** <br>
  Step 2) Create a basic n-grams  **** Done **** <br>
  Step 3) Create a way to influence n-grams based on key word **** Done **** <br>
  Step 4) Tweak weights/influence of song relevance
  Step 5) Make it a search problem
