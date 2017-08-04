import random
import re
import textwrap
from collections import OrderedDict
from PIL import Image, ImageDraw, ImageFont

class Conversions:

	_IMG = None

	def __init__(self,img):
		self._IMG = img

	def bw(self):
		img = self._IMG.convert('1')
		return img

class Cropper:

	_IMG_URL = None
	_X1, _X2 = 0, 0
	_Y1, _Y2 = 0, 0

	def __init__(self,img_url,(x1,y1),(x2,y2)):
		self._IMG_URL = img_url
		self._X1, self._Y1 = (x1,y1)
		self._X2, self._Y2 = (x2,y2)

	def crop(self):
		img = Image.open(self._IMG_URL)
		img = img.crop((0,0,self._X2-self._X1,
				self._Y2-self._Y1))
		img.save(self._IMG_URL)
		return img

class Art:

	_IMG_URLS = None
	_LAYOUT = None

	def __init__(self, img, img_urls):
		self._LAYOUT = img
		self._IMG_URLS = img_urls

	def set(self, artbox):
		paste_up = Image.new('RGBA',(3300,5100),(0,0,0,255))
		layout = self._LAYOUT
		paste_up.paste(self._LAYOUT,(0,0))
		for box in range(len(artbox)):
			x = artbox[box][0][0]
			y = artbox[box][0][1]
			img = Image.open(self._IMG_URLS[box])
			paste_up.paste(img,(x,y))
		return paste_up

class Lettering:

	_FACE = None
	_TYPE = None
	_SIZE = 60

	def makeBox(self, dim, img, lh, iw, ih, next_x, next_y):
		tw,th = dim
		bg = (255,255,153)
		locs = [((iw,ih)),((next_x-(25+tw+self._SIZE),ih)),
			((iw,next_y-(25+th+self._SIZE))),((next_x-(25+tw+self._SIZE),next_y-(25+th+self._SIZE)))]
		loc_x,loc_y = random.choice(locs)
		draw = ImageDraw.Draw(img)
		draw.rectangle([(loc_x,loc_y),
		                (loc_x+(tw+self._SIZE),loc_y+(th+self._SIZE))],
						outline='black',
						fill=bg)
		return img,(loc_x,loc_y)

	def setText(self, img, loc, s, lh):
		lines = 0
		draw = ImageDraw.Draw(img)
		for frag in s:
			draw.text((loc[0]+self._SIZE/2,loc[1]+(self._SIZE/2 + lines)),frag,font=self._TYPE,fill='black')
			lines += lh/len(s)
		return img

	def __init__(self, type):
		self._FACE = type
		self._TYPE = ImageFont.truetype(type,self._SIZE)

	def makeLettering(self, sents, img, artbox):
		def resize(s):
			seed = random.randint(15,25)
			frag = textwrap.wrap(s[0],seed)
			return frag
		sent_id = 0
		next_x, next_y = 0, 0
		for box in artbox:
			s = [sents[sent_id].strip()]
			x = box[0][0]
			y = box[0][1]
			next_x = box[1][0]
			next_y = box[1][1]
			tw, th = self._TYPE.getsize(max(s,key=len))
			if tw > (next_x-x)*.95:
				s = resize(s)
			else:
				sets = [self._TYPE.getsize(frag) for frag in s]
				tw,th = max(sets)
				if len(s) > 1: lh = ((len(s) * th) + self._SIZE)
				else: lh = self._SIZE
				img, loc = self.makeBox((tw,lh),img,lh,x+25,y+25,next_x,next_y)
				img = self.setText(img,loc,s,lh)
			sent_id +=1
		return img
