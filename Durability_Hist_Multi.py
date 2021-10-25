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

def load_function(cols, header):

    #Load Multiple files
    fileNames=fd.askopenfilenames()

    #for loop load the data
    dataList=[]
    loadTime=0
    for name in fileNames:
        print("Loading new file: "+name)
        t0=t.time()
        data=pd.read_csv(name,usecols=cols,index_col=False,header=header,skiprows=lambda x: x%20 != 0)
        dataList.append(data)
        t1=t.time()
        deltaT=t1-t0
        loadTime=loadTime+deltaT
    print("Finished loading files, total load time: "+str(round(loadTime,3))+" seconds")


    #Mesh all of the dataframes from dataList together into one dataFrame
    finalFrame=pd.concat(dataList,ignore_index=True)

    return(finalFrame)

def main():

    cols=["TC0 - DUT1 SCI50",
    "TC1 - DUT1 SCI60",
    "TC2 - DUT1 SCO40",
    "TC3 - DUT1 SWI50",
    "TC4 - DUT1 SWI60",
    "TC5 - DUT1 SWI70",
    "TC6 - DUT1 SWO40",
    "TC7 - DUT2 SCI50",
    "TC8 - DUT2 SCI60",
    "TC9 - DUT2 SCO40",
    "TC10 - DUT2 SWI50",
    "TC11 - DUT2 SWI60",
    "TC12 - DUT2 SWI70",
    "TC13 - DUT2 SWO40"]

    data = load_function(cols,0)


    # This does calculates the |Vdq| amplitude for each unit and makes in a new column called ICM2 - Udq (V)
    data['MAX - DUT1'] = data[cols[0:7]].max(axis=1)
    data['MAX - DUT2'] = data[cols[7:14]].max(axis=1)
    # This prints each datum as a hhistogram of units, IDK how to make all graphs pop up together

    col = 'MAX - DUT1'
    counts, bins = np.histogram(data[col],bins=[40,60,80,100,120,140,160,180,200])
    counts = counts/data[col].size

    bins = [50,70,90,110,130,150,170,190]
    fig, ax = plt.subplots()
    plt.bar(bins,counts,color='g',width=20)
    plt.xlabel("TC Temp "+col)
    plt.ylabel('Percentage')
    plt.title('Histogram of Temps')
    add_bar_labels(ax)
    plt.show()

    col = 'MAX - DUT2'
    counts, bins = np.histogram(data[col],bins=[40,60,80,100,120,140,160,180,200])
    counts = counts/data[col].size

    bins = [50,70,90,110,130,150,170,190]
    fig, ax = plt.subplots()
    plt.bar(bins,counts,color='g',width=20)
    plt.xlabel("TC Temp "+col)
    plt.ylabel('Percentage')
    plt.title('Histogram of Temps')
    add_bar_labels(ax)
    plt.show()


main()
