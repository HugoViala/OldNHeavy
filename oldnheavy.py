"""Class to properly encapsulate all the data required to rank a file """


from UserDict import UserDict
import time
import os
import math

class FileInfo(UserDict):
    "store file metadata"
    def __init__(self, filepath):
        UserDict.__init(self)
        data["filename"] = os.path.splitext(os.path.split(filepath)[1])[0]
        data["timeModified"] = ceil((time.time() - os.path.getmtime(filepath))/(60*60*24))
        data["timeAccessed"] = ceil((time.time() - os.path.getatime(filepath))/(60*60*24))
        data["size"] = os.path.getsize(filepath)
        
