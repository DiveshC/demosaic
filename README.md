# Demosaicing Project 1 - 3SK3
## System requirments
In order to run the project an installation of python is requires, in addition to that the following libraries are also needed:
- Pillow
- numpy

```
$ pip install pillow

$ pip install numpy 
``` 

## Running 
Within the main directory you can run the following command in the terminal. It takes 2 arguments:
- input rgb image path 
- desired output image path
```
$ python demosaic.py "<input file path>" "<output file path>"
```
Example snipet:
```
python demosaic.py "data/in/raptors.jpg" "data/out/demosaic-raptors.png"
```

If there is some issues with passing the file paths in the terminal command, within the demosaic.py file on line 13 and 14 there are hardcoded file paths that can be replaced with the desired image paths. Comment the lines above it as well (lines 9 and 10).
```
# using command terminal arguments
input_filename = sys.argv[1]
output_name = sys.argv[2]
# using hardcoded file path
# NOTE: if the commandline argument is failing just uncomment this and replace with the file path desired
# input_filename = "data/in/raptors.jpg"
# output_name = "data/in/raptors.png"
```

### File structure
There are 2 main files, the demosaic.py and a utils.py. Heres a quick breakdown of the purpose of each:
- demosaic.py for the interpolation of data and generating output rgb image
- utils.py contains helper functions for the demosaicing 

The utils functions are imported in demosaic.py.

### Full Documentation
The [full report](./docs/Report.pdf) on the algorithms used and design process is in the docs folder 