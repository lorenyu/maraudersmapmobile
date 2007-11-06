import appuifw, colorMod
from graphics import *

class Map:
	
	def __init__(self):
		self.image = Image.open("C:\\Data\\Images\\tressider-lowquality.jpg")
		# read this in from text file - can eval(text), and then have a dictionary
		f = file(u"C:\\Data\\Others\\tressider2-coords.txt", "r")
		str = ""
		for line in f:
			str += line.strip()
		f.close()
		mapCoords = eval(str)		
		self.coords = mapCoords
		