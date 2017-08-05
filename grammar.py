from textblob import TextBlob
from textblob_aptagger import PerceptronTagger

class Entity:

	@staticmethod
	def noun(s):
		pos_list = ['NN','NNS','JJ','VB','VBD','VBG','VBN',
				'VBP','VBZ','RB','RBR','RBS']
		token = TextBlob(s,pos_tagger=PerceptronTagger())
		return [word for word, speech in token.tags if speech in pos_list]
