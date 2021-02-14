import numpy as np
from numpy.linalg import inv
from numpy import matmul
from PIL import Image
import sys
from utils import mosaic, lin_interp, cubic_interp, get_samples, generate_B, fill_block, fill_missing, error

# using command terminal arguments
input_filename = sys.argv[1]
output_name = sys.argv[2]
# using hardcoded file path
# NOTE: if the commandline argument is failing just uncomment this and replace with the file path desired
# input_filename = "data/in/raptors.jpg"
# output_name = "data/in/raptors.png"

print("Opening {}".format(input_filename))
img = Image.open(input_filename)
img_data_rgb = np.asarray(img)

## get mosaic of image
img_data = mosaic(img_data_rgb.T)

r_data = get_samples(img_data, img_data.shape,"r", "data")
g_data = get_samples(img_data, img_data.shape, "g", "data")
b_data = get_samples(img_data, img_data.shape,"b", "data")
imgHeight = img_data.shape[0]
imgWidth = img_data.shape[1]

#interpolating red
print("interpolating Red ... ")
init = 0
dim = [7,7]
for i in range(0, img_data.shape[0], 2):
    for j in range(1, img_data.shape[1], 2):
        block = np.full([8,8], None)
        if(i-2<0 and j-3<0):
            # missing samples corner case 1 
            r= abs(i-2)
            c= abs(j-3)
            block[r:r+5, c:c+5] = img_data[i:i+5, j-1:j+4]
            block = fill_missing(block,[r,r+5, c,c+5], dim, block[r][c])
        elif(i-2<0 and j+4 > imgWidth):
            # missing corner case 2:
            r= abs(i-2)
            c =imgWidth-(j-3)
            block[r:r+5, :c] = img_data[i:i+5, j-3:imgWidth]
            block = fill_missing(block,[r,r+5, 0,c], dim, block[r][0])
        elif(i+5>imgHeight and j-3<0):
            # missing samples corner case 3 
            r = imgHeight-(i-2)
            c= abs(j-3)
            block[:r, c:c+5] = img_data[i-2:imgHeight, j-1:j+4]
            block = fill_missing(block,[0,r, c,c+5], dim, block[0][c])
        elif(i+5>imgHeight and j+4 > imgWidth):
            # missing corner case 4:
            r = imgHeight-(i-2)
            c= imgWidth-(j-3)
            block[:r, :c] = img_data[i-2:imgHeight, j-3:imgWidth]
            block = fill_missing(block,[0,r, 0,c], dim, block[0][0])
        elif(j-3 < 0 and (i-2>=0 and i+4<=imgHeight)):
            #row missing cases (left)
            c= abs(j-3)
            block[:dim[0], c:c+5] = img_data[i-2:i+5, j-1:j+4]
            block = fill_missing(block,[0,dim[0], c,c+5], dim, block[0][c])
        elif(j+4 > imgWidth and (i-2>=0 and i+4<=imgHeight)):
            #row missing cases (right)
            c= imgWidth-(j-3)
            block[:dim[0], :c] = img_data[i-2:i+5, j-3:imgWidth]
            block = fill_missing(block,[0,dim[0], 0,c], dim, block[0][0])
        elif(i-2 < 0 and (j-3>=0 and j+3<=imgWidth)):
            #column missing cases(top)
            r = abs(i-2)
            block[r:r+5, 0:dim[1]] = img_data[i:i+5, j-3:j+4]
            block = fill_missing(block,[r,r+5, 0,dim[1]], dim, block[r][0])
        elif(i+5 > imgHeight and (j-3>=0 and j+3<=imgWidth)):
            #column missing cases(bottom)
            r = imgHeight-(i-2)
            block[:r, :dim[1]] = img_data[i-2:imgHeight, j-3:j+4]
            block = fill_missing(block,[0,r, 0,dim[1]], dim, block[0][0])
        else:
            block=img_data[i-2:i+5, j-3:j+4]

        f = get_samples(block, [4,4])
        B = generate_B(block, [4,4])
        r_data[i][j] = cubic_interp(2, 3, B, f)

        if(i+1<imgHeight):
            r_data[i+1][j] = cubic_interp(3, 3, B, f)
            r_data[i+1][j-1] = cubic_interp(3, 2, B, f)
        ## end of blocks in row
        if(j+2 == imgWidth):
            r_data[i+1][j+1] = cubic_interp(3, 4, B, f)

## interpolating blue channel
print("interpolating Blue ... ")
for i in range(0, img_data.shape[0], 2):
    for j in range(0, img_data.shape[1], 2):
        # handle edge cases
        block = np.full([8,8], None)
        if(i-3<0 and j-3<0):
            # missing samples corner case 1 
            r= abs(i-3)
            c= abs(j-3)
            block[r:dim[0], c:dim[0]] = img_data[0:i+4, 0:j+4]
            block = fill_missing(block,[r,dim[0], c,dim[1]], dim, img_data[i+1][j+1])
        elif(i-3<0 and j+4 > imgWidth):
            # missing corner case 2:
            r= abs(i-3)
            c =imgWidth-(j-3)
            block[r:dim[1], :c] = img_data[0:i+4, j-3:imgWidth]
            block = fill_missing(block,[r,dim[1], 0,c], dim, img_data[i+1][j-1])
        elif(i+4>imgHeight and j-3<0):
            # missing samples corner case 3 
            r = imgHeight-(i-3)
            c= abs(j-3)
            block[:r, c:dim[1]] = img_data[i-3:imgHeight, 0:j+4]
            block = fill_missing(block,[0,r, c,dim[1]], dim, img_data[i-1][j+1])
        elif(i+4>imgHeight and j+4 > imgWidth):
            # missing corner case 4:
            r = imgHeight-(i-3)
            c= imgWidth-(j-3)
            block[:r, :c] = img_data[i-3:imgHeight, j-3:imgWidth]
            block = fill_missing(block,[0,r, 0,c], dim, img_data[i-1][j-1])
        elif(j-3 < 0 and (i-3>=0 and i+4<=imgHeight)):
            #row missing cases (left)
            c= abs(j-3)
            block[:dim[0], c:dim[1]] = img_data[i-3:i+4, 0:j+4]
            block = fill_missing(block,[0,dim[0], c,dim[1]], dim, img_data[i+1][j+1])
        elif(j+4 > imgWidth and (i-3>=0 and i+4<=imgHeight)):
            #row missing cases (right)
            c= imgWidth-(j-3)
            block[:dim[0], :c] = img_data[i-3:i+4, j-3:imgWidth]
            block = fill_missing(block,[0,dim[0], 0,c], dim, img_data[i+1][j-1])
        elif(i-3 < 0 and (j-3>=0 and j+4<=imgWidth)):
            #column missing cases(top)
            r = abs(i-3)
            block[r:dim[1], 0:dim[1]] = img_data[0:i+4, j-3:j+4]
            block = fill_missing(block,[r,dim[1], 0,dim[1]], dim, img_data[i+1][j+1])
        elif(i+4 > imgHeight and (j-3>=0 and j+4<=imgWidth)):
            #column missing cases(bottom)
            r = imgHeight-(i-3)
            block[:r, :dim[1]] = img_data[i-3:imgHeight, j-3:j+4]
            block = fill_missing(block,[0,r, 0,dim[1]], dim, img_data[i-1][j+1])
        else:
            block=img_data[i-3:i+4, j-3:j+4]

        f = get_samples(block, [4,4])
        B = generate_B(block, [4,4])
        b_data[i][j] = cubic_interp(3, 3, B, f)

        if(i+1<imgHeight):
            b_data[i+1][j] = cubic_interp(4, 3, B, f)
        if(j+1<imgWidth):
            b_data[i][j+1] = cubic_interp(3, 4, B, f)

## interpolating green channel
print("interpolating Green ... ")
dim = [3,3]
dimSmall = [2,2]
for i in range(img_data.shape[0]):
    init = i%2
    block = np.full([3,3], None)
    for j in range(init, img_data.shape[1], 2):
        if(i-1<0 and j-1<0):
            #corner case 1 (top left)
            r = abs(i-1)
            c = abs(j-1)
            block[r:dim[0], c:dim[1]] = img_data[0:i+2, 0:j+2]
            block = fill_missing(block, [r,dim[0],c,dim[1]], dim, img_data[i][j+1])
        elif(i-1<0 and j+2>imgWidth):
            #corner case 2 (top right)
            r = abs(i-1)
            c = imgWidth-(j-1)
            block[r:dim[0], 0:c] = img_data[0:i+2, j-1:imgWidth]
            block = fill_missing(block, [r,dim[0],0,c], dim, img_data[i+1][j])
        elif(i+2>imgHeight and j-1<0):
            #corner case 3 (bottom left)
            r = imgHeight-(i-1)
            c = abs(j-1)
            block[0:r, c:dim[1]] = img_data[i-1:imgHeight, 0:j+2]
            block = fill_missing(block, [0,r,c,dim[1]], dim, img_data[i-1][j])
        elif(i+2>imgHeight and j+2>imgWidth):
            #corner case 4 (bottom right)
            r = imgHeight - (i-1)
            c = imgWidth - (j-1)
            block[:r,:c] = img_data[i-1:imgHeight, j-1:imgWidth]
            block = fill_missing(block, [0,r,0,c], dim, img_data[i][j-1])
        elif(i-1<0 and (j-1>=0 and j+1<=imgWidth)):
            #edge case 1 (top)
            r = abs(i-1)
            block[r:dim[0], :dim[1]] = img_data[0:i+2, j-1:j+2]
            block = fill_missing(block, [r,dim[0], 0,dim[1]], dim, img_data[i][j+1])
        elif(i+2>imgHeight and (j-1>=0 and j+1<=imgWidth)):
            #edge case 2 (bottom)
            r = imgHeight - (i-1)
            block[:r, :dim[1]] = img_data[i-1:imgHeight, j-1:j+2]
            block = fill_missing(block, [0,r, 0,dim[1]], dim, img_data[i][j+1])
        elif(j-1<0 and (i-1>=0 and i+1<=imgHeight)):
            #edge case 3 (left)
            c = abs(j-1)
            block[:dim[0], c:dim[1]] = img_data[i-1:i+2, 0:j+2]
            block = fill_missing(block, [0,dim[0], c,dim[1]], dim, img_data[i][j+1])
        elif(j+2>imgWidth and (i-1>=0 and i+1<=imgHeight)):
            #edge case 4 (right)
            block = np.full([3,3], None)
            c = imgWidth - (j-1)
            block[:dim[0], 0:c] = img_data[i-1:i+2, j-1:imgWidth]
            block = fill_missing(block, [0,dim[0],0,c], dim, img_data[i-1][j])
        else:
            block = img_data[i-1:i+2, j-1:j+2]

        f = get_samples(block, 4, "g")
        B = generate_B(block, [4,4], "g")
        g_data[i][j] = lin_interp(0.5, 0.5, B, f)

final_arr = np.asarray([r_data.T,g_data.T,b_data.T])

c_img = Image.fromarray(np.uint8(final_arr.T),'RGB')
filename = "demosaic-{}.png".format("lion")
c_img.save(output_name)
print("Saved {}".format(output_name))

print(error(img_data_rgb, final_arr))