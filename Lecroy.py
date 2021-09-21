import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import filedialog as fd
import time as t

def lecroy_load_function():

    #Load Multiple files
    fileNames=fd.askopenfilenames()

    #Data columns to be imported
    cols=["Time",
          "Ampl"]

    #for loop load the data
    dataList=[]
    t0=t.time()
    print("Loading new file: ")
    dataList.append(pd.read_csv(fileNames[0],usecols=cols[0:2],index_col=False,header = 4))
    dataList.append(pd.read_csv(fileNames[1],usecols=cols[1:2],index_col=False,header = 4))
    dataList.append(pd.read_csv(fileNames[2],usecols=cols[1:2],index_col=False,header = 4))
    t1=t.time()
    deltaT=t1-t0
    print("Finished loading files, total load time: "+str(round(deltaT,3))+" seconds")

    #Mesh all of the dataframes from dataList together into one dataFrame
    finalFrame=pd.concat(dataList,ignore_index=True,axis=1)
    #relabelling columns
    newCols = ['Time (s)','A','B','C']
    finalFrame = finalFrame.rename(columns={ind : newCols[ind] for ind in range(4)})
    print(finalFrame)
    #Return dataframe and used columns
    return finalFrame,newCols

def main():
    finalFrame,cols = lecroy_load_function()
    saveDir = fd.askdirectory()
    saveFile = saveDir + '/scopeOutput.csv'
    finalFrame.to_csv(saveFile,index=False)

main()
