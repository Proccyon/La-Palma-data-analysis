import numpy as np
from scipy import signal
from astropy.io import fits
from FileReader import MakePath

#-----MainFunctions-----#

#Saves and array as a .fit file
def SaveFitsFile(Image,FileName):
    hdu = fits.PrimaryHDU(Image)
    hdul = fits.HDUList([hdu])
    hdul.writeto(MakePath(FileName,"fit"))
    
#-----MainFunctions-----#
    
