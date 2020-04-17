# HSI-Library
Procedure for extracting spectral data from data cube using Fiji/Image J.

This macro should be installed in the Fiji/Image J plugins folder along with the XYZtoRGB.py and LambdaStacktoXYZ.py macros. 

The program will need to be restarted to successfully install plugins. Once installed the plugins will be available from 
the plugins tab, usually at the end of the list.

The macro will complete the following steps:
  1. Import user file and open associated .hdr file (which should be included in the same folder as the .bil file)
  2. Transform the .bil data cube to .tiff data cube
  3. Transform specral data to XYZ tristimulus space
  4. Transform XYZ to adobe RGB, D65 Illuminant. See http://brucelindbloom.com/index.html?Eqn_RGB_XYZ_Matrix.html 
     for transform matrix.

The macro will also produce an associated .txt log file which contains a general outline of the parameters used in 
the transformations above.
