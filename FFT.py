# FFT is rough but works, try it in combination with Lecroy data and the Lecroy.py converter script
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import filedialog as fd
import time as t
from scipy.fft import fft, fftfreq

def single_load_function(cols,header):

    #Load Multiple files
    name=fd.askopenfilename()

    #Data columns to be imported
    #for loop load the data
    print("Loading new file: ")
    t0=t.time()
    data=pd.read_csv(name,usecols=cols,index_col=False,header=header)
    t1=t.time()
    deltaT=t1-t0
    print("Finished loading files, total load time: "+str(round(deltaT,3))+" seconds")

    return data

def main():
    cols=["Time (s)","A","B","C"]
    data = single_load_function(cols,0)
    N = 100*(len(data.index)//100)
    print(N)
    sampleRate = round(1/(data[cols[0]][1]-data[cols[0]][0]))
    print('Sample rate is: '+str(sampleRate/1000000)+' MS/s')
    yf = fft(data[cols[1:4]][0:N],axis=0)
    print(yf)
    xf = fftfreq(N,1.0/sampleRate)
    print(xf)
    plt.plot(xf[:N//2],2.0/N * np.abs(yf)[:N//2])
    plt.ylabel("Frequency")
    plt.xlabel("Amplitdue")
    plt.title("FFT")
    plt.grid()
    plt.show()
main()
