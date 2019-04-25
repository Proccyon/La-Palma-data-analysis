from astropy.utils.data import get_pkg_data_filename
import sys,os
from astropy.io import fits

#-----SideFunctions-----#

#Makes a path to a file in the same folder as the script
def MakePath(FileName,FileType):
    return os.path.dirname(sys.argv[0])+r'/ '[0] +str(FileName)+"."+FileType

#Makes a path to a folder in the same folder as the script
#If target folder is inside another folder(or multiple) make FolderNames a list with folder names
def MakeFolderPath(FolderNames):
    
    Path = os.path.dirname(sys.argv[0])+r'/ '[0]
    
    if(type(FolderNames) is list):
        for FolderName in FolderNames:
            Path += FolderName+r'/ '[0]
    if(type(FolderNames) is str): 
        Path += FolderNames + r'/ '[0]
        
    return Path
    
#Finds the paths to all the files in a specific folder
def FindImagePaths(FolderName,Filetype):
    FolderPath = MakeFolderPath(FolderName)
    PathList = os.listdir(FolderPath)
    NewPathList = []
    for Path in PathList:
        if(Path[-len(Filetype):]==Filetype):
            NewPathList.append(FolderPath + Path)
    return NewPathList

#--/--SideFunctions--/--#


#-----MainFunctions-----#

#Returns a list of all .fit images in a specific folder
#FolderName should be the name of the folder, not the complete path, see MakeFolderPath function
def FindImages(FolderName,Filetype="fit",CcdNumber=4):
    PathList = FindImagePaths(FolderName,Filetype)
    ImageList = []
    for Path in PathList:
        File = fits.open(Path,ignore_missing_end=True)
        ImageList.append(File[CcdNumber].data)
    return ImageList


#-----MainFunctions-----#

#-----Example-----#
#ImageList = FindImages(["Data","M82"])

#The path here is C:\Users\Eigenaar\Desktop\La Palma\Data\M82
#In this case the code is inside the folder 'La Palma' and .fit files are inside 'M82'
