from cProfile import label
from inspect import trace
from itertools import count
import os
import sys
HERE = os.path.dirname(os.path.abspath(__file__))
SIMULATIONCONTROL = os.path.dirname(HERE)
sys.path.append(SIMULATIONCONTROL)

import matplotlib as mpl
mpl.use('Agg')
import math
import matplotlib.pyplot as plt
import numpy as np
from resultlib import *
import seaborn as sns
plt.rcParams.update({'font.size': 13})
plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42


if __name__ == '__main__':
    tasksAssemble = [] 
    for run in sorted(get_runs())[::-1]:
        tasksAssemble.append(get_pure_task(run))
    tasksAssemble2 = list(set(tasksAssemble))
    print('Assemble', tasksAssemble2)
    # for i in range(len(tasksAssemble2)):
    #     tasksAssemble2[i] = tasksAssemble2[i].replace('.','_')
    # print('Assemble', tasksAssemble2)
    a = 1
    b = 1
    c = 1
    sum = 0
    sum1 = 0
    sum2 = 0
    count1 = 1
    count2 = 1
    bench = []
    lowfre = []
    quickfre = []
    lowfre1 = []
    quickfre1 = []
    rot = []
    tasksAssemble2 = ['cholesky','radix','lu.cont','fluidanimate','barnes',
                      'water.nsq','streamcluster','blackscholes','swaptions',
                      'radiosity','ocean.cont','bodytrack','fft']
    for i in tasksAssemble2:
        for run in sorted(get_runs())[::-1]:
            if(i == get_pure_task(run) and 'ttsp' == get_scheduling(run)):
                a = get_average_response_time(run)
                #print("f100 is ",a), 
            elif(i == get_pure_task(run) and 'ondemand' == get_scheduling(run)):
                #print(get_data(run))
                b = get_average_response_time(run)
                
                 
        sum = sum + 100-np.round((a/b) * 100, 3)
        count1 = count1 * np.round((b/a-1) * 100, 2)
        bench.append(i)
        rot.append(a)
        lowfre.append(b)
        #lowfre1.append(np.round((b/a-1) * 100, 3))
        lowfre1.append(100-np.round((a/b) * 100, 2))
        #print(i,' speedup: ', np.round((b/a-1) * 100, 2))
        print(i,' speedup: ', 100-np.round((a/b) * 100, 3))
    # bench.append('Avg(speedup)')
    # rot.append(0)
    # lowfre.append(0)
        
    ssize = len(rot)
    for i in range(ssize):
        print('('+bench[i]+','+str(rot[i])+')')
    for i in range(ssize):
        print('('+bench[i]+','+str(lowfre[i])+')')
    for i in range(ssize):
        print('('+bench[i]+','+str(lowfre1[i])+')')
    for i in range(ssize):
        print('('+str(i+1)+','+str(rot[i])+')')
    for i in range(ssize):
        print('('+str(i+1)+','+str(lowfre[i])+')')
    print("The speed up is ", sum / (ssize))
    x=np.arange(ssize)
    cmap = plt.cm.get_cmap("Set3", 10)
    fig, ax = plt.subplots(figsize=(10,4.3))  
    bar_width=0.2
    ln1 = ax.bar(x,          rot,bar_width,color=cmap(0),edgecolor="k",hatch='***',label='3D-stacked T-TSP')
    ln2 = ax.bar(x+bar_width,lowfre,bar_width,color=cmap(1),edgecolor="k",hatch='///',label='ondemand')
    ax.legend(prop={'size': 12}, loc=2, ncol=1,facecolor=None, framealpha=0.3)
    box = ax.get_position()
    ax.set_position([box.x0 - 0.07, box.y0 + 0.05, box.width * 1.12, box.height * 1.03])
    plt.xticks(x+bar_width/2,bench,rotation=21)
    #lowfre1.append(sum / (ssize))
    ax1 = ax.twinx()
    ln3 = ax1.bar(x+2 * bar_width,lowfre1,bar_width,color=cmap(3),edgecolor="k",hatch='+++',label='speedup')
    box = ax1.get_position()
    plt.axhline(sum / (ssize),color=cmap(7),linestyle='--')
    ax1.set_position([box.x0 - 0.07, box.y0 + 0.05, box.width * 1.12, box.height * 1.03])
    ax1.legend(prop={'size': 12}, loc=1, ncol=1,facecolor=None, framealpha=0.3)
    
    # ln = ln1 + ln2 + ln3
    # labs = [l.get_label() for l in ln]
    # ax.legend(ln,labs,loc = 0)
    #ax1.legend(ln,labs,loc = 0,prop={'size': 12},facecolor=None, framealpha=0.3)
    
    
    ax.set_ylabel("Execution time(ns)")
    ax1.set_ylabel("Speedup(%)")
    fig.savefig('./speedup.pdf',format='pdf')
    
    
    
             
             
  