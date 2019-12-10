#!/root/anaconda3/bin/python3.7
import subprocess
import math
import random
import matplotlib.pyplot as plt
import numpy as np
import sys
from copy import deepcopy
import time
import statistics
import argparse
import glob
import shutil
import os
from subprocess import Popen, PIPE, STDOUT
from itertools import groupby

start_time = time.time()

NUM_DET_NECESSARY = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49] #, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99]
DET_NECESSARY = []
data_file_bottom = ['DEPOT_SECTION', '1', '-1', 'EOF']
matrix = []
path = "/home/belousov_an/Industrial/DATA/data"
path1 = "/home/belousov_an/Industrial/DATA/data_con"
path2 = "/home/belousov_an/Industrial/"
DET = []  # список деталей
CONDITION = []
CONDITIONS = {}  # условия
COMPATIBILITY = {}
WEIGHT = []
WEIGHTS = {}  # веса
COMPAT_MATRIX = []  # матрица совместимости
CLUSTERS = [] # кластера деталей
CLUSTER_ELEM = []
WEIGHT_MATRIX = []
WEIGHT_MATRIX_Temp = []
CLUSTERS_TEMP = []
temp = []
num_cluster = [] # переменная, в которой хранится номера кластеров
Array = []
count = 0
seq = []
lscc = []
summa = 10000000000000
first_cl = 0
first_cluster = []
match_cluster = [] # сформированные кластера
fin_cluster = []
ctsp_lenght = 10000000
ctsp_tour = []
max_cl = 0

files_INSTANCES = glob.glob(path2 + 'Instances/GREEDY_2/*')
files_TOURS = glob.glob(path2 + 'Tours/GREEDY_2/*')
files_LSCC = glob.glob(path2 + 'LSCC/GREEDY_2/*')
files_TSP = glob.glob(path2 + 'CLKH-1.0/TSP/GREEDY_2/tsp*')
for f in files_TOURS:
    os.remove(f)
for f in files_INSTANCES:
    os.remove(f)
for f in files_LSCC:
    os.remove(f)
for f in files_TSP:
    os.remove(f)



def file_open_data_con(A):
    f = open(A, 'r', encoding='utf-8')
    lines = f.readlines()
    data_array = [] * len(lines)
    row = 0
    for line in lines:
        elements = list(map(int, line.split()))
        data_array.append(elements)
        row += 1
    f.close()
    return data_array


def file_open_data(A):
    f = open(A, 'r', encoding='utf-8')
    lines = f.readlines()
    lines = [int(line.rstrip()) for line in lines]
    return lines


CONDITION = file_open_data_con(path1)
WEIGHT = file_open_data(path)

N = len(WEIGHT)

for i in range(N):
    DET.append('A' + str(i))

for i in NUM_DET_NECESSARY:
    DET_NECESSARY.append('A' + str(i))

for i in range(len(DET)):
    WEIGHTS[DET[i]] = WEIGHT[i]


for i in range(N):
    Array = []
    for j in range(N):
        if i == j or CONDITION[i][j] != 0:
            Array.append(False)
        else:
            Array.append(True)
    COMPAT_MATRIX.append(Array)
    COMPATIBILITY[i] = Array
                                                        

def proverka(A, B):
    for i in A:
        if COMPAT_MATRIX[i][B] == False:
            return False
    return True

def array_true(A):
    array = [A]
    i = 0
    C = deepcopy(WEIGHT)
    C[A] = -1
    while i != len(DET):
        if C[i] == max(C) and C[i] != -1:
            C[i] = -1
            array.append(i)
            i = 0
        else:
            i += 1
    return array

def maxclique(A):
    array = [A]
    for i in DET:
        if proverka(array, DET.index(i)) == True:
            array.append(DET.index(i))
    return array

def maxclique_greedy(A):
    c = [A[0]]
    for i in A:
        if proverka(c, i) == True:
           c.append(i)
    return c

for i in NUM_DET_NECESSARY:
    num_cluster = deepcopy(maxclique_greedy(array_true(i)))
    CLUSTERS_TEMP.append(num_cluster)

# Убираем повторяющиеся элемненты в кластерах
def match(Matrix):
    for i in Matrix:
        for j in Matrix:
            if i != j:
                for k in i:
                    for n in j:
                        if k == n:
                            j.remove(n)
            elif i == j and Matrix.index(i) != Matrix.index(j):
                for k in i:
                    for n in j:
                        if k == n:
                            j.remove(n)
    while ([] in Matrix):
        Matrix.remove([])
    return Matrix

CLUSTERS_TEMP = deepcopy(match(CLUSTERS_TEMP))

for i in CLUSTERS_TEMP:
    if len(i) == 1 and i[0] not in NUM_DET_NECESSARY:
            CLUSTERS_TEMP.remove(i)

for i in CLUSTERS_TEMP:
    if i not in match_cluster:
         match_cluster.append(i)

for i in match_cluster:
    for j in i:
        CLUSTER_ELEM.append(j)

data_atsp_top = ['NAME : DATA.gtsp', 'TYPE : AGTSP', 'DIMENSION : ' + str(len(CLUSTER_ELEM)), 'GTSP_SETS : ' + str(len(match_cluster)),
                 'EDGE_WEIGHT_TYPE: EXPLICIT', 'EDGE_WEIGHT_FORMAT: FULL_MATRIX', 'EDGE_WEIGHT_SECTION']

for i in match_cluster:
    for j in i:
        for k in i:
            if j != k and COMPAT_MATRIX[j][k] == False:
                CONDITION[j][k] = 777777777

# Матрица весов для элементов кластера
for i in range(len(CLUSTER_ELEM)):
    temp_array = []
    for j in range(len(CLUSTER_ELEM)):
        temp_array.append(CONDITION[CLUSTER_ELEM[i]][CLUSTER_ELEM[j]])
    WEIGHT_MATRIX.append(temp_array)

def external(Matrix, Matrix_1, Matrix_2, value1, value2):
    count = 0
    file1 = open(path2 + "CLKH-1.0/TSP/GREEDY_2/tsp" + str(value1) + str(value2) + ".par", 'w')
    file1.write("PROBLEM_FILE = /home/belousov_an/Industrial/Instances/GREEDY_2/TOUR_TSP" + str(value1) + str(value2) + "\n")
    file1.write("OUTPUT_TOUR_FILE = /home/belousov_an/Industrial/Tours/GREEDY_2/TOUR_TSP" + str(value1) + str(value2))	
    file = open(path2 + "Instances/GREEDY_2/TOUR_TSP" + str(value1) + str(value2), 'w')
    file.write("\n".join(data_atsp_top))
    file.write("\n")
    for string in Matrix:
        for s in string:
            file.write(str(s) + " ")
        file.write('\n')
    file.write("GTSP_SET_SECTION")
    file.write("\n")
    for string in Matrix_1:
        file.write(str(count + 1) + " ")
        for s in string:
            file.write(str(Matrix_2.index(s)+1) + " ")
        file.write('-1' + '\n')
        count += 1
    file.write('EOF')
    file.close()
    file1.close()

temp_value = 0

for i in match_cluster:
    WEIGHT_MATRIX_Temp = deepcopy(WEIGHT_MATRIX)
    if  match_cluster.index(i) == 0:
        for m in i:
            for n in CLUSTER_ELEM:
                if n not in i:
                    WEIGHT_MATRIX_Temp[CLUSTER_ELEM.index(n)][CLUSTER_ELEM.index(m)] = 777777777
        for k in match_cluster:	
            for l in range(len(k)):
                if i != k:
                    temp_value = WEIGHT_MATRIX_Temp[CLUSTER_ELEM.index(k[l])][CLUSTER_ELEM.index(i[0])]
                    WEIGHT_MATRIX_Temp[CLUSTER_ELEM.index(k[l])][CLUSTER_ELEM.index(i[0])] = -100000
                    external(WEIGHT_MATRIX_Temp, match_cluster, CLUSTER_ELEM, CLUSTER_ELEM.index(i[0]), CLUSTER_ELEM.index(k[l]))
                    WEIGHT_MATRIX_Temp[CLUSTER_ELEM.index(k[l])][CLUSTER_ELEM.index(i[0])] = temp_value
def minimum(A):
    minimal = 10000
    elem = 0
    for i in A:
        if CONDITION[A[0]][i] < minimal:
            minimal = CONDITION[A[0]][i]
            elem = i
    A.remove(elem)
    A[0] = elem
    return elem, A

def _incluster(A):
    minimal = 1000
    elem = 0
    for i in A:
        if CONDITION[A[0]][i] == 0:
            elem = i
    A.remove(elem)
    A[0] = elem
    return elem, A

def greedy(A):
    i=0
    array = [A[0]]
    arr = list(A)
    while len(arr) > 1:
        elem, arr = minimum(A)
        array.append(elem)
    return array

def tour_tsp(value1):
    T = []
    file = open(path2 + "Tours/GREEDY_2/" + str(value1), 'r')
    for i, line in enumerate(file):
        if i > 5 and i < 6 + len(CLUSTER_ELEM):
            line = line.replace("\n", "")
            T.append(int(line))
        elif i == 1:
            line = line.replace("\n", "")
            S = line[19:]
    file.close()
    return S, T

def TSP():
    for i in os.listdir(path2 + "CLKH-1.0/TSP/GREEDY_2/"):
        subprocess.run(["/home/belousov_an/Industrial/CLKH-1.0/CLKH", "/home/belousov_an/Industrial/CLKH-1.0/TSP/GREEDY_2/" + i], stdout=subprocess.PIPE, universal_newlines=True)
TSP()

compare_value = 0
compare_tour = []

for i in os.listdir(path2 + "Tours/GREEDY_2/"):
    compare_value, compare_tour = tour_tsp(i)
    if int(compare_value) < ctsp_lenght:
        ctsp_lenght = int(compare_value)
        ctsp_tour = deepcopy(compare_tour)

for i in CLUSTER_ELEM:
    max_cl += WEIGHT[i]

#print(match_cluster)


c = 0
for i in CONDITION:
    for j in i:
        if j == 0:
            c += 1

print(ctsp_lenght+100000, max_cl, c/(len(CONDITION)*len(CONDITION))) 

