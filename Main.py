import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from FileReader import FindImages
from DataReduction import ReduceFunc
from ImageSaver import SaveFitsFile
from ImageMover import CombineImages

#Removes bias, scales with flat and combines the science images
#Result is saved as a .fit file
#SaveName is name of the result that is being saved
#FolderName is the name of the folder with science images
#BiasName is the name of the folder with the bias images
#FlatName is the name of the folder with the bias images
#The science images are combined by cross-correlating
#(x0,y0),(x0+size,y0+size) is the area that is being cross-correlated (smaller area to save time)
#If ShowResult is True the result will be plotted
def MakeFinalImage(SaveName,FolderName,FlatName,BiasName,x0=1000,y0=1000,size=300,ShowResult=False):

    RawImageList = FindImages(FolderName)
    
    Reduce = ReduceFunc(BiasName,FlatName)
    ImageList = Reduce(RawImageList)
    
    CombinedImage = CombineImages(ImageList,x0,y0,size)

    if(ShowResult):
        CombinedImage = CombinedImage[200:,200:]
        CombinedImage = CombinedImage[:-200,:-200]
        Vmin = 0#
        Vmax = np.amax(CombinedImage)/50

        plt.imshow(CombinedImage-np.average(CombinedImage),cmap="gray",vmin=Vmin,vmax=Vmax)
        plt.show()
    
    SaveFitsFile(CombinedImage,SaveName)
    
#-----Example-----#

#MakeFinalImage("NGC5845_5",["Data","NGC5845"],["Data","Flats"],["Data","Bias"],ShowResult=True,x0=1000,y0=1000,size=200)
#In this case the science images, flats and biases are in the folder C:\Users\Eigenaar\Desktop\La Palma\Data

#--/--Example--/--#
