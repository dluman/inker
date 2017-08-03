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
