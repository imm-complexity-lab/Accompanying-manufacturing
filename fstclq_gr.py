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
from pprint import pprint

start_time = time.time()
G = nx.DiGraph()

NUM_DET_NECESSARY = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49] #, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99]
DET_NECESSARY = []
matrix = []
path = "/home/belousov_an/Industrial/"
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
CLUSTERS_TEMP = []
WEIGHT_MATRIX = []
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
max_cl = 0


files_INSTANCES = glob.glob(path + 'Instances/CLIQUE_2/*')
files_TOURS = glob.glob(path + 'Tours/CLIQUE_2/*')
files_LSCC = glob.glob(path + 'CLIQUE_2/LSCC/*')
for f in files_TOURS:
    os.remove(f)
for f in files_INSTANCES:
    os.remove(f)
for f in files_LSCC:
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

N = len(WEIGHT)

for i in range(N):
    DET.append('A' + str(i))

for i in NUM_DET_NECESSARY:
    DET_NECESSARY.append('A' + str(i))

for i in range(len(DET)):
    CONDITIONS[DET[i]] = CONDITION[i]

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

def maxclique_file_input():
       edge = 0

       for i in tour:
           arr_temp = []
           file = open(path + "CLIQUE_2/LSCC" + "/" + str(NUM_DET_NECESSARY[int(i)-1]) + ".wclq", 'w')
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
    for i in os.listdir(path + "CLIQUE_2/LSCC"):
        p = 0
        lscc = []
        try:
            s = subprocess.run(["/home/belousov_an/TSM/tsm-release/tsm-mwc", "/home/belousov_an/Industrial/CLIQUE_2/LSCC/" + str(i)], stdout=subprocess.PIPE, universal_newlines=True)
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

#print(CLUSTERS_TEMP)

for i in CLUSTERS_TEMP:
    #print(i, type(i))
    if len(i) == 1 and i[0] not in NUM_DET_NECESSARY:
        #print(i)
        CLUSTERS_TEMP.remove(i)

#print(CLUSTERS_TEMP)

for i in CLUSTERS_TEMP:
    if i not in match_cluster:
        match_cluster.append(i)

for i in match_cluster:
    for j in i:
           CLUSTER_ELEM.append(j)

for i in NUM_DET_NECESSARY:
    if i not in CLUSTER_ELEM:
        match_cluster.append(maxclique_greedy(array_true(i)))
        macth_cluster = deepcopy(match(match_cluster))
        for j in match_cluster[len(match_cluster)-1]:
            CLUSTER_ELEM.append(j)

#print(match_cluster)

def digraph(A):
    array = []
    for i in A:
        for j in i:
            G.add_node(j)
            for k in i:
                if COMPAT_MATRIX[j][k] == True and k != j:
                    G.add_edge(j, k)
            if len(list(nx.bfs_tree(G,j))) == len(i):
                #print(list(nx.bfs_tree(G,j)))
                array.append(list(nx.bfs_tree(G,j)))
                break
    return array

match_cluster = deepcopy(digraph(match_cluster))

#print(match_cluster)
                                	
CLUSTER_ELEM = [el for el, _ in groupby(sorted(CLUSTER_ELEM))]

first_cluster = deepcopy(match_cluster[0])
fin_cluster.append(first_cluster)

for i in match_cluster:
    for j in i:
        for k in i:
            if j != k and COMPAT_MATRIX[j][k] == False:
                CONDITION[j][k] = 777777777

def cluster_minimum(A):
    minimum = 1000000
    array = []
    idx = 0
    first_cluster = deepcopy(fin_cluster)[len(fin_cluster)-1]
    for i in range(1, len(A)):
        A[i].insert(0, first_cluster[len(first_cluster)-1])
        arr = deepcopy(A[i])
        if CONDITION[arr[0]][arr[1]] < minimum:
            minimum = CONDITION[arr[0]][arr[1]]
            array = deepcopy(arr)
            array.remove(arr[0])
            idx = i
    if array == []:
        minimum = 0
    return array, idx, minimum


def greedy_cluster(A):
    arr = []
    min = 0
    while len(A) > 1:
        arr, idx, m = cluster_minimum(deepcopy(A))
        if arr != []:
            fin_cluster.append(arr)
        A.remove(A[idx])
        A[0] = arr
        min += m
    return fin_cluster, min


for i in match_cluster:
	for j in i:
		max_cl += WEIGHT[j]

fin_array, tour_min = greedy_cluster(deepcopy(match_cluster))

    
#print(match_cluster)

c = 0
for i in CONDITION:
    for j in i:
        if j == 0:
            c += 1

print(tour_min, max_cl, c/(len(CONDITION)*len(CONDITION)))


