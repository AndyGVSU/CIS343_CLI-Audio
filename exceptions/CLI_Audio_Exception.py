"""
CLI_Audio_Exception - Parent class for cli-audio custom exceptions.
Extends the Exception class.
"""

class CLI_Audio_Exception(Exception):
    def __init__(self, message):
        self.message = message

"""
This is intended to be thrown when an audio file can't be opened
for some reason.
"""
class CLI_Audio_File_Exception(CLI_Audio_Exception):
    def __init__(self, message):
        super(CLI_Audio_Exception, self).__init__(message)

"""
This is intended to be thrown when the size of the screen is too small.
"""
class CLI_Audio_Screen_Size_Exception(CLI_Audio_Exception):
    def __init__(self, message):
        super(CLI_Audio_Exception, self).__init__(message)
