import curses
import curses.textpad
from exceptions.CLI_Audio_Exception import CLI_Audio_Screen_Size_Exception
from exceptions.CLI_Audio_Exception import CLI_Audio_File_Exception
from library.Library import Library

import sys
import os

class FrontEnd:

    def __init__(self, player):
        self.player = player
        self.pageLength = 12
        self.library = Library(self.pageLength)
        #self.player.play(sys.argv[1])
        curses.wrapper(self.menu)
       
    def menu(self, args):
        self.stdscr = curses.initscr()
        
        screenSize = self.stdscr.getmaxyx()
        minY = 15
        minX = 90
        
        message = ""
        if (screenSize[0] < minY or screenSize[1] < minX):
            if (screenSize[0] < minY):
                message = message + "\nScreen size of " + str(screenSize[0]) + " isn't tall enough; must be at least " + str(minY)
            if (screenSize[1] < minX):
                message = message + "\nScreen size of " + str(screenSize[1]) + " isn't wide enough; must be at least " + str(minX)
            raise CLI_Audio_Screen_Size_Exception(message)
  
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
            c = self.stdscr.getch()

            if c == 27:
                self.quit()
            elif c == ord('p'):
                self.player.pause()
                if self.player.getCurrentSong() == self.player.getStartSong():
                    self.drawError("No song selected!")

            elif c == ord('c'):
                self.changeSong()
                #self.stdscr.touchwin()
                #self.stdscr.refresh()
            elif c == ord('l'):
                self.changeLibrary()
                #self.stdscr.touchwin()
                #self.stdscr.refresh()
            elif c == ord('['):
                if self.library.getPage() > 0:
                    self.library.addPage(-1)
                    self.refreshLibraryPad()
                elif self.library.isEmpty():
                    self.drawError("No library loaded!")
            elif c == ord(']'):
                if self.library.getPage() < self.library.getTotalPages():
                    self.library.addPage(1)
                    self.refreshLibraryPad()
                elif self.library.isEmpty():
                    self.drawError("No library loaded!")
    
    def updateSong(self):
        self.stdscr.addstr(16,10, "                                        ")
        self.stdscr.addstr(15,10, "Now playing: ")
        self.stdscr.addstr(16,10, self.player.getCurrentSong())

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

        try:
            songNumber = int(songNumber.decode(encoding="utf-8"))
        except ValueError:
            self.drawError("Song number invalid!")
            return
        
        try:
            self.player.play(self.library.getFile(songNumber))
        except KeyError:
            self.drawError("Song number out of library range!")
            return
        except CLI_Audio_File_Exception:
            self.drawError("Song file invalid!")
            return

        self.updateSong()

    def quit(self):
        self.player.stop()
        exit()

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

        #if not self.player.getPaused():
        #    self.player.pause()

        try:
            self.library.loadFiles(path)
        except CLI_Audio_File_Exception:
            self.drawError("Path does not exist!")

        self.refreshLibraryPad()
    
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
                    self.libraryPad.addstr(1 + y, 1, str(key) + ": " + self.library.getFile(key))

        self.libraryPad.refresh()

    def drawError(self, message):
        self.stdscr.addstr(3,5,"                                 ")
        self.stdscr.addstr(3,5,message)
    
    def resetError(self):
        self.stdscr.addstr(3,5,"                                 ")
