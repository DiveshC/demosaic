import numpy as np
from numpy.linalg import inv
from numpy import matmul
import sys

# linear interp
def mosaic(rgb_arr):
    mos = np.zeros(rgb_arr[0].T.shape)
    r = rgb_arr[0].T
    g = rgb_arr[1].T
    b = rgb_arr[2].T
    # R
    for i in range(0, r.shape[0], 2):
        for j in range(0, r.shape[1], 2):
            mos[i][j] = r[i][j]
    # G
    for i in range(g.shape[0]):
        init = 1-(i%2)
        for j in range(init, g.shape[1], 2):
            mos[i][j] = g[i][j]
    # B
    for i in range(1, b.shape[0], 2):
        for j in range(1, b.shape[1], 2):
            mos[i][j] = b[i][j]
    return mos

def lin_interp(xi, yi, B, F):
    inp = np.array([xi*yi, xi, yi, 1])
    # print(B)
    Binv = inv(B)
    coef = matmul(Binv, F)
    prod = matmul(coef,inp)
    # print(prod, F)
    # return x * Binv * F * Binv.T * y
    return prod

# cubic 

def cubic_interp(xi, yi, B, F):
    x = np.array([xi**3, xi**2, xi, 1])
    y = np.array([yi**3, yi**2, yi, 1])
    Binv = inv(B)
    prod = matmul(Binv, F)
    prod2 = matmul(prod, Binv.T)
    prod3 = matmul(x, prod2)
    prod4 = matmul(prod3, y)
    # return x * Binv * F * Binv.T * y
    return matmul(prod3, y)

def get_samples(blk, dim, color="r", mode=None):
    f = np.zeros(dim)
    s = np.full(blk.shape, None)
    r = 0
    init = 0
    ## green samples
    if(color == "g"):
        k=0
        for i in range(blk.shape[0]):
            init = 1-(i%2)
            for j in range(init, blk.shape[1], 2):
                if(mode=="data"):
                    f[i][j] = blk[i][j]
                else:
                    f[k] = blk[i][j]
                k+=1
        return f
    ## red/blue samples
    if(color == "b"):
        init = 1
    for i in range(init, blk.shape[0], 2):
        c = 0
        for j in range(init, blk.shape[1], 2):
            f[r][c] = blk[i][j]
            s[i][j] = blk[i][j]
            c += 1
        r += 1
    
    if(mode == "data"):
        f=s
    return f

def generate_B(s,dim, mode="r"):
    B = np.zeros(dim)
    init=0
    if(mode == "g"):
        k=0
        for i in range(s.shape[0]-1):
            for j in range(s.shape[1]-1):
                B[k] = [ i*j, i, j, 1]
                k+=1
        return B
    if(mode == "b"):
        init = 1
    j=0
    for i in range(init, s.shape[0], 2):
        B[j] = [i**3, i**2, i, 1]
        j+=1
    return B

def fill_block(blk, B, F):
    for i in range(blk.shape[0]):
        for j in range(blk.shape[1]):
            if(blk[i][j] == None):
                blk[i][j] = cubic_interp(i, j, B, F)
    return blk     
'''
Args
blk - the block of data we do have samples for
coord - the x,y ranges for where the blk sits in the 8x8
desired_dim - desirable block size
replace - the value we fill in for the missing samples
'''
def fill_missing(blk,coord, desired_dim, replace):
    des = np.full(desired_dim, replace)
    des[coord[0]:coord[1], coord[2]:coord[3]] = blk[coord[0]:coord[1], coord[2]:coord[3]]
    return des

def error(inp, outp):
    ref = inp.T
    r = ref[0]
    g = ref[1]
    b = ref[2]
    rGen = outp[0]
    gGen = outp[1]
    bGen = outp[2]
    sumR=0
    sumG=0
    sumB=0
    Nsamples = r.shape[0]*r.shape[1]
    for i in range(r.shape[0]):
        for j in range(r.shape[1]):
            sumR += (r[i][j] - rGen[i][j])**2
            sumG += (g[i][j] - gGen[i][j])**2
            sumB += (b[i][j] - bGen[i][j])**2
    
    return (sumR+sumG+sumB)/(Nsamples*3)