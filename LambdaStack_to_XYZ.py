#Take spectral image data and transform into XYZ tristumulus Space

from ij import IJ, ImagePlus
from ij.plugin import ImageCalculator
from ij.process import ImageProcessor
from ij.process import FloatProcessor
from fiji.util.gui  import GenericDialogPlus
import ij.plugin.PlugIn
import math

#Input parameters
gd = GenericDialogPlus("Input Parameters")  
gd.addNumericField("Wavlength Spacing (nm)", 2, 0)  # show 3 decimals
gd.addNumericField("Starting Wavelength (nm)", 393, 0)  # show 3 decimals
gd.addNumericField("Ending Wavelength (nm)", 750, 0)  # show 3 decimals 
gd.showDialog()  

spacing = int(gd.getNextNumber())  
start_wave = int(gd.getNextNumber())  
end_wave = int(gd.getNextNumber()) 

lim = (end_wave-start_wave)/spacing

#color matching functions
def red():

	a0=0.2817
	a1=-0.3183
	b1=-0.07613
	a2=0.1517
	b2=0.2493
	a3=-0.09975
	b3=-0.09847
	a4=-0.02849
	b4=0.01255
	a5=0.01489 
	b5=-0.01755
	a6=-0.005536
	b6=-0.007948
	w=0.01647

	Red =[]
	for A in range(0, lim):
		x = (start_wave+(A*spacing))
		R =  a0 + (a1 * math.cos(x*w)) + (b1 * math.sin(x*w)) + (a2 * math.cos(2*x*w)) + (b2 * math.sin(2*x*w)) + (a3 * math.cos(3*x*w)) + (b3 * math.sin(3*x*w)) + (a4 * math.cos(4*x*w)) + (b4* math.sin(4*x*w)) + (a5 * math.cos(5*x*w)) + (b5 * math.sin(5*x*w)) + (a6 * math.cos(6*x*w)) + (b6 * math.sin(6*x*w))
		Red.append(R)
	return(Red)


def green():
	a0 = 0.3078 
	a1 = -0.3635
 	b1 = -0.2801
 	a2 = 0.05479 
 	b2 = 0.1905  
 	a3 = -0.0006051
 	b3 = -0.05219 
 	a4 = 0.01237 
 	b4 = 0.01693 
 	w = 0.01801


	Green =[]
	for A in range(0, lim):
		x = (start_wave+(A*spacing))
		G =  a0 + a1*math.cos(x*w) + b1*math.sin(x*w) + a2*math.cos(2*x*w) + b2*math.sin(2*x*w) + a3*math.cos(3*x*w) + b3*math.sin(3*x*w) + a4*math.cos(4*x*w) + b4*math.sin(4*x*w)
		Green.append(G)
	return(Green)


def blue():
	a1 = 1.092 
	b1 = 456.5 
	c1 = 21.39  
	a2 = 0.5744  
	b2 = 462.9  
	c2 = 41.09  
	a3 = 0.8858 
	b3 = 433.3 
	c3 =  15.04  



	Blue =[]
	for A in range(0, lim):
		x = (start_wave+(A*spacing))
		B = a1*math.exp(-((x-b1)/c1)**2) + a2*math.exp(-((x-b2)/c2)**2) + a3*math.exp(-((x-b3)/c3)**2)
		Blue.append(B)
	return(Blue)
	

imp2 = IJ.getImage()
imp2.setTitle ('master') 
n_slices = imp2.getStack().getSize()
IJ.run("Slice Remover", "first="+str(lim+2)+" last="+str(n_slices)+" increment=1")#remove slices greater than max wavelength, 750nm
imp3 = imp2.duplicate()
imp4 = imp2.duplicate()

#apply color matching functions to stack

for i in range(1, lim+1):
  imp2 = IJ.getImage()
  
  imp2.setSlice(i)
  f = red()[i-1]
  IJ.run("Multiply...", "value=" + str(f) + " slice")

  
for i in range(1, lim+1):  
  imp3.show()
  imp3 = IJ.getImage()
  imp3.setTitle("master2")
  imp3.setSlice(i)
  g = green()[i-1]
  IJ.run("Multiply...", "value=" + str(g) + " slice") 

  
for i in range(1, lim+1): 
  imp4.show() 
  imp4 = IJ.getImage()
  imp4.setTitle("master4")
  imp4.setSlice(i)
  b = blue()[i-1]
  IJ.run("Multiply...", "value=" + str(b) + " slice") 

#fiddly bits to make an image stack and display 

IJ.selectWindow("master")
IJ.run("Z Project...", "projection=[Average Intensity]")
imp2.changes = False
imp2.close()

IJ.selectWindow("master2")
IJ.run("Z Project...", "projection=[Average Intensity]")
imp3.changes = False
imp3.close()

IJ.selectWindow("master4")
IJ.run("Z Project...", "projection=[Average Intensity]")
imp4.changes = False
imp4.close()

IJ.run("Images to Stack", "name=Stack title=[] use")
imp = IJ.getImage()
imp.setTitle("XYZ")
IJ.run("Make Composite", "display=Composite")
IJ.run("Enhance Contrast", "saturated=0.35")
IJ.run("Next Slice [>]")
IJ.run("Enhance Contrast", "saturated=0.35")
IJ.run("Next Slice [>]")
IJ.run("Enhance Contrast", "saturated=0.35")