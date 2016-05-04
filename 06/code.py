# run strings on png, find out it's a piet program, inspect the image closely, remove all doubts 
from PIL import Image
from PIL import ImageOps
img = Image.open('alice_shocked.png')
mirror = ImageOps.mirror(img)
mirror.save("mirror.png")
#submit mirror.png to http://www.bertnase.de/npiet/npiet-execute.php
