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
matrix = []
path = "/home/belousov_an/Industrial/DATA/data"
path1 = "/home/belousov_an/Industrial/DATA/data_con"
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
match_cluster = [] # сформированные кластера
fin_cluster = []
max_cl = 0

files_INSTANCES = glob.glob(path + 'Instances/*')
files_TOURS = glob.glob(path + 'Tours/*')
files_LSCC = glob.glob(path + 'LSCC/*')
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

#print(CONDITION[6][11])

# Убираем повторяющиеся элемненты в кластерах
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


CLUSTERS_TEMP = deepcopy(match(CLUSTERS_TEMP))

for i in CLUSTERS_TEMP:
    if len(i) == 1 and i[0] not in NUM_DET_NECESSARY:
            CLUSTERS_TEMP.remove(i)

for i in CLUSTERS_TEMP:
    if i not in match_cluster:
                 match_cluster.append(i)

#CLUSTER_ELEM = [el for el, _ in groupby(sorted(CLUSTER_ELEM))]

# Матрица весов для элементов кластера
for i in range(len(CLUSTER_ELEM)):
    temp_array = []
    for j in range(len(CLUSTER_ELEM)):
        temp_array.append(CONDITION[CLUSTER_ELEM[i]][CLUSTER_ELEM[j]])
    WEIGHT_MATRIX.append(temp_array)

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

first_cluster = deepcopy(match_cluster[0])

fin_cluster.append(first_cluster)

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
    return array, idx, minimum


def greedy_cluster(A):
    arr = []
    min = 0
    while len(A) > 1:
        arr, idx, m = cluster_minimum(deepcopy(A))
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
