import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import arctan, sqrt
from scipy import signal
from numpy import sin, arange, pi
from scipy.signal import lfilter, firwin

def OpensignalsDataEditing(data):
    first_column = data.columns[0]
    scnd_column = data.columns[1]
    EditedData = data.drop([first_column , scnd_column] , axis=1)
    for x in range(len(EditedData[2])):
        if EditedData[2][x] == 0.00000:
            EditedData[2][x] = 0.00001
        if EditedData[3][x] == 0.00000:
            EditedData[3][x] = 0.00001
        if EditedData[4][x] == 0.00000:
            EditedData[4][x] = 0.00001
    EditedData = EditedData[2].to_frame('x').join(EditedData[3].to_frame('y')).join(EditedData[4].to_frame('z'))
    return EditedData

def ADXLDataEditing(data):
    RoundedData = np.around(data , decimals = 5)
    for x in range(len(RoundedData[0])):
        if RoundedData[0][x] == 0.00000:
            RoundedData[0][x] = 0.00001
        if RoundedData[1][x] == 0.00000:
            RoundedData[1][x] = 0.00001
        if RoundedData[2][x] == 0.00000:
            RoundedData[2][x] = 0.00001
    EditedData = RoundedData[0].to_frame('x').join(RoundedData[1].to_frame('y')).join(RoundedData[2].to_frame('z')).join(data[3].to_frame('sec'))
    return EditedData


    # data[[(x == 0.0000) for x in data[0]]]
    # data[[(x == 0.0000) for x in data[1]]]
    # data[[(x == 0.0000) for x in data[2]]]

def AddSeconds(data):
    Seconds = np.arange(0 , np.size(data , 0) * 0.001 , 0.001 , dtype=float)
    Seconds = np.around(Seconds , decimals=3)
    data.insert(3 ,  "sec" , Seconds)
    return data

def DataToGs(data):
    Cmin=28000  
    Cmax=38000

    data[2] = (data[2].astype(float) - Cmin) / (Cmax - Cmin) * 2 - 1 
    data[3] = (data[3].astype(float) - Cmin) / (Cmax - Cmin) * 2 - 1 
    data[4] = (data[4].astype(float) - Cmin) / (Cmax - Cmin) * 2 - 1 
    RoundedInGs = np.around(data , decimals = 5)
    return RoundedInGs

def DataToDegrees(data):
    xAngle= []
    yAngle= []
    zAngle= []

    xAngle = arctan( data['x']/( sqrt( data['y'] ** 2 + data['z']**2)))
    yAngle = arctan( data['y']/( sqrt( data['x'] ** 2 + data['z']**2)))
    zAngle = arctan( sqrt( data['x']**2 + data['y'] ** 2)/data['z'])

    xAngle *= 180 ;    yAngle *= 180 ;    zAngle *= 180
    xAngle /= pi ;    yAngle /= pi ;    zAngle /= pi
    
    DataInDegrees = xAngle.to_frame('x').join(yAngle.to_frame('y')).join(zAngle.to_frame('z')).join(data['sec'].to_frame('sec'))
    RoundedInDegrees = np.around(DataInDegrees , decimals=5)
    return RoundedInDegrees

def OffsetRemoving(data):
    data['x'] = data['x'] - data['x'][0]
    data['y'] = data['y'] - data['y'][0]
    data['z'] = data['z'] - data['z'][0]
    RoundedWithoutOffset = np.around(data , decimals=5)
    return RoundedWithoutOffset

def NotFilteredDataShow(data):
    x= data['x']
    y= data['y']
    z= data['z']
    seconds= data['sec']

    plt.title('Pôvodný signál, os x')
    plt.plot(seconds, x, label='Pôvodný signál ')
    plt.xlabel('Čas [s]')
    plt.ylabel('Uhol [°]')
    plt.show()

    plt.title('Pôvodný signál, os y')
    plt.plot(seconds, y, label='Pôvodný signál')
    plt.xlabel('Čas [s]')
    plt.ylabel('Uhol [°]')
    plt.show()

    plt.title('Pôvodný signál, os z')
    plt.plot(seconds , z , label='Pôvodný signál')
    plt.xlabel('Čas [s]')
    plt.ylabel('Uhol [°]')
    plt.show()

def MedianFilter(data, window):
    x= data['x']
    y= data['y']
    z= data['z']
    seconds= data['sec']

    plt.title('Mediánový filter, os x')
    plt.plot(seconds , signal.medfilt(x , window))
    plt.xlabel('Čas [s]')
    plt.ylabel('Uhol [°]')
    plt.show()

    plt.title('Mediánový filter, os y')
    plt.plot(seconds , signal.medfilt(y , window))
    plt.xlabel('Čas [s]')
    plt.ylabel('Uhol [°]')
    plt.show()

    plt.title('Mediánový filter, os z')
    plt.plot(seconds , signal.medfilt(z , window))
    plt.xlabel('Čas [s]')
    plt.ylabel('Uhol [°]')
    plt.show()

def LowPassFilter(data, fs,fmax, numtaps):
    x= data['x']
    y= data['y']
    z= data['z']
    seconds= data['sec']
    cutoff= fmax / (fs / 2)
    FIR = firwin (numtaps , cutoff = cutoff , window = "hamming" , pass_zero='lowpass')
    filteredFIRx = signal.filtfilt (FIR , 1 , x , axis=0)
    filteredFIRy = signal.filtfilt (FIR , 1 , y , axis=0)
    filteredFIRz = signal.filtfilt (FIR , 1 , z , axis=0)

    plt.title('FIR filter, os x')
    plt.plot(seconds , filteredFIRx)
    plt.xlabel('Čas [s]')
    plt.ylabel('Uhol [°]')
    plt.show()

    plt.title('FIR filter, os y')
    plt.plot(seconds , filteredFIRy)
    plt.xlabel('Čas [s]')
    plt.ylabel('Uhol [°]')
    plt.show()

    plt.title('FIR filter, os z')
    plt.plot(seconds , filteredFIRz)
    plt.xlabel('Čas [s]')
    plt.ylabel('Uhol [°]')
    plt.show()
    