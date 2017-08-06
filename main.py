import random
import string
import sys
import traceback
from subprocess import call
from grammar import Entity
from rendering import Art, Lettering, Conversions, Cropper, Filters
from corpus import File, Textops
from layouts import Page
from sourcerer import PhotoSearch
from publish import Publish

print "DELETING IMAGE CACHE"
try:
	call('rm imgscratch/*.jpg',shell=True)
	print "OK"
except: print "FAILED"
print "DELETING LAYOUT CACHE"
try:
	call('rm layouts/*.jpg', shell=True)
	print "OK"
except: print "FAILED"

img_urls = list()

text = File.read('text/source.txt')
sentences = Textops.sentences(text)

for layouts in range(10):
	random.shuffle(sentences)
	panel_no = random.randint(1,8)
	narrative = sentences[0:panel_no]
	exclude = set(string.punctuation)

	img, artbox = Page((3300,5100)).make(panel_no)

	for p in range(panel_no):
		try: w = random.choice(Entity.noun(narrative[p]))
		except IndexError: pass #print narrative[p]
		img_urls.append(PhotoSearch(''.join([ch for ch in w if ch not in exclude])).doSearch(artbox[p]))
	try:
		for i in range(len(img_urls)):
			Cropper(img_urls[i],artbox[i][0],artbox[i][1]).crop()
			Filters(img_urls[i]).saturate()
			#Filters(img_urls[i]).halftone()
		img = Art(img,img_urls).set(artbox)
		img = Lettering('type/animeace.ttf').makeLettering(narrative,img,artbox)
		img.save('layouts/test'+str(layouts+1)+'.jpg')
		print 'GENERATED: PAGE #%s' % str(layouts+1)
	except: print sys.exc_info()[0], traceback.print_tb(sys.exc_info()[2])
	img_urls = list()
