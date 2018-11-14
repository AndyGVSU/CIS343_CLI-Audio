"""PyAudio Example: Play a wave file (callback version)."""

import pyaudio
import wave
import time
from exceptions.CLI_Audio_Exception import CLI_Audio_File_Exception

class Player:
    def __init__(self):
        self.startSong = "Nothing playing."
        self.currentSong = self.startSong
        self.stream = None
        self.paused = True
        self.position = 0

    """Returns the first song played (nothing)."""
    def getStartSong(self):
        return self.startSong

    """Gets the filename of the song currently playing."""
    def getCurrentSong(self):
        return self.currentSong

    """Returns whether the player is paused or not."""
    def getPaused(self):
        return self.paused

    """Pauses the current song (as long as it is not the first song)."""
    def pause(self):
        if (self.currentSong != self.startSong):
            if self.paused == False:
                self.paused = True
                self.stream.stop_stream()
            else:
                self.paused = False
                self.stream.start_stream()

    """Plays the song track (given the filename is valid)."""
    def play(self, track):
        self.paused = False
        self.currentSong = track

        try:
            self.wf = wave.open(track, 'rb')
        except Exception:
            raise CLI_Audio_File_Exception("Error opening wave file.")

        # instantiate PyAudio (1)
        self.p = pyaudio.PyAudio()

        # open self.stream using callback (3)
        self.stream = self.p.open(format=self.p.get_format_from_width(self.wf.getsampwidth()),
                channels=self.wf.getnchannels(),
                rate=self.wf.getframerate(),
                output=True,
                stream_callback=self.callback)

        # start the self.stream (4)
        self.stream.start_stream()

    """Ends the player permanently (if a stream exists)."""
    def stop(self):
        if self.stream != None:
            self.stream.stop_stream()
            self.stream.close()
            self.wf.close()
            self.p.terminate() 

    """Allows the stream to be opened."""
    def callback(self, in_data, frame_count, time_info, status):
        data = self.wf.readframes(frame_count)
        return (data, pyaudio.paContinue)

