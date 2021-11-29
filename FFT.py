# FFT is rough but works, try it in combination with Lecroy data and the Lecroy.py converter script
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import filedialog as fd
import time as t
from scipy.fft import fft, fftfreq

def np_print_full(arr):
    with np.printoptions(threshold=np.inf):
        print(arr)

def pd_print_full(x):
    pd.set_option('display.max_rows', len(x))
    print(x)
    pd.reset_option('display.max_rows')

def single_load_function(cols,header):

    name=fd.askopenfilename()

    print("Loading new file: ")
    t0=t.time()
    data=pd.read_csv(name,usecols=cols,index_col=False,header=header)
    t1=t.time()
    deltaT=t1-t0
    print("Finished loading files, total load time: "+str(round(deltaT,3))+" seconds")

    return data

def fft_algorithm(N,sampleRate,data,cols):
    X = 1.0/N * fft(data[cols][0:N],axis=0)
    freq = fftfreq(N,1.0/sampleRate)
    return X,freq

def get_fundamental(sampleRate,data):
    neg = np.signbit(data)
    zeroCross = (~neg[1:] & neg[:-1]).nonzero()[0]+1
#    np_print_full(zeroCross)
    badCross = ((zeroCross[1:] - zeroCross[:-1]) < data.size/40)
#    np_print_full(badCross)
    numBad = 0
    for idx in range(badCross.size):
        if(badCross[idx] == True):
            numBad = numBad + 1
        else:
            zeroCross[idx] = np.mean(zeroCross[idx-numBad:idx+1])
            numBad = 0
    zeroCross = np.delete(zeroCross,badCross.nonzero()[0])
#    print(zeroCross)

    wrongWay = []
    for idx in range(zeroCross[:-1].size):
        if(data[zeroCross[idx] + round(data.size/40)] < 0):
            wrongWay.append(idx)

    if (data[zeroCross[-1] - round(data.size/40)] > 0):
        wrongWay.append(zeroCross.size - 1)

    zeroCross = np.delete(zeroCross,wrongWay)

#    np_print_full(zeroCross)
    cycles = zeroCross.size - 1
    period = (zeroCross[-1] - zeroCross[0])/cycles
    fund = sampleRate/period
    return(fund)

def add_bar_labels(ax, space = 10):
    for rect in ax.patches:
        y_value = rect.get_height()
        x_value = rect.get_x() + rect.get_width()/2

        ax.annotate('{:,.1f}'.format(y_value),
        (x_value, y_value),
        xytext=(0, space),
        textcoords='offset points',
        ha='center',
        va='top')

def main():
    cols=["Time (s)","A","B","C"]

    data = single_load_function(cols,0)

    plt.plot(data[cols[0]],data[cols[1]],color='darkgreen')
    plt.plot(data[cols[0]],data[cols[2]],color='forestgreen')
    plt.plot(data[cols[0]],data[cols[3]],color='darkred')
    plt.xlabel("Time (s)")
    plt.figlegend(cols[1:4])
    plt.grid()
    plt.show()

    sampleRate = round(10/(data[cols[0]][10]-data[cols[0]][0]))
    print('Sample rate is: '+str(sampleRate/1000000)+' MS/s')

    fund = get_fundamental(sampleRate,data[cols[1]].to_numpy())
    print("Fundamental is: "+str(fund)+" Hz")

    cycle = sampleRate/fund
    cycles = len(data.index)//cycle
    N = int(cycle*(cycles))
    print('N = '+str(N)+' Samples')

    X,freq = fft_algorithm(N,sampleRate,data,cols[1:4])
    phase = np.arctan2(np.real(X),np.imag(X))
    XRe = 2.0 * np.abs(X)[:N//2]
    XAvg = np.mean(XRe,axis=1)

    freqRe = freq[:N//2]

    freqLim = freqRe<=fund*20

    fig, ax = plt.subplots()
    plt.bar(freqRe[freqLim][::int(cycles)], XAvg[freqLim][::int(cycles)],width=20,color=['darkgreen','forestgreen','darkred'])
    add_bar_labels(ax)
    plt.xlabel("Frequency")
    plt.ylabel("Amplitdue")
    plt.title("FFT")
    plt.grid()
    plt.show()

main()
