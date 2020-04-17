//User selects data file for analysis. LambdaStacktoXYZ and XYZ to RBG macros must be installed as plugins.

//Identifies current directory from user selected file and extracts the path 
//and file name for the correspinding file

path=File.openDialog("Select Data File");
dir= File.directory;
name=File.nameWithoutExtension;
file=File.name;

//Clears the log window
print("\\Clear");

//Prints values to log for confirmation that correct files are used.
  print("Path:", path);
  print("Name:", name);
  print("Directory:", dir);
  
 //Opens associated hdr file as long as .bil and .bil.hdr are in the same directory
open(file + ".hdr");

//Creates dialog window to input values for importing data cube and prints to log window for recordkeeping.
Dialog.create("Input Parameters")
Dialog.addMessage("Refer to HDR file for values");
Dialog.addNumber("Lines",956)
Dialog.addNumber("Samples",640)
Dialog.addNumber("Bands", 240)
Dialog.show();

lines=Dialog.getNumber();
samples=Dialog.getNumber();;
bands=Dialog.getNumber();;;

//Prints data cube values to log window for recordkeeping
  print("Number of Images/Lines:",lines)
  print("Width/Samples", samples)
  print("Height/Bands:", bands);

//Imports Raw data as a 16-bit signed image with user specified values and little-endian field flagged.
run("Raw...", "open=[path] image=[16-bit Signed] width=samples height=bands number=lines little-endian");

//Reslice data and saves resliced data cube as tiff
run("Reslice [/]...", "output=1.000 start=Top avoid");
reslicename=name + "_reslice";
 saveAs("Tiff", dir+ reslicename);

//Transform to 32-bit and duplicate window
run("32-bit");
 saveAs("Tiff", dir+ reslicename +"32bit");;
run("Duplicate...", "duplicate");

//LambdaStack to XYZ macro
//Takes spectral image data and transforms into XYZ tristumulus Space
run("LambdaStack to XYZ", "wavlength=2 starting=393 ending=750");
 print("In LambaStack to XYZ macro:\n2nm wavelength spacing from 393 nm to 750 nm")

//XYZ to RGB macro:
//transform XYZ to adobe RGB, D65 Illuminant. See http://brucelindbloom.com/index.html?Eqn_RGB_XYZ_Matrix.html 
//for transform matrix.

run("XYZ to RGB");
run("32-bit");

//Creates a new folder for 32 bit data and saves RGB data to folder
File.makeDirectory(dir+ "/32bit" );
RGB32=name + "_RGB_32bit";
 saveAs("Tiff", dir+ "/32bit/" + RGB32);

//Creates a new folder for 8 bit data and saves RGB data to folder
run("RGB Color");
File.makeDirectory(dir+ "/8bit" );
RGB8=name + "_RGB_8bit";
 saveAs("Tiff", dir+ "/8bit/" + RGB8);

//Saves log window with printed parameters used in data analysis
selectWindow("Log");
 saveAs("text", dir+ name+"Log.txt");