# This tool imports a bunch of selected MGI EOL snapshots and uses only the last data point (called newpoint in the snapshot), and does basic Stat analysis and plots histograms with 3sigma lines
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import filedialog as fd
import time as t

def np_print_full(arr):
    with np.printoptions(threshold=np.inf):
        print(arr)

def pd_print_full(x):
    pd.set_option('display.max_rows', len(x))
    print(x)
    pd.reset_option('display.max_rows')

def add_bar_labels(ax, space = 10):
    for rect in ax.patches:
        y_value = rect.get_height()
        x_value = rect.get_x() + rect.get_width()/2

        ax.annotate('{:,.2f}%'.format(100*y_value),
        (x_value, y_value),
        xytext=(0, space),
        textcoords='offset points',
        ha='center',
        va='top')

def load_function(cols, header, resample):

    #Load Multiple files
    fileNames=fd.askopenfilenames()

    #for loop load the data
    dataList=[]
    loadTime=0
    for name in fileNames:
        print("Loading new file: "+name)
        t0=t.time()
        data=pd.read_csv(name,usecols=cols,index_col=False,header=header,skiprows=lambda x: x%resample != 0)
        dataList.append(data)
        t1=t.time()
        deltaT=t1-t0
        loadTime=loadTime+deltaT
    print("Finished loading files, total load time: "+str(round(loadTime,3))+" seconds")


    #Mesh all of the dataframes from dataList together into one dataFrame
    finalFrame=pd.concat(dataList,ignore_index=True)

    return(finalFrame)

def main():

    cols=lambda x : True
    data = load_function(cols,1,1)

    saveDir = fd.askdirectory()
    saveFile = saveDir + '/Combined.csv'

    data.to_csv(saveFile,index=False)


main()
