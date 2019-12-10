#!/root/anaconda3/bin/python3.7
import subprocess
import networkx as nx
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
from subprocess import Popen, PIPE, STDOUT, run
from itertools import groupby

start_time = time.time()

G = nx.DiGraph()

NUM_DET_NECESSARY = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49] #, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99]
DET_NECESSARY = []
matrix = []
path = "/home/belousov_an/Industrial/CLIQUE/"
path3 = "/home/belousov_an/Industrial/"
path1 = "/home/belousov_an/Industrial/DATA/data"
path2 = "/home/belousov_an/Industrial/DATA/data_con"
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
CLUSTERS_TEMP = []
WEIGHT_MATRIX_Temp = []
temp = []
num_cluster = [] # переменная, в которой хранится номера кластеров
Array = []
count = 0
seq = []
lscc = []
summa = 10000000000000
first_cl = 0
first_cluster = []
match_cluster = []
fin_cluster = []
tour = []
ctsp_lenght = 10000000
ctsp_tour = []
max_cl = 0

files_INSTANCES = glob.glob(path3 + 'Instances/CLIQUE/*')
files_TOURS = glob.glob(path3 + 'Tours/CLIQUE/*')
files_LSCC = glob.glob(path + 'LSCC/*')
files_TSP = glob.glob(path3 + 'CLKH-1.0/TSP/CLIQUE/*')

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


CONDITION = file_open_data_con(path2)
WEIGHT = file_open_data(path1)

for i in range(len(CONDITION)):
    CONDITION[i][i] = 777777777

N = len(WEIGHT)

for i in range(N):
    DET.append('A' + str(i))

for i in range(len(DET)):
    CONDITIONS[DET[i]] = CONDITION[i]

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


def array_el_true(A):
    array = [A]
    for i in DET:
        if COMPAT_MATRIX[A][DET.index(i)] == True:
            array.append(DET.index(i))
    return array

def maxclique_data_array(arr1):
	temp = []
	for i in arr1:
		for j in arr1:
			if i != j and COMPAT_MATRIX[i][j] == True:
				temp.append([i, j])
	return temp

def maxclique_greedy(A):
    c = [A[0]]
    for i in A:
        if proverka(c, i) == True:
           c.append(i)
    return c


def match_array(A):
    n = []
    new_n = []
    for i in A:
        if i not in n:
            n.append(i)
    for i in n:
        if (list(reversed(i))) in n:
            n.remove(list(reversed(i)))
    for i in n:
        if int(i[0]) > int(i[1]):
            i[0], i[1] = i[1], i[0]
    return n

for i in range(len(NUM_DET_NECESSARY)):
    tour.append(i+1)

def match(Matrix):
    for i in Matrix:
        for j in Matrix:
            if i != j:
                for k in i:
                    for n in j:
                        if k == n:
                            j.remove(n)    
    while ([] in Matrix):
        Matrix.remove([])
    return Matrix

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

def maxclique_file_input():
       edge = 0

       for i in tour:
           arr_temp = []
           file = open(path + "LSCC" + "/" + str(NUM_DET_NECESSARY[int(i)-1]) + ".wclq", 'w')
           arr_temp = deepcopy(array_el_true(NUM_DET_NECESSARY[int(i) - 1]))
           arr = deepcopy(maxclique_data_array(arr_temp))
           arr = match_array(arr)
           if arr == []:
               file.write("p edge " + str(len(DET)) + " " + str(len(arr)) + "\n")
               for l in range(len(DET)):
                   if l != NUM_DET_NECESSARY[int(i) - 1]:
                       file.write("v " + str(l + 1) + " " + '0')
                       file.write("\n")
                   else:
                       file.write("v " + str(l + 1) + " " + str(WEIGHTS[DET[l]]))
                       file.write("\n")
               for line in sorted(arr):
                   file.write("e ")
                   for s in line:
                       file.write(str(int(s) + 1) + " ")
               file.write("\n")
           else:
               file.write("p edge " + str(len(DET)) + " " + str(len(arr)) + "\n")
               for l in range(len(DET)):
                   file.write("v " + str(l + 1) + " " + str(WEIGHTS[DET[l]]))
                   file.write("\n")
               for line in sorted(arr):
                   file.write("e ")
                   for s in line:
                       file.write(str(int(s) + 1) + " ")
                   file.write("\n")
           file.close()

def maxclique():
    arr = []
    f_cl = 0
    summa = 999999999999
    for i in os.listdir(path + "LSCC"):
        p = 0
        lscc = []
        try:
            s = subprocess.run(["/home/belousov_an/TSM/tsm-release/tsm-mwc", "/home/belousov_an/Industrial/CLIQUE/LSCC/" + str(i)], stdout=subprocess.PIPE, universal_newlines=True)
            output = s.stdout.split('\n')
            for j in (output[len(output)-3].split(' ')):
                if j != "M" and j != "":
                    lscc.append(int(j)-1)
            i = i.replace(".", "").replace("wclq", "")
            for k in CONDITIONS['A' + str(i)]:
                if k != 0:
                    p += 1
            if p < summa:                
                f_cl = NUM_DET_NECESSARY.index(int(i))
                summa = p
        except:
            print("Что-то пошло не так!")
        arr.append(lscc)
    return arr, f_cl

maxclique_file_input()

CLUSTERS_TEMP, first_cl = maxclique()

#if first_cl != 0:
#    CLUSTERS_TEMP[first_cl], CLUSTERS_TEMP[0] = CLUSTERS_TEMP[0], CLUSTERS_TEMP[first_cl]
                                                                               
CLUSTERS_TEMP = deepcopy(match(CLUSTERS_TEMP))

for i in CLUSTERS_TEMP:
    if len(i) == 1 and i[0] not in NUM_DET_NECESSARY:
        CLUSTERS_TEMP.remove(i)

for i in CLUSTERS_TEMP:
	if i not in match_cluster:
		match_cluster.append(i)

CLUSTER_ELEM_TEMP = []

for i in match_cluster:
    for j in i:
        CLUSTER_ELEM_TEMP.append(j)

for i in NUM_DET_NECESSARY:
    if i not in CLUSTER_ELEM_TEMP:
        match_cluster.append(maxclique_greedy(array_true(i)))
        macth_cluster = deepcopy(match(match_cluster))
        for j in match_cluster[len(match_cluster)-1]:
            CLUSTER_ELEM_TEMP.append(j)

#print(match_cluster)

def digraph(A):
    array = []
    for i in A:
        G.clear()
        for j in i:
            G.add_node(j)
            for k in i:
                if COMPAT_MATRIX[j][k] == True and k != j:
                    #print(j, k)
                    G.add_edge(j, k)
            if len(list(nx.bfs_tree(G,j))) == len(i):
               #print(G.edges)
               array.append(list(nx.bfs_tree(G,j)))
               break
    return array

match_cluster = deepcopy(digraph(match_cluster))

for i in match_cluster:
    for j in i:
        CLUSTER_ELEM.append(j)

#print(match_cluster)
#print(CLUSTER_ELEM)

#CLUSTER_ELEM = [el for el, _ in groupby(sorted(CLUSTER_ELEM))]

data_atsp_top = ['NAME : DATA.gtsp', 'TYPE : AGTSP', 'DIMENSION : ' + str(len(CLUSTER_ELEM)), 'GTSP_SETS : ' + str(len(match_cluster)),
                 'EDGE_WEIGHT_TYPE: EXPLICIT', 'EDGE_WEIGHT_FORMAT: FULL_MATRIX', 'EDGE_WEIGHT_SECTION']

for i in match_cluster:
    for j in i:
        for k in i:
            if j != k and COMPAT_MATRIX[j][k] == False:
                CONDITION[j][k] = 777777777

for i in range(len(CLUSTER_ELEM)):
    temp_array = []
    for j in range(len(CLUSTER_ELEM)):
        temp_array.append(CONDITION[CLUSTER_ELEM[i]][CLUSTER_ELEM[j]])
    WEIGHT_MATRIX.append(temp_array)

def external(Matrix, Matrix_1, Matrix_2, value1, value2):
    count = 0
    file1 = open(path3 + "CLKH-1.0/TSP/CLIQUE/tsp" + str(value1) + str(value2) + ".par", 'w')
    file1.write("PROBLEM_FILE = /home/belousov_an/Industrial/Instances/CLIQUE/TOUR_TSP" + str(value1) + str(value2) + "\n")
    file1.write("OUTPUT_TOUR_FILE = /home/belousov_an/Industrial/Tours/CLIQUE/TOUR_TSP" + str(value1) + str(value2))	
    file = open(path3 + "Instances/CLIQUE/TOUR_TSP" + str(value1) + str(value2), 'w')
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
	if match_cluster.index(i) == 0:
		for m in i:
			for n in CLUSTER_ELEM:
				if n not in i:
					WEIGHT_MATRIX_Temp[CLUSTER_ELEM.index(n)][CLUSTER_ELEM.index(m)] = 777777777
		#for j in range(len(i)):
		for k in match_cluster:	
			for l in range(len(k)):
				if i != k:
					temp_value = WEIGHT_MATRIX_Temp[CLUSTER_ELEM.index(k[l])][CLUSTER_ELEM.index(i[0])]
					WEIGHT_MATRIX_Temp[CLUSTER_ELEM.index(k[l])][CLUSTER_ELEM.index(i[0])] = -1000000
					external(WEIGHT_MATRIX_Temp, match_cluster, CLUSTER_ELEM, CLUSTER_ELEM.index(i[0]), CLUSTER_ELEM.index(k[l]))
					WEIGHT_MATRIX_Temp[CLUSTER_ELEM.index(k[l])][CLUSTER_ELEM.index(i[0])] = temp_value

def tour_tsp(value1):
	T = []	
	file = open(path3 + "Tours/CLIQUE/" + str(value1), 'r')
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
	for i in os.listdir(path3 + "CLKH-1.0/TSP/CLIQUE"):
		subprocess.run(["/home/belousov_an/Industrial/CLKH-1.0/CLKH", "/home/belousov_an/Industrial/CLKH-1.0/TSP/CLIQUE/" + i], stdout=subprocess.PIPE, universal_newlines=True)
TSP()

compare_value = 0
compare_tour = []

for i in os.listdir(path3 + "Tours/CLIQUE/"):
	compare_value, compare_tour = tour_tsp(i)
	if int(compare_value) < ctsp_lenght:
		ctsp_lenght = int(compare_value)
		ctsp_tour = deepcopy(compare_tour)

for i in CLUSTER_ELEM:
	max_cl += WEIGHT[i]

#print(match_cluster)
#print(WEIGHT_MATRIX[35][34])
#print(COMPAT_MATRIX[83][89])
c = 0
for i in CONDITION:
    for j in i:
        if j == 0:
            c += 1
print(ctsp_lenght+1000000, max_cl, c/(len(CONDITION)*len(CONDITION)))
#print("--- %s seconds ---" % (time.time() - start_time))


