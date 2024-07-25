# -*- coding: utf-8 -*-
"""
Created on Mon Jul  8 11:01:38 2024

@author: Mateo-drr
"""

import byble as byb
import matplotlib.pyplot as plt
from pathlib import Path
from scipy.io import loadmat
import numpy as np

#PARAMS
fc=6e6
fs=50e6
idx=0
date ='05Jul'
imgtype = 'Rf' #image type to be loaded
fkey = 'rf' #dictionary key of the mat data
depthCut=6292
highcut=fc+1e6
lowcut=fc-1e6
frameLines=129
save=True
frameCrop=False #manually crop frames

#Get list of files in directory
current_dir = Path(__file__).resolve().parent.parent 
datapath = current_dir / 'data' / 'acquired' / date / 'pydata'
fileNames = [f.name for f in datapath.iterdir() if f.is_file()]

_=input()
for idx in range(0,len(fileNames)):
    print('Working on img', idx)
    ###############################################################################
    #Load matlab data
    ###############################################################################
    #load a selected file
    file = fileNames[idx]
    mat_data = loadmat(datapath / file)
    img = mat_data[fkey][:depthCut,:]
    
    ###############################################################################
    #Processing
    ###############################################################################
    #filter the data
    imgfilt = byb.bandFilt(img, highcut=highcut, lowcut=lowcut, fs=fs, N=len(img[:,0]), order=6)
    #plot fouriers
    byb.plotfft(img[:,0], fs)
    byb.plotfft(imgfilt[:,0], fs)
    
    #normalize
    imgfiltnorm = 20*np.log10(np.abs(imgfilt)+1) # added small value to avoid log 0
    
    # Plot the data
    byb.plotUS(20*np.log10(np.abs(imgfilt)+1))
    plt.show()
    byb.plotUS(imgfiltnorm)
    plt.show()
    
    ###############################################################################
    #Frame crop
    ###############################################################################
    if frameCrop:
        #Find index of the frames
        fidx = byb.findFrame(imgfiltnorm,frameLines,getframes=False)
        #Crop the frames without normalization
        frames = byb.cropFrames(imgfilt, fidx)
        #Merge frames to remove noise
        image = np.mean(frames,axis=0)
        #Plot
    
    else:
        #TODO check shape of array with already cut frames to do a mean
        pass
        
    byb.plotUS(20*np.log10(np.abs(image)+1))
    plt.show()
    
    ###############################################################################
    #Save file
    ###############################################################################
    if save:
        np.save(datapath.parent / 'processed' / f'{imgtype.lower()}_cf_{idx:03d}_{fidx[0]+1}',image)


