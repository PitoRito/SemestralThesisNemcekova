import pandas as pd
import time
import numpy as np
import csv
import matplotlib.pyplot as plt
from scipy import signal
from numpy import arctan, sqrt
from numpy import sin, arange, pi
from scipy.signal import lfilter, firwin
import DataEditing

#Read data

data = pd.read_csv("BioSignals\PatrikOpenSignals.txt",delimiter=',', header = None)

# Remove first 3 columns

EditedData = DataEditing.OpensignalsDataEditing(data)

# add Seconds

DataWithSeconds = DataEditing.AddSeconds(EditedData)

# Transforming mV to Gs, values Cmin and Cmax and transfer function got from https://www.biosignalsplux.com/notebooks/Categories/Pre-Process/unit_conversion_ACC_rev.php
# DataInGs = DataEditing.DataToGs(DataWithSeconds)

# Converting to degrees

DataInDegrees = DataEditing.DataToDegrees (DataWithSeconds)

# setting 0

DataWithoutOffset = DataEditing.OffsetRemoving(DataInDegrees)

# Not filtred data

DataEditing.NotFilteredDataShow(DataWithoutOffset)

# Median Filter

DataEditing.MedianFilter(DataWithoutOffset, 101)

#LowPass filtering

DataEditing.LowPassFilter(DataWithoutOffset, 1000, 6, 300)