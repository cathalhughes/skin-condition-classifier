from PIL import Image
import matplotlib as plt
from pylab import *
import os

	
def close_event():
	plt.close()

def imageFeatureExtraction(fname):
	image = Image.open(fname)
	image.show()
	image = image.convert("L")
	imArray = array(image)
	figure()
	gray()
	contour(image, origin='image')
	axis('equal')
	axis('off')
	figure()
	#hist(imArray.flatten(), 128)
	
	show()

for file in os.listdir("images"):
	imageFeatureExtraction("images/" + file)
