"""Class to properly encapsulate all the data required to rank a file """


import time
import os
import math

class FileInfo:
    "store file metadata"
    def __init__(self, filepath):
        (self.path, filefullname) = os.path.split(filepath)
        (self.filename, self.fileext) = os.path.splitext(filefullname)
        self.timeModified = int(math.ceil((time.time() - os.path.getmtime(filepath))/(60*60*24)))
        self.size = os.path.getsize(filepath)


class Filter:
    "store how to rank a fileInfo"
    def __init__(self, sFunc=(lambda s : s), tFunc=(lambda t : t)):
        self.sizeFunc = sFunc
        self.timeFunc = tFunc

    def filterFile(self, fileinfo):
        return self.sizeFunc(fileinfo.size) * self.timeFunc(fileinfo.timeModified)


def listOfFilesInDir(directory):
    def listOfFilesInDirAux(directory, currentL):
        currentL.extend([FileInfo(os.path.join(directory,f)) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))])
        if len([f for f in os.listdir(directory) if os.path.isdir(os.path.join(directory,f))]) < 1:
            return currentL
        else:
            for folder in [os.path.join(directory,f) for f in os.listdir(directory) if os.path.isdir(os.path.join(directory,f))]:
                currentL = listOfFilesInDirAux(folder, currentL)
            return currentL
    return listOfFilesInDirAux(directory, [])

linearFilter = Filter()
sizeOnlyFilter = Filter((lambda s : s), (lambda t : 1))
timeOnlyFilter = Filter((lambda s : 1), (lambda t : t))

def sortedFilesByFilter(fileList, filt = linearFilter):
    fileList.sort(key = lambda f : filt.filterFile(f), reverse=True)
    return fileList
        
    
    
if __name__ == "__main__":
    print "\n".join([f.filename for f in sortedFilesByFilter(listOfFilesInDir("c:\\users\\hugo\\documents\\github\\mybreak"),timeOnlyFilter)])
