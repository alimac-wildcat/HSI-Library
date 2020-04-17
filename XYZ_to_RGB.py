#transform XYZ to adobe RGB, D65 Illuminant. See http://brucelindbloom.com/index.html?Eqn_RGB_XYZ_Matrix.html for 
#transform matrix.

from org.ejml.simple import SimpleMatrix 
from ij import IJ, ImagePlus
from ij.plugin import ImageCalculator
from ij.process import ImageProcessor
from ij.process import FloatProcessor
from org.ejml.simple import SimpleMatrix 
import cmath, math

imp2 = IJ.getImage()

#XYZ to RGB transform Matrix
M = [[2.0413690, -0.5649464, -0.3446944], [-0.9692660,  1.8760108,  0.0415560], [0.0134474, -0.1183897,  1.0154096]]
M = SimpleMatrix(M)

#Import XYZ Images. Normalize by white balance before.
n_slices = imp2.getStack().getSize()
I =[]
for i in range(1, n_slices+1):
  imp2.setSlice(i) 
  n = imp2.getProcessor().getPixels()   
  n2 = [val for val in n]
  I.append(n2)

D= SimpleMatrix(I) 

RGB = M.mult(D).getMatrix().data

L1 = [RGB[i:i+imp2.height*imp2.width] for i in range(0, len(RGB), imp2.height*imp2.width)]

#fiddly bits to make an image stack and display 

R = ImagePlus("Red", FloatProcessor(imp2.width,imp2.height,L1[0])).show()
G= ImagePlus("Green", FloatProcessor(imp2.width,imp2.height,L1[1])).show()
B = ImagePlus("Blue", FloatProcessor(imp2.width,imp2.height,L1[2])).show()

IJ.run("Images to Stack", "name=Stack title=[] use")
imp = IJ.getImage()
imp.setTitle("RGB")
IJ.run("Make Composite", "display=Composite")
IJ.run("Enhance Contrast", "saturated=0.35")
IJ.run("Next Slice [>]")
IJ.run("Enhance Contrast", "saturated=0.35")
IJ.run("Next Slice [>]")
IJ.run("Enhance Contrast", "saturated=0.35")