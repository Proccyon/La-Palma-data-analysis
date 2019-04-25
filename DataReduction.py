import numpy as np
from FileReader import FindImages
import matplotlib.pyplot as plt

#-----SideFunctions-----#

#Makes a superbias by taking the average of multiple biases
def MakeSuperBias(BiasList):
    SuperBias = np.zeros(BiasList[0].shape)
    for Bias in BiasList:
        SuperBias += Bias
    return SuperBias / len(BiasList)

#Makes a superflat by subtracting the bias and taking the average
def MakeSuperFlat(FlatList,Bias):
    SuperFlat = np.zeros(FlatList[0].shape)
    i = 0
    for Flat in FlatList:
        i+=1
        Flat = Flat.astype(float)-Bias.astype(float)
        #plt.figure()
        #plt.title(str(i))
        #plt.imshow(Flat[1000:300+1000,1000:300+1000])
        #plt.show()
        
        SuperFlat += Flat / np.amax(Flat)
    return SuperFlat / np.amax(SuperFlat)

#--/--SideFunctions--/--#

#-----MainFunctions-----#

#Removes the bias from an image and scales by the flat
#If multiple images have to be reduced make 'Image' as list of images
def Reduce(ImageList,BiasFolder,FlatFolder):
    BiasList = FindImages(BiasFolder)
    SuperBias = MakeSuperBias(BiasList)
       
    FlatList = FindImages(FlatFolder)
    SuperFlat = MakeSuperFlat(FlatList,SuperBias)

    #If ImageList is indeed a list go through each image seperately
    if(type(ImageList)==list):
        ReducedImageList = []
        for Image in ImageList:
            ReducedImageList.append((Image-SuperBias)/SuperFlat)
        return ReducedImageList
        
    #If ImageList is a single image return this
    return (ImageList-SuperBias)/SuperFlat
    

#Creates a function simmilar to 'Reduce' without having to input BiasFolder and FlatFolder
def ReduceFunc(BiasFolder,FlatFolder):
    return lambda Image : Reduce(Image,BiasFolder,FlatFolder)
    
#--/--MainFunctions--/--#

#-----Example-----#
#Images = FindImages(["Data","M82"])
#ReduceFunction = ReduceFunc(["Data","Bias"],["Data","Flats"])
#ReducedImage = ReduceFunction(Images[0])

#plt.figure()
#plt.imshow(np.log10(ReducedImage),cmap="Greys",vmin=4,vmax=5.2)
#plt.show()

#--/--Example--/--#
    
    