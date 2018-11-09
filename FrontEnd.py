import curses
import curses.textpad
from exceptions.CLI_Audio_Exception import CLI_Audio_Screen_Size_Exception
from exceptions.CLI_Audio_Exception import CLI_Audio_File_Exception

import sys
import os

class FrontEnd:

    def __init__(self, player):
        self.libraryMap = {}
        self.libraryPage = 0
        self.player = player
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

        self.libraryPad = curses.newpad(100,100)
        self.libraryPad.border()

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
                self.updateSong()
                #self.stdscr.touchwin()
                #self.stdscr.refresh()
            elif c == ord('l'):
                self.changeLibrary()
                #self.stdscr.touchwin()
                #self.stdscr.refresh()
            elif c == ord('['):
                if self.libraryPage > 0:
                    self.libraryPage = self.libraryPage - 1
                    self.refreshLibraryPad()
                elif not self.getLibraryLoaded():
                    self.drawError("No library loaded!")
            elif c == ord(']'):
                if self.libraryPage < self.getLibraryPages():
                    self.libraryPage = self.libraryPage + 1
                    self.refreshLibraryPad()
                elif not self.getLibraryLoaded():
                    self.drawError("No library loaded!")
    
    def updateSong(self):
        self.stdscr.addstr(15,10, "                                        ")
        self.stdscr.addstr(15,10, "Now playing: " + self.player.getCurrentSong())

    def changeSong(self):
        if len(self.libraryMap) == 0:
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
            return;
        
        try:
            self.player.play(self.libraryMap[songNumber])
        except KeyError:
            self.drawError("Song number out of library range!")
            return;

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
        if not self.player.getPaused():
            self.player.stop()
        #if path not in os.scandir(os.curdir):
        #    raise CLI-Audio_File_Exception("Path does not exist.")
        
        self.libraryMap = {}

        songCount = 0
        with os.scandir(path) as it:
            for entry in it:
                if entry.is_file():
                    filename = os.fsdecode(entry)

                    if filename.endswith(".wav"):
                        self.libraryMap[songCount] = filename
                        songCount = songCount + 1

        self.libraryPad.erase()

        row = 0
        if not self.getLibraryLoaded():
            self.libraryPad.addstr(5, 50, "No files found!")

        for key in self.libraryMap:
            self.libraryPad.addstr(5 + row, 50, str(key) + ": " + self.libraryMap[key])
            row = row + 1
        self.refreshLibraryPad()
    
    def refreshLibraryPad(self):
        self.stdscr.addstr(19,50,"<PAGE " + str(self.libraryPage + 1) + " OF " + str(self.getLibraryPages() + 1) + ">")
        self.stdscr.refresh()
        self.libraryPad.refresh((17 * self.libraryPage), 50, (5 * self.libraryPage), 50, 16, 90)
        #self.libraryPad.refresh((17 * self.libraryPage), 50, (5 * self.libraryPage), 50, 16, 90)

    def getLibraryLoaded(self):
        return len(self.libraryMap) > 0

    def getLibraryPages(self):
        return int(len(self.libraryMap) / 12)

    def drawError(self, message):
        self.stdscr.addstr(3,5,"                                 ")
        self.stdscr.addstr(3,5,message)
    
    def resetError(self):
        self.stdscr.addstr(3,5,"                                 ")
