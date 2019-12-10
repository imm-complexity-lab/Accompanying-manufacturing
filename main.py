#!/root/anaconda3/bin/python3.7
import subprocess
import math
import random
import matplotlib.pyplot as plt
import numpy as np
import sys


N = 100
p = 11
T = 100
path = "/home/belousov_an/Industrial/Results/A_5/"

clq_fstclq_ctsp = 0
clq_fstclq_gr = 0
clq_gr_ctsp = 0
clq_gr_gr = 0
tsp_fstclq_ctsp = 0
tsp_fstclq_gr = 0
tsp_gr_ctsp = 0
tsp_gr_gr = 0

external_1 = []
internal_1 = []
external_2 = []
internal_2 = []
external_3 = []
internal_3 = []
external_4 = []
internal_4 = []
null_1 = []
null_2 = []
null_3 = []
null_4 = [] 


def main():
    s1 = subprocess.check_output(["/home/belousov_an/Industrial/CLKH-1.0/fstclq_ctsp.py"])
    s2 = subprocess.check_output(["/home/belousov_an/Industrial/CLKH-1.0/fstclq_gr.py"])
    s3 = subprocess.check_output(["/home/belousov_an/Industrial/CLKH-1.0/gr_ctsp.py"])
    s4 = subprocess.check_output(["/home/belousov_an/Industrial/CLKH-1.0/gr_gr.py"])
    array1 = []
    array2 = []
    array3 = []
    array3 = []
    sum2 = 0
    sum3 = 0
    
    s1 = s1.decode('utf-8')
    array1 = s1.split()
    
    s2 = s2.decode('utf-8')
    array2 = s2.split()
    
    s3 = s3.decode('utf-8')
    array3 = s3.split()
    
    s4 = s4.decode('utf-8')
    array4 = s4.split()
	
    return array1, array2, array3, array4


#for i in range(1, N):
#    print("Begining: p =", i)
#    clq_fstclq_ctsp = 0
#    clq_fstclq_gr = 0
#    clq_gr_ctsp = 0
#    clq_gr_gr = 0
#    tsp_fstclq_ctsp = 0
#    tsp_fstclq_gr = 0
#    tsp_gr_ctsp = 0
#    tsp_gr_gr = 0
#    external_1 = []
#    internal_1 = []
#    external_2 = []
#    internal_2 = []
#    external_3 = []
#    internal_3 = []
#    external_4 = []
#    internal_4 = []   
for i in range(T):
    subprocess.run(["/home/belousov_an/Industrial/Scripts/generate_data.py", "-nd", str(N)])
    a, b, c, d = main()
    
    if int(a[0]) > 1000: 
        clq_fstclq_ctsp += clq_fstclq_ctsp/(j+1)
    else: 
        clq_fstclq_ctsp += int(a[0])
        external_1.append(a[0]) 
        
    if int(c[0]) > 1000:
        clq_gr_ctsp += clq_gr_ctsp/(j+1)
        external_3.append(c[0])
    else:
        clq_gr_ctsp += int(c[0])
        external_3.append(c[0])
    
    clq_fstclq_gr += int(b[0])
    external_2.append(b[0])
    clq_gr_gr += int(d[0])
    external_4.append(d[0])
   
    tsp_fstclq_ctsp += int(a[1])
    internal_1.append(a[1])
    tsp_fstclq_gr += int(b[1])
    internal_2.append(b[1])
    tsp_gr_ctsp += int(c[1])
    internal_3.append(c[1])
    tsp_gr_gr += int(d[1])
    internal_4.append(d[1])
    null_1.append(a[2])
    null_2.append(b[2])
    null_3.append(c[2])
    null_4.append(d[2])
    
    print("STEP: ", i)

file1 = open(path + "FstClq_CTSP/fstclq_ctsp", 'w')
file2 = open(path + "FstClq_GR/fstclq_gr", 'w')
file3 = open(path + "GR_CTSP/gr_ctsp", 'w')
file4 = open(path + "GR_GR/gr_gr" , 'w')
file5 = open(path + "FstClq_CTSP/fstclq_ctsp" + "_", 'w')
file6 = open(path + "FstClq_GR/fstclq_gr" + "_", 'w')
file7 = open(path + "GR_CTSP/gr_ctsp" + "_", 'w')
file8 = open(path + "GR_GR/gr_gr" + "_", 'w')


clq_fstclq_ctsp = clq_fstclq_ctsp/T
clq_fstclq_gr = clq_fstclq_gr/T
clq_gr_ctsp = clq_gr_ctsp/T
clq_gr_gr = clq_gr_gr/T
	
tsp_fstclq_ctsp = tsp_fstclq_ctsp/T
tsp_fstclq_gr = tsp_fstclq_gr/T
tsp_gr_ctsp = tsp_gr_ctsp/T
tsp_gr_gr = tsp_gr_gr/T
    
file1.write(str(round(clq_fstclq_ctsp, 3)) + " " + str(round(tsp_fstclq_ctsp, 3)))
file2.write(str(round(clq_fstclq_gr, 3)) + " " + str(round(tsp_fstclq_gr, 3)))
file3.write(str(round(clq_gr_ctsp, 3)) + " " + str(round(tsp_gr_ctsp, 3)))
file4.write(str(round(clq_gr_gr, 3)) + " " + str(round(tsp_gr_gr, 3)))
for i in range(len(external_1)):
    file5.write(str(internal_1[i]) + " " + str(external_1[i]) + " " + str(null_1[i]) + "\n")
    file6.write(str(internal_2[i]) + " " + str(external_2[i]) + " " + str(null_2[i]) + "\n")
    file7.write(str(internal_3[i]) + " " + str(external_3[i]) + " " + str(null_3[i])+ "\n")
    file8.write(str(internal_4[i]) + " " + str(external_4[i]) + " " + str(null_4[i]) + "\n")
    
    #print(clq_fstclq_ctsp, tsp_fstclq_ctsp)
    #print(clq_fstclq_gr, tsp_fstclq_gr)
    #print(clq_gr_ctsp, tsp_gr_ctsp)
    #print(clq_gr_gr, tsp_gr_gr)




