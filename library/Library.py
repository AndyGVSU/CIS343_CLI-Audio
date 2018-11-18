from exceptions.CLI_Audio_Exception import CLI_Audio_File_Exception
import os

"""
Library class. Used to get song information from a given directory, and
display information in a curses window, which is done through the FrontEnd.
"""
class Library:

    """
    Constructor for the class. pageLength determines how long each page should be.
    """
    def __init__(self, pageLength):
        self.libraryMap = {}
        self.libraryPage = 0;
        self.pageLength = pageLength

    """
    Returns the current length of the libraryMap.
    """
    def __len__(self):
        return len(self.libraryMap)

    """
    Loops through a given path, and checks for .wav files. If the file is a .wav,
    then add the file to the libraryMap, and increment songCount.
    """
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

    """
    Returns song information given a song number.
    """
    def getFile(self, key):
        return self.libraryMap[key]

    """
    Increments the current library page
    """
    def addPage(self, incPage):
        self.libraryPage = self.libraryPage + incPage

    """
    Returns the total number of library pages.
    """
    def getTotalPages(self):
        return int(len(self.libraryMap) / self.pageLength)

    """
    Returns whether the library map is currently empty or not.
    """
    def isEmpty(self):
        return len(self.libraryMap) == 0

    """
    Returns the current page number used by the library map.
    """
    def getPage(self):
        return self.libraryPage

