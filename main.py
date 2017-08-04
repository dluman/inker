import random
import string
from rendering import Art, Lettering, Conversions, Cropper
from corpus import File, Textops
from layouts import Page
from sourcerer import PhotoSearch


'''
To Do

Do cropping: see http://matthiaseisen.com/pp/patterns/p0202/
BUT! Somehow, need to ensure that the image is an appropriate size (e.g. not smaller than the artbox to which it belongs. This goes in sourcerer.

'''

img_urls = list()

text = File.read('text/montecarlo.txt')
sentences = Textops.sentences(text)
random.shuffle(sentences)

for layouts in range(10):

	panel_no = random.randint(1,8)
	narrative = sentences[0:panel_no]
	exclude = set(string.punctuation)

	img, artbox = Page((3300,5100)).make(panel_no)

	for p in range(panel_no):
		w = random.choice(narrative[p].strip().split(' '))
		img_urls.append(PhotoSearch(''.join([ch for ch in w if ch not in exclude])).doSearch())
	for i in range(len(img_urls)):
		Cropper(img_urls[i],artbox[i][0],artbox[i][1]).crop()
	img = Art(img,img_urls).set(artbox)
	img = Lettering('type/animeace.ttf').makeLettering(narrative,img,artbox)
	img.save('layouts/test'+str(layouts+1)+'.jpg')
	img_urls = list()
