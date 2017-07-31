import re

class File:

	@staticmethod
	def read(filename):
		with open(filename,'rb') as f:
			contents = f.read()
		return contents

class Textops:

	@staticmethod
	def sentences(text):
		pass
