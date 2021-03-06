import cv2
import random
import re
import textwrap
import numpy
from collections import OrderedDict
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from scipy.misc import imsave

class Conversions:

	_IMG = None

	def __init__(self,img):
		self._IMG = img

	def bw(self):
		img = self._IMG.convert('1')
		return img

class Filters:

	_IMG_URL = None

	def __init__(self,img):
		self._IMG_URL = img

	'''
	This code comes from:
	http://www.geeksforgeeks.org/cartooning-an-image-using-opencv-python/

	It is a slight modification of the effect that the OP was going for.
	'''

	def saturate(self):
		img = cv2.imread(self._IMG_URL)
		steps = 2
		filters = 50
		for _ in xrange(steps):
			img = cv2.pyrDown(img)
		for _ in xrange(filters):
			img = cv2.bilateralFilter(img,9,9,7)
		for _ in xrange(steps):
			img = cv2.pyrUp(img)
		img_bw = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
		img_bl = cv2.medianBlur(img_bw,3)
		edges = cv2.adaptiveThreshold(img_bl,255,
						cv2.ADAPTIVE_THRESH_MEAN_C,
						cv2.THRESH_BINARY,5,2)
		(x,y,z) = img.shape
		edges = cv2.cvtColor(edges,cv2.COLOR_GRAY2RGB)
		img = cv2.bitwise_and(img,edges)
		cv2.imwrite(self._IMG_URL,img)

	'''
	This code comes from:
	https://stackoverflow.com/questions/9506841/using-python-pil-to-turn-a-rgb-image-into-a-pure-black-and-white-image

	The answer which proposed this solution is further down the page as it is, surprisingly, not the accepted answer.
	'''

	def halftone(self):
		def imgArray(a,t):
			for i in range(len(a)):
				for j in range(len(a[0])):
					if a[i][j] > t:
						a[i][j] = 255
					else:
						a[i][j] = 0
			return a
		img = Image.open(self._IMG_URL)
		img = img.convert('L')
		img = numpy.array(img)
		img = imgArray(img,110)
		imsave(self._IMG_URL, img)

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
		try: img.save(self._IMG_URL)
		except: pass
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
	_SIZE = 50
	_INDEX = 0
	_BOXES = list()

	def isOverprint(self,x1,y1,x2,y2):
		oprint = False
		def overprint(dim1_min,dim1_max,dim2_min,dim2_max):
			return (dim1_min <= dim2_max) and (dim2_min <= dim1_max)
		for box in self._BOXES:
			dx1, dy1 = box[0][0], box[0][1]
			dx2, dy2 = box[1][0], box[1][1]
			oprint = overprint(dx1,x1,dx2,x2) and overprint(dy2,y2,dy1,y1)
		return oprint

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
		self._BOXES.append( ((loc_x,loc_y) , (loc_x+(tw+self._SIZE),loc_y+(th+self._SIZE))) )
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
		isPrinted = True
		next_x, next_y = 0, 0
		for box in artbox:
			if len(artbox) >= 3: isPrinted = bool(random.getrandbits(1))
			if isPrinted:
				s = [sents[self._INDEX].strip()]
				print "SHOULD PRINT: %s" % s
				x = box[0][0]
				y = box[0][1]
				next_x = box[1][0]
				next_y = box[1][1]
				tw, th = self._TYPE.getsize(max(s,key=len))
				if tw > (next_x-x)*.90:
					s = resize(s)
				sets = [self._TYPE.getsize(frag) for frag in s]
				tw,th = max(sets)
				if len(s) > 1: lh = ((len(s) * th) + self._SIZE)
				else: lh = self._SIZE
				if self.isOverprint(x+25,y+25,next_x,next_y): continue
				else: img, loc = self.makeBox((tw,lh),img,lh,x+25,y+25,next_x,next_y)
				img = self.setText(img,loc,s,lh)
			self._INDEX +=1
		return img
