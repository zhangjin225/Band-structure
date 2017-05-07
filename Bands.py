# Edited by Jin Zhang 07-11-2016
# obtaining the band structure E(k) from vasp calculation. EIGENVAL and OUTCAR will be used 
import numpy as np
import matplotlib.pyplot as plt
import itertools
from math import sqrt


fields=[]
q = []
d = []
t = [0.0]

## enter E-fermi
e_fermi = input ("Please enter Fermi energy from static calculation: ")   # enter e-fermi
e_fermi = float(e_fermi) 

## open EIGENVAL file 
with open ("EIGENVAL", "r") as eigenval:
    K_num = eigenval.readlines() [5]
    K_num = int (K_num.split() [1])  # the number of K points
    
## open EIGENVAL file 
with open ("EIGENVAL", "r") as eigenval:
    content = [x.rstrip() for x in eigenval]  
    data = [x[6:] for x in content [8:]]   # skip first 8 rows and start reading  from 8th rows; skip first 10 colume and start reading from 6th colume ***********
   # print (len(data[7]))
    for i in range(len(data)):
        if len(data[i]) < int(40):  # using the  length of string to delete the useless line, like "0.0000000E+00  0.0000000E+00  0.0000000E+00  0.7142857E-02"
            m = data[i]
            fields.extend(m.split())
n = fields  # band data
k = int((len(n))/K_num)  
band = np.asarray(n, dtype = np.float64) # convert to array (array type)
band = [i-e_fermi for i in band] # subduct fermi energy (list type)
band = np.asarray(band, dtype = np.float64) # convert list to array (array type)
band = band.reshape(K_num, k) #
print (band)

## open OUTCAR
with open ("OUTCAR", "r") as outcar:
    lines = outcar.readlines()
    for i in range(len(lines)):
        if "2pi" in lines[i]:  # use "2pi" to pinpoint the starting line
            a = i
            print(a)  # begin from this line
##        if "E-fermi" in lines[i]:
##            b = i
##            print (b)
##            c=float(lines[b].split()[2])  #E-fermi
##            print (c)
with open ("out.txt", "r") as out:
    lines = out.readlines()
    for i in range(a+1, a+1+K_num):
        j = lines[i]
        q.extend(j.split())
K_point = np.asarray(q, dtype = np.float64) # convert to array
h = int(len(K_point)/K_num)
K_point = K_point.reshape(K_num, h) # obtain the 3D k-point

## calculating the 2D k-point from 3D k-point
for i in range(K_num-1):
    diff_K = K_point [i+1, :] - K_point [i, :]
    b = sqrt((diff_K [0])**2 + (diff_K [1])**2 + (diff_K [2])**2)  # calculating the distance between two points. d=sqrt((x2-x1)^2+(y2-y1)^2+(z2-z1)^2)
    d.append (b)  
for i in range(len(d)):  
    p = t[i]+d[i]
    t.append(p)
t= np.asarray(t)
t = t.reshape(K_num,1) # obtain the 2D k-point
print (t)

## merge k-point and band date into one file and export this file
Band_data = np.hstack((t, band))   #or using "total = np.concatenate((t, band), axis =1)"
np.savetxt("band.txt", Band_data)
print (Band_data)


