from os import listdir
from os.path import isfile, join
from pyproj import Transformer
# numpy нужен для scipy
import numpy as np
from scipy.optimize import minimize

import os

# записи txt-файлов
import sys

import math

#для записи вложенных многоугольников
import pickle

###############################imports from shapely#######################
import shapely
from shapely import ops
from shapely.geometry import Point
from shapely.geometry import LinearRing
from shapely.geometry import Polygon
from shapely.geometry import LineString
from shapely import wkt
from shapely.ops import linemerge, unary_union, polygonize
import matplotlib.pyplot as plt

#ускоряем shapely
from shapely import speedups
speedups.enable()

#matplotlib
import matplotlib.pyplot

#for sorting:
from operator import itemgetter, attrgetter

with open('waypoints.txt', 'r', encoding='utf-8') as g:
    data=g.readlines()


num_list = []
str_num = str('0')
mark_num = 0

for line in data:
    for i in range(len(line)):
        if (line[i].isspace() == True):
            mark_num = 0
            if (str_num != 0):
                num_list += [float(str_num)]
            str_num = str('0')
        elif (line[i].isdigit() == True) or (line[i] == '.') :
            if (mark_num == 0):
                 str_num = str(line[i]) 
            else:
                str_num += str(line[i])
            mark_num = 1


wgs_coords = []
for num in num_list:
    if ((math.floor(num) == 45) or (math.floor(num) == 50)) and (num != 45) and (num != 50) : 
        wgs_coords += [num]




coords = []
for i in range(int(len(wgs_coords)/2)):
    coords += [[wgs_coords[2*i], wgs_coords[2*i+1]] ]

print("coords = ", coords)

#print("len(coords) = ", len(coords)) 


name_kml = "epsg:4326" # names of CRS used
name_ortog = "epsg:20009"
transformer = Transformer.from_crs(name_kml, name_ortog) # рассматриваем трансформации 2D --> 2D или 3D --> 3D.

coords_ortog = []

for i in range(len(coords)):
    x, y = transformer.transform(coords[i][0], coords[i][1])
    coords_ortog += [[x, y]]

print("coords_ortog = ", coords_ortog)

lengths2 = []
for i in range(len(coords_ortog)-1):
    lengths2 += [math.sqrt((coords_ortog[i][0] - coords_ortog[i+1][0])**2 + (coords_ortog[i][1] - coords_ortog[i+1][1])**2)]

print("lengths2 = ", lengths2)

lengths = []
for i in range(len(coords_ortog)-1):
    if (i%2 == 1):
        lengths += [math.sqrt((coords_ortog[i][0] - coords_ortog[i+1][0])**2 + (coords_ortog[i][1] - coords_ortog[i+1][1])**2)]


areas2 = []
for i in range(len(lengths)):
    areas2 += [lengths[i] * 6]


print("len(areas2) = ", len(areas2))
print("areas2 = ", areas2)




print("max(areas2) = ", max(areas2))



def count_k_s(areas, t_turn, Velocity, height ):
    k = len(areas) #total number
    S_total = sum(areas)
    time_opt = ((S_total/(height*Velocity)) + k*t_turn)/3

    print("time_opt = ", time_opt)
    
    time = 0
    mark1 = 0
    mark2 = 0
    k1 = 0
    k2 = 0
    for i in range(len(areas)):
        
        time += t_turn + areas[i]/(height*Velocity)
        if (mark1 == 0):
            if (time >= time_opt):
                mark1 = 1
                k1 = i+1
        elif (mark2 == 0):
            if (time >= 2*time_opt):
                mark2 = 1
                k2 = i+1
    
    print("time = ", time)

    return [k1, k2 - k1, k - k2]


t_turn = 10

height = 6

Velocity = 6

print("count_k_s(areas, t_turn, Velocity, height )=",count_k_s(areas2, t_turn, Velocity, height ))



