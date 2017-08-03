import random
from rendering import Lettering, Conversions
from corpus import File, Textops
from layouts import Page

text = File.read('text/montecarlo.txt')
sentences = Textops.sentences(text)
random.shuffle(sentences)
panel_no = random.randint(1,8)
narrative = sentences[0:panel_no]

img, artbox = Page((3300,5100)).make(panel_no)
img = Lettering('type/animeace.ttf').makeLettering(narrative,img,artbox)
img.save('layouts/test.png')
