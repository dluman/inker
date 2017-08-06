import PyPDF2
import random
from PIL import Image, ImageDraw

class Page:

	_SIZE = None
	_MARGIN = None
	_PADDING = None
	_BORDER = 25
	_MAXCOLS = 4
	_MAXROWS = 4

	def __init__(self,size):
		self._SIZE = size
		self._MARGIN = 300
		self._PADDING = None

	def gridify(self,grid):
		rows, cols = [], []
		space = (self._SIZE[0]-self._MARGIN/2, self._SIZE[1]-self._MARGIN/2)
		for col in grid:
			origin, offset = self._MARGIN/4, 0
			if col > 1: self._PADDING = 0
			else: self._PADDING = 0
			col_size = space[0]/col
			for x in range(col):
				origin += offset
				if x < range(col): rows.append( (origin,origin+col_size) )
				offset = (origin+col_size) - origin + self._PADDING
			cols.append(rows)
			rows = []
		origin, offset = self._MARGIN/4, 0
		for row in range(len(grid)):
			row_size = space[1]/len(grid)
			origin += offset
			rows.append( (origin,origin+row_size) )
			offset = (origin + row_size) - origin
		return rows,cols

	def divisions(self,n):
		def sum_to_n(n, size, limit=None):
    			if size == 1 or n == 1:
        			yield [n]
        			return
    			if limit is None:
        			limit = n
    			start = (n + size - 1) // size
    			stop = min(limit, n - size + 1) + 1
    			for i in range(start, stop):
        			for tail in sum_to_n(n - i, size - 1, i):
					yield [i] + tail
		num_rows = 0
		while num_rows == 0 or num_rows > n:
			num_rows = random.randint(1,self._MAXROWS)
		try:
			grids = [grid for grid in sum_to_n(n,num_rows) if max(grid) <= self._MAXCOLS-1]
			grid = random.choice(grids)
			random.shuffle(grid)
		except IndexError: self.divisions(n)
		return grid

	def draw(self, rows, cols, img):
		artbox = []
		d = ImageDraw.Draw(img)
		for r in range(len(rows)):
			for col in cols[r]:
				x1,y1 = col[0],rows[r][0]
				x2,y2 = col[1],rows[r][1]
				#BOUNDING BOX
				d.rectangle([(x1,y1),(x2,y2)],outline='black',fill='black')
				#ARTBOX
				d.rectangle([(x1+self._BORDER,y1+self._BORDER),
						(x2-self._BORDER,y2-self._BORDER)],
						outline='black',fill='white')
				artbox.append([(x1+self._BORDER,y1+self._BORDER),(x2-self._BORDER,y2-self._BORDER)])
		return img, artbox

	def make(self,n):
		grid = self.divisions(n)
		rows,columns = self.gridify(grid)
		img = Image.new('RGB',self._SIZE)
		img, artbox = self.draw(rows,columns,img)
		#img.save('layouts/test.png')
		return img, artbox
