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

	def makeBox(self, dim, img, lh, iw, ih):
		#iw,ih = img.size
		tw,th = dim
		bg = (255,255,153)
		#locs = [((iw*.06),(ih*.06)),
		#        ((iw*.985)-(tw+self._SIZE),(ih*.06)),
		#	((iw*.06),(ih*.90)-(lh)),
		#	((iw*.985)-(tw+self._SIZE),(ih*.90)-(lh)),
		#	((iw*.06),(ih*.50)),
		#	((iw*.985)-(tw+self._SIZE),(ih*.50))]
		locs = [((iw*.06+tw+self._SIZE,ih*.90-(lh)))]
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

	#def makeLettering(self, s, img):
	#	def resize(s):
	#		seed = random.randint(15,25)
	#		frag = textwrap.wrap(s[0],seed)
	#		return frag
	#	iw,ih = img.size
	#	tw, th = self._TYPE.getsize(max(s,key=len))
	#	if tw > (iw-(iw*.025)):
	#		s = resize(s)
	#		self.makeLettering(s,img)
	#	else:
	#		sets = [self._TYPE.getsize(frag) for frag in s]
	#		tw,th = max(sets)
	#		if len(s) > 1: lh = ((len(s) * th) + self._SIZE)
	#		else: lh = self._SIZE
	#		img,loc = self.makeBox((tw,lh),img,lh)
	#		img = self.setText(img,loc,s,lh)
	#	return img


	def makeLettering(self, s, img, iw,ih):
		def resize(s):
			seed = random.randint(15,25)
			frag = textwrap.wrap(s[0],seed)
			return frag
		tw, th = self._TYPE.getsize(max(s,key=len))
		if tw > (iw):
			s = resize(s)
			self.makeLettering(s,img,iw,ih)
		else:
			sets = [self._TYPE.getsize(frag) for frag in s]
			tw,th = max(sets)
			if len(s) > 1: lh = ((len(s) * th) + self._SIZE)
			else: lh = self._SIZE
			img,loc = self.makeBox((tw,lh),img,lh,iw,ih)
			img = self.setText(img,loc,s,lh)
		return img
