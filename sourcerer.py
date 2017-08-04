import flickrapi
import json
import random
import requests
import shutil
import webbrowser

class PhotoSearch:

	'''
	Wait for the right time to flash them keys.
	'''

	API_KEY = None
	SECRETS = None
	PHOTOS = list()
	FLICKR_GNE = 'http://flickr.com/photo.gne?id='
	PARAMS = 'url_sq,url_t,url_s,url_q,url_m,url_n,url_z,url_c,url_l,url_o'
	SEARCH_TERM = None

	def __init__(self,term):
		self.SEARCH_TERM = term
	        with open('api/flickr_keys') as f:
        	        auth = json.load(f)
		self.API_KEY = auth['key']
		self.SECRETS = auth['secret']


	def doSearch(self):
		flickr = flickrapi.FlickrAPI(self.API_KEY,self.SECRETS,format='json')
		searchStream = json.loads(flickr.photos.search(text=self.SEARCH_TERM,per_page=10,extras=self.PARAMS))
		photos = searchStream['photos']['photo']

		for photo in photos:
			try:
				if photo['ispublic'] and photo['url_o']:
					if photo['width_o'] >= 3300 and photo['height_o'] >=5100: self.PHOTOS.append(photo['url_o'])
			except: continue

		choice = random.choice(self.PHOTOS)
		photo_bin = requests.get(choice, stream=True)
		if photo_bin.status_code == 200:
			with open('imgscratch/'+self.SEARCH_TERM+'.jpg','wb') as p:
				photo_bin.raw.decode_content = True
				shutil.copyfileobj(photo_bin.raw,p)
		return 'imgscratch/'+self.SEARCH_TERM+'.jpg'
