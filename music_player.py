import pygame
import pygame.mixer as mixer
from enum import Enum

from exceptions import SongNotFoundException


class States(Enum):
    """An enum to represent the possible states of a MusicPlayer"""
    stopped = 1
    playing = 2
    paused = 3

class MusicPlayer(object):

    def __init__(self):
        """Initialise pygame mixer and set attributes"""
        mixer.init()
        self.state = States.stopped

    def play_song(self, filename):
        """Play the specified song"""
        try:
            song = mixer.music.load(filename)
        except pygame.error:
            raise SongNotFoundException("File '{}' is not an audio file or does not exist"
                                        .format(filename))

        mixer.music.play()
        self.state = States.playing

    def toggle_pause(self):
        """Pause if currently playing, and unpause if currently paused"""
        if self.state == States.playing:
            mixer.music.pause()
            self.state = States.paused

        elif self.state == States.paused:
            mixer.music.unpause()
            self.state = States.playing

    def stop(self):
        """Stop playback"""
        if self.state != States.stopped:
            mixer.music.stop()
            self.state = States.stopped

