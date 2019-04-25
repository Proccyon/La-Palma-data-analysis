import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import time
from FileReader import FindImages
from DataReduction import ReduceFunc
from ImageSaver import SaveFitsFile

#-----SideFunctions-----#

def PredictTime(size,a=3.883,b=-19.08):
    return 2*np.exp(b)*(size**a)

#Finds index of an array where array has a global maximum
def MaxIndex(Array):
    return np.unravel_index(np.argmax(Array), Array.shape)
    
#Finds how much you have to move array 2 to match array 1
def GetOffset(Array1,Array2):
    Array1New = Array1 - np.average(Array1) #Remove background noise
    Array2New = Array1 - np.average(Array2)
    
    SelfCorr = signal.correlate2d(Array1New,Array1New,mode="same",boundary="symm") #Self-correlation and cross-correlation
    CrossCorr = signal.correlate2d(Array1New,Array2New,mode="same",boundary="symm")
    
    IndexSelf = MaxIndex(SelfCorr) #Finds the index where correlation is maximum
    IndexCross = MaxIndex(CrossCorr)
    
    dx = IndexCross[0]-IndexSelf[0]
    dy = IndexCross[1]-IndexSelf[1]
    
    return dx,dy
    
#Moves an array by (dx,dy)
def MoveImage(Image,dx,dy):
    return np.roll(np.roll(Image,dx,axis=0),dy,axis=1)    

#Cuts an array from (x0,y0) to (x0+size,y0+size)    
def Cutout(Image,x0,y0,size):
    return np.copy(Image[y0:y0+size,x0:x0+size])

#--/--SideFunctions--/--#

#-----MainFunctions-----#

#Combines mutliple science images by centering them
def CombineImages(ImageList,x0=1000,y0=1000,size=400):
    
    #Predicts time needed to execute centering
    print("Predicted processing time: "+str(round(PredictTime(size)*len(ImageList)/60,2))+"m")
    time.sleep(0.5)
    
    #Takes a small part of the first image
    #Taking CrossCorrelations takes a lot of time, only a part of the image is used
    ZeroImageCutout = Cutout(ImageList[0],x0,y0,size) 
    OutputImage = np.copy(ImageList[0])
    
    #Goes through all images, moves them and adds them together
    for i in range(1,len(ImageList)):
        ImageCutout = Cutout(ImageList[i],x0,y0,size)
        dx,dy = GetOffset(ZeroImageCutout,ImageCutout)
        OutputImage += MoveImage(ImageList[i],dx,dy)
        print("{} Image centered, {} more to go...".format(i,len(ImageList)-i-1))
        
        
    return OutputImage / len(ImageList)

#--/--MainFunctions--/--#

#-----Example-----#
RawImageList = FindImages(["Data","M82"])

Reduce = ReduceFunc(["Data","Bias"],["Data","Flats"])
ImageList = Reduce(RawImageList)

x0 = 1000
y0 = 1000
size = 200

#M82 = CombineImages(ImageList,x0,y0,size)
#I = ImageList[0]
#plt.imshow(I-np.average(I),cmap="gray",vmin=100,vmax=80000)
#plt.show()

#SaveFitsFile(M82,"M82")

#--/--Example--/--#