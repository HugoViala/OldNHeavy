"""Class to properly encapsulate all the data required to rank a file """


import time
import os
import math
from collections import OrderedDict


class FileInfo:
    "store file metadata"
    maxLen = OrderedDict()
    maxLen["filename"] = 30
    maxLen["fileext"] = 6
    maxLen["size"] = 10
    maxLen["timeModified"] = 4
    def __init__(self, filepath, cwd):
        (self.path, filefullname) = os.path.split(filepath)
        self.path = self.path[len(cwd):]
        (self.filename, self.fileext) = os.path.splitext(filefullname)
        self.timeModified = int(math.ceil((time.time() - os.path.getmtime(filepath))/(60*60*24)))
        self.size = os.path.getsize(filepath)

    def display(self):
        s = ""
        for (att, n) in FileInfo.maxLen.items():
            if len(str(getattr(self, att))) <= n:
                s = s + str(getattr(self, att))+ " " * (n - len(str(getattr(self, att) ) ) )  + "|"
            else:
                s = s + (str(getattr(self, att)))[:n] + "|"
        return s + self.path
        


class Filter:
    "store how to rank a fileInfo"
    def __init__(self, sFunc=(lambda s : s), tFunc=(lambda t : t)):
        self.sizeFunc = sFunc
        self.timeFunc = tFunc

    def filterFile(self, fileinfo):
        return self.sizeFunc(fileinfo.size) * self.timeFunc(fileinfo.timeModified)


def listOfFilesInDir(cwd):
    """look recursively for all the files in the cwd dir"""
    unaccessibleDir = ["Ma musique", "Mes images", "Mes vid\xe9os"]
    def listOfFilesInDirAux(directory, currentL):
        currentL.extend([FileInfo(os.path.join(directory,f),cwd) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory,f))])
        for folder in [os.path.join(directory,f) for f in os.listdir(directory) if os.path.isdir(os.path.join(directory,f)) and f not in unaccessibleDir]:
            currentL = listOfFilesInDirAux(folder, currentL)
        return currentL
    return listOfFilesInDirAux(cwd, [])

linearFilter = Filter()
sizeOnlyFilter = Filter((lambda s : s), (lambda t : 1))
timeOnlyFilter = Filter((lambda s : 1), (lambda t : t))

def sortedFilesByFilter(fileList, filt = linearFilter, nDisplay = 50):
    """sort the files in the fileList according to the filter and displaying only a certain amount"""
    l = fileList
    l.sort(key = lambda f : filt.filterFile(f), reverse=True)
    return l[:nDisplay]

def oldnheavy(directory, filt = linearFilter, nDisplay = 50):
    print "Analyzing data..."
    return "\n".join([f.display() for f in sortedFilesByFilter(listOfFilesInDir(directory),filt, nDisplay)])
    
    
if __name__ == "__main__":
    import sys
    if len(sys.argv) >= 2:
        directory = sys.argv[1]
    else:
        directory = os.getcwd()
    print oldnheavy(directory)
    
#TODO(hugo) : GUI ?
#TODO(hugo) : display size of some dirs (but not all dirs are pertinent because otherwise they would always be on top... on you can decide with a flag...
#TODO(hugo) : maybe do some cleaning : after all a "Filter" is a really a filter, just a function N^2 -> N and we could implement REAL filter (like only show files whose rank is >= CONST)
