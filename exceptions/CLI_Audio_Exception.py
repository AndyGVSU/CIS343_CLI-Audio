"""CLI_Audio_Exception - Parent class for cli-audio custom exceptions"""

class CLI_Audio_Exception(Exception):
    def __init__(self, message):
        self.message = message

class CLI_Audio_File_Exception(CLI_Audio_Exception):
    def __init__(self, message):
        super(CLI_Audio_Exception, self).__init__(message)

class CLI_Audio_Screen_Size_Exception(CLI_Audio_Exception):
    def __init__(self, message):
        super(CLI_Audio_Exception, self).__init__(message)
