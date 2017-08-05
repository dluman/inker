import flickrapi
import json
import random
import requests
import shutil
import sys

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

	def doSearch(self,artbox):
		self.PHOTOS = list()
		flickr = flickrapi.FlickrAPI(self.API_KEY,self.SECRETS,format='json')
		searchStream = json.loads(flickr.photos.search(text=self.SEARCH_TERM,per_page=1000,extras=self.PARAMS))
		photos = searchStream['photos']['photo']

		box_w = artbox[1][0] - artbox[0][0]
		box_h = artbox[1][1] - artbox[0][1]
		for photo in photos:
			try:
				if photo['ispublic'] and photo['url_o']:
					photo_w = int(photo['width_o'])
					photo_h = int(photo['height_o'])
					if photo_w > box_w and photo_h > box_h:
						self.PHOTOS.append(photo['url_o'])
			except: continue #print self.SEARCH_TERM, len(self.PHOTOS), sys.exc_info()
		#print 'Searching %s (%d found)...' % (self.SEARCH_TERM,len(self.PHOTOS))


		try:
			choice = random.choice(self.PHOTOS)
			photo_bin = requests.get(choice, stream=True)
			if photo_bin.status_code == 200:
				filename = str(abs(hash(choice)))
				with open('imgscratch/'+filename+'.jpg','wb') as p:
					photo_bin.raw.decode_content = True
					shutil.copyfileobj(photo_bin.raw,p)
			return 'imgscratch/'+filename+'.jpg'
		except: pass
