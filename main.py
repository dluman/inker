import random
from rendering import Lettering, Conversions
from corpus import File, Textops
from layouts import Page

img, artbox = Page((3300,5100)).make(random.randint(1,8))
prev_w, prev_h, index = 0, 0, 0
for box in artbox:
	#w, h = (box[1][0]-box[0][0]), (box[1][1]-box[0][1]+prev_h)+50
	w, h = (box[0][0]),(box[0][1]+prev_h)+50
	if prev_h != h: prev_h = h
	if index < len(box): prev_w += w
	img = Lettering('type/animeace.ttf').makeLettering(['A test with some longer text.'],img,w,h)
	index += 1
img.save('test.png')
