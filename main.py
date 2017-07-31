import random
from rendering import Lettering, Conversions
from corpus import File, Textops
from layouts import Page

img, artbox = Page((3300,5100)).make(random.randint(1,8))
img = Lettering('type/animeace.ttf').makeLettering(['A test with some longer text.'],img,artbox)
img.save('layouts/test.png')
