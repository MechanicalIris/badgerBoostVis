# -*- coding: utf-8 -*-
#TODO: Change legend font to larger one
#Change output to mp4
#Adjust for database download + implement time display
#Order of read in may have to be ammended for this
"""
Created on Thu Sep  2 10:23:51 2021
@author: Robin
Badger-boost visualisation
"""
#Imports#####
#conda install -c conda-forge ffmpeg-python
import json
import numpy as np
from matplotlib import pyplot as plt
import os
import cv2
import re
from datetime import datetime
from natsort import natsorted, ns
#Variables/initializations
colours = plt.cm.jet(np.linspace(0.1,1,10))
files = []
maximumx = []
minimumx = []
minimumy = []
maximumy = []
counter = 0
numbers = re.compile(r'(\d+)')
def numericalSort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts
#NOTE: Must think about file naming and how it reads in files sequentially
directory = 'C:\\Users\\Robin\\Desktop\\BBFinal'

for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    if os.path.isfile(f) and filename.endswith('.json'):
        with open(f, 'r') as readIn:
            data2 = json.load(readIn)
        uD2 = data2['userData'].keys()
        for i in uD2:
    #print(data2['userData'][i].keys())
            if "nonNativeBalance" in data2['userData'][i]:
                counter+=1
                files.append(f)
                #print(os.path.basename(f))
                break
        
files = natsorted(files, key=lambda y: y.lower())
#print(files)
#from sklearn.cluster import AgglomerativeClustering
#Notes
#Needs to be changed for the download model
#Need to scan through files first to find the global x and y maximum
#Subroutines###################################
#Gradient and intercept calculator for colour gradient
#Arguments: x1,y1,x2,y2
#Returns: gradient, intercept
def gradientIntercept(x1,y1,x2,y2):
    m = (y2-y1)/(x2-x1)
    c = y1 - (m*x1)
    return m,c
#Cleanup png files
def cleanUp():
    for k in range(1,len(files)+1):
        fileName = "%i.png" % k
        os.remove(fileName)
#Create video subroutine - takes in the directory where the pngs have been created.
#Void return
def createVideo(path):
    images = natsorted([img for img in os.listdir(path) if img.endswith(".png")], key=lambda y: y.lower())
    frame = cv2.imread(os.path.join(path, images[0]))
    height, width, layers = frame.shape
    fps = 3
   # video = cv2.VideoWriter('visualisation.avi', 0, fps, (width,height))
    video = cv2.VideoWriter('output.mp4',0x7634706d , fps, (width,height))
    for image in images:
        video.write(cv2.imread(os.path.join(directory, image)))
    cv2.destroyAllWindows()
    video.release()
#Setup Axis for plotting
def setAxis(date):
    ax.clear()
    plt.rcParams.update({'font.size': 30})
    ax.set_yscale('log')
    ax.set_xscale('log')
    ax.set_xlim([minx,maxx])
    ax.set_ylim([miny,maxy])
    ax.tick_params(axis='x', labelsize=30, which='both', length=10)
    ax.tick_params(axis='y', labelsize=30, which='both', length=10)
    ax.set_xlabel('Non Native Balance ($)', fontsize=30)
    ax.set_ylabel('Native Balance ($)', fontsize=30)
    ax.set_title('Native vs. Non Native Balance (Log-Log Scale)', fontsize=30)
    ax.grid()
    ax.plot(x,x,label ='s = 1', color = colours[0])
    ax.plot(x,20*x, label='s = 20', color = colours[1])
    ax.plot(x,150*x, label='s = 150', c = colours[2])
    ax.plot(x,200*x, label='s = 200', color = colours[3])
    ax.plot(x,500*x, label='s = 500', color = colours[4])
    ax.plot(x,600*x, label='s = 600', color = colours[5])
    ax.plot(x,1200*x, label='s = 1200', color = colours[6])
    ax.plot(x,1400*x, label='s = 1400', color = colours[7])
    ax.plot(x,2000*x, label='s = 2000', color = colours[8])
    ax.text(0.5, 0.5, date, size = 30)
    ax.legend(title='Stake Ratio, s', loc='upper right', fontsize=30)
    
#Generates the array for plotting - takes in a dictionary - extracted from json file in this context
#Returns in this order: array for nonzero stake data, array for zero stake data, number of points which have non zero stake ratio, 
#maximum non native, minimum non native, maximum native, minimum native
#For the nonzero stake data array:
#Zeroth column: non Native (x)
#First column: native (y)
#Second column: stake ratio
#Third column: float used to assign colour
def generateArray(badgerDict):
    dim = len(badgerDict['userData'])
    uD = badgerDict['userData'].keys()
    userDataZero = []
    userDataNonZero = []
    dim = 0
    for i in uD:
        
        ls = []
        #print(badgerDict['userData'][i])
        ls.append(badgerDict['userData'][i]['nonNativeBalance'])
        ls.append(badgerDict['userData'][i]['nativeBalance'])
        ls.append(badgerDict['userData'][i]['stakeRatio'])
        sR = badgerDict['userData'][i]['stakeRatio']
        if sR != 0:
            dim+=1
            #If statements used to set appropriate colour
            if 0 < sR <=1:
                #Checked
                ls.append((gradientIntercept(0,0,1,0.1)[0]*sR)+gradientIntercept(0,0,1,1)[1])
            if 1 < sR <=20:
                #Checked
                ls.append((gradientIntercept(1,0.1,20,0.2)[0]*sR)+gradientIntercept(1,0.1,20,0.2)[1])
            if 20 < sR <=150:
                #Checked
                ls.append((gradientIntercept(20,0.2,150,0.3)[0]*sR)+gradientIntercept(20,0.2,150,0.3)[1])
            if 150 < sR <=200:
                #Checked
                ls.append((gradientIntercept(150,0.3,200,0.4)[0]*sR)+gradientIntercept(150,0.3,200,0.4)[1])
            if 200 < sR <=500:
                #Checked
                ls.append((gradientIntercept(200,0.4,500,0.5)[0]*sR)+gradientIntercept(200,0.4,500,0.5)[1])
            if 500 < sR <=600:
                #Checked
                ls.append((gradientIntercept(500,0.5,600,0.6)[0]*sR)+gradientIntercept(500,0.5,600,0.6)[1])
            if 600 < sR <=1200:
                #Checked
                ls.append((gradientIntercept(600,0.6,1200,0.7)[0]*sR)+gradientIntercept(600,0.6,1200,0.7)[1])
            if 1200 < sR <=1400:
                #Checked
                ls.append((gradientIntercept(1200,0.7,1400,0.8)[0]*sR)+gradientIntercept(1200,0.7,1400,0.8)[1])
            if 1400 < sR <=2000:
                #Checked
                ls.append((gradientIntercept(1400,0.8,2000,0.9)[0]*sR)+gradientIntercept(1400,0.8,2000,0.9)[1])
            if sR > 2000:
                #Checked
               ls.append((gradientIntercept(1400,0.8,2000,0.9)[0]*sR)+gradientIntercept(1400,0.8,2000,0.9)[1])
                
            userDataNonZero.append(ls)
            continue
        #For zero Sr data points
        ls.append(0)
        userDataZero.append(ls)
    sparseData = np.array(userDataZero)    
    data = np.array(userDataNonZero)
    minx = np.amin(data[:,[0]])
    maxx = np.amax(data[:,[0]])
    miny = np.amin(data[:,[1]])
    maxy = np.amax(data[:,[1]])
    return data, sparseData, dim, maxx, minx, maxy, miny
#Read in JSON files########### 
for k in range(0,len(files)):
    with open(files[k], 'r') as readIn:
        data2 = json.load(readIn)  
    maximumx.append(generateArray(data2)[3])
    minimumx.append(generateArray(data2)[4])
    maximumy.append(generateArray(data2)[5])
    minimumy.append(generateArray(data2)[6])   
maxx = max(maximumx)
minx = min(minimumx)
maxy = max(maximumy)
miny = min(minimumy)   
minimum = min(minx,miny)
maximum = max(maxx,maxy)    
x = np.linspace(minimum,maximum,10000)
#userDataNonZeroMain[i][j] - use to access jth user of ith data set
fig = plt.figure(figsize=(30, 30), dpi=40)
ax = fig.add_subplot(111)
#Generate plots and save as pngs
for k in range(0,len(files)):
    print(k,'/',len(files)-1)
    f = natsorted(files, key=lambda y: y.lower())[k]
    unixTimeCode = int(re.search(r'\d+', f).group())
    dateTime = datetime.utcfromtimestamp(unixTimeCode).strftime('%Y-%m-%d %H:%M:%S')
    print(dateTime)
    setAxis(dateTime)
    with open(f, 'r') as readIn:
        data2 = json.load(readIn)  
    data3 = generateArray(data2)[0]
    for j in range(0,generateArray(data2)[2]):
        ax.plot(data3[j,0],data3[j,1], color = plt.cm.rainbow(data3[j,3]), marker='o', markersize=10)
    l = k+1
    fileName = "%i.png" % l
    plt.savefig(fileName)   
createVideo(directory)
#Cleanup - delete pngs produced
cleanUp()
plt.close()
