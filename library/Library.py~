from exceptions.CLI_Audio_Exception import CLI_Audio_File_Exception
import os

class Library:
    def __init__(self, pageLength):
        self.libraryMap = {}
        self.libraryPage = 0;
        self.pageLength = pageLength

    def __len__(self):
        return len(self.libraryMap)

    def loadFiles(self, path):
        self.libraryMap = {}
        self.libraryPage = 0
        try:
            songCount = 0
            with os.scandir(path) as it:
                for entry in it:
                    if entry.is_file():
                        filename = os.fsdecode(entry)

                        if filename.endswith(".wav"):
                            self.libraryMap[songCount] = filename
                            songCount = songCount + 1
        except Exception:
            raise CLI_Audio_File_Exception("Path does not exist!")
    
    def getFile(self, key):
        return self.libraryMap[key]

    def addPage(self, incPage):
        self.libraryPage = self.libraryPage + incPage

    def getTotalPages(self):
        return int(len(self.libraryMap) / self.pageLength)

    def isEmpty(self):
        return len(self.libraryMap) == 0

    def getPage(self):
        return self.libraryPage

