import curses
import curses.textpad
from exceptions.CLI_Audio_Exception import CLI_Audio_Screen_Size_Exception
from exceptions.CLI_Audio_Exception import CLI_Audio_File_Exception
from library.Library import Library

import sys
import os

"""
This is the GUI of the application - here, the client can play audio and
use the provided functionality, which is done through curses.
"""
class FrontEnd:
    """
    Constructor of the class. Takes in self and the player.
    """
    def __init__(self, player):
        """Player to communicate with from this class"""
        self.player = player
        """Page length for the library to display per page."""
        self.pageLength = 12
        """Library to pull songs from."""
        self.library = Library(self.pageLength)
        """Wrapper for the curses menu."""
        curses.wrapper(self.menu)
     
    """
    Initializes the menu for the GUI. Additionally, provides functionality
    for the commands that the user can apply.
    """
    def menu(self, args):
        self.stdscr = curses.initscr()
        
        """Max window size. If screen is less than this, then CLI_Audio_Screen_Size_Exception is thrown."""
        screenSize = self.stdscr.getmaxyx()
        minY = 20
        minX = 102
        
        message = ""
        if (screenSize[0] < minY or screenSize[1] < minX):
            if (screenSize[0] < minY):
                message = message + "\nScreen size of " + str(screenSize[0]) + " isn't tall enough; must be at least " + str(minY)
            if (screenSize[1] < minX):
                message = message + "\nScreen size of " + str(screenSize[1]) + " isn't wide enough; must be at least " + str(minX)
            raise CLI_Audio_Screen_Size_Exception(message)
  
        """Initialize the curses window"""
        self.stdscr.border()
        self.stdscr.addstr(0,0, "cli-audio",curses.A_REVERSE)
        self.stdscr.addstr(5,10, "c - Change Current Song")
        self.stdscr.addstr(6,10, "p - Play/Pause")
        self.stdscr.addstr(7,10, "l - Library")
        self.stdscr.addstr(8,10, "[ - Next Library Page")
        self.stdscr.addstr(9,10, "] - Previous Library Page")
        self.stdscr.addstr(10,10, "ESC - Quit")
        self.updateSong()
        self.stdscr.refresh()

        self.libraryPad = curses.newwin(14,50,5,50)
        self.libraryPad.mvwin(5,50)
        self.libraryPad.border()
        self.libraryPad.refresh()

        wait = 0
        while True:
            #Wait for user input.
            c = self.stdscr.getch()
            
            #escape = quit
            if c == 27:
                self.quit()
            elif c == ord('p'):
                self.player.pause()
                if self.player.getCurrentSong() == self.player.getStartSong():
                    self.drawError("No song selected!")

            #change song
            elif c == ord('c'):
                self.changeSong()

            #change library
            elif c == ord('l'):
                self.changeLibrary()

            #go back one page in library
            elif c == ord('['):
                if self.library.getPage() > 0:
                    self.library.addPage(-1)
                    self.refreshLibraryPad()
                elif self.library.isEmpty():
                    self.drawError("No library loaded!")

            #go forward a page in the library
            elif c == ord(']'):
                if self.library.getPage() < self.library.getTotalPages():
                    self.library.addPage(1)
                    self.refreshLibraryPad()
                elif self.library.isEmpty():
                    self.drawError("No library loaded!")
    
    """
    Update song function. Called when new song is loaded in. Displays song information.
    """
    def updateSong(self):
        self.stdscr.addstr(16,10, "                                        ")
        self.stdscr.addstr(15,10, "Now playing: ")
        self.stdscr.addstr(16,10, self.player.getCurrentSong())

    """
    Changes the current song playing. Creates a window where the user
    can select a song from the loaded library.
    """
    def changeSong(self):
        if self.library.isEmpty():
            self.drawError("No library loaded!")
            return

        self.resetError()
        changeWindow = curses.newwin(3, 30, 1, 50)
        changeWindow.border()
        changeWindow.addstr(0,0, "Select a song number:", curses.A_REVERSE)
        self.stdscr.refresh()
        curses.echo()
        songNumber = changeWindow.getstr(1,1, 30)
        curses.noecho()
        del changeWindow
        self.stdscr.touchwin()
        self.stdscr.refresh()

        if not self.player.getPaused():
            self.player.stop()

        self.refreshLibraryPad()
        
        #Attempt to change the song with the given song number.
        try:
            songNumber = int(songNumber.decode(encoding="utf-8"))
        except ValueError:
            self.drawError("Song number invalid!")
            return
        
        #Send the update to the player.
        try:
            self.player.play(self.library.getFile(songNumber))
        except KeyError:
            self.drawError("Song number out of library range!")
            return
        except CLI_Audio_File_Exception:
            self.drawError("Song file invalid!")
            return

        self.updateSong()

    """
    Quits the player. Sends the quit command to the player as well.
    """
    def quit(self):
        self.player.stop()
        exit()

    """
    Changes the library. Opens a window for the user to input a directory path.
    """
    def changeLibrary(self):
        self.resetError()

        changeWindow = curses.newwin(5, 40, 5, 50)
        changeWindow.border()
        changeWindow.addstr(0,0, "What is the file path?", curses.A_REVERSE)
        self.stdscr.refresh()
        curses.echo()
        path = changeWindow.getstr(1,1, 30)
        curses.noecho()
        del changeWindow
        self.stdscr.touchwin()
        self.stdscr.refresh()

        try:
            self.library.loadFiles(path)
        except CLI_Audio_File_Exception:
            self.drawError("Path does not exist!")

        self.refreshLibraryPad()
    
    """
    Changes the page of the library. Used for both [ and ] input. Gets
    the next <pagelength> number of songs to display.
    """
    def refreshLibraryPad(self):
        self.stdscr.addstr(19,50,"<PAGE " + str(self.library.getPage() + 1) + " OF " + str(self.library.getTotalPages() + 1) + ">")
        self.libraryPad.erase()
        self.libraryPad.border()

        if self.library.isEmpty():
            self.libraryPad.addstr(1, 1, "No files found!")
        else:
            for y in range(0,self.pageLength):
                key = y + (self.pageLength * self.library.getPage())
                if key < len(self.library):
                    media = self.library.getFile(key)
                    if len(media) >= 45:
                        media = media[0:45]
                    self.libraryPad.addstr(1 + y, 1, str(key) + ": " + media)

        self.libraryPad.refresh()

    """
    Displays an error message in the curses window.
    """
    def drawError(self, message):
        self.stdscr.addstr(3,5,"                                 ")
        self.stdscr.addstr(3,5,message)
    
    """
    Resets the error window.
    """
    def resetError(self):
        self.stdscr.addstr(3,5,"                                 ")
