import pygame.mixer as mixer

class MusicPlayer(object):

    def __init__(self):
        """Initialise pygame mixer and set attributes"""
        mixer.init()
        self.playing = False

    def play_song(self, filename):
        """Play the specified song"""
        song = mixer.music.load(filename)
        mixer.music.play()
        self.playing = True

    def toggle_pause(self):
        """Pause if currently playing, and unpause if currently paused"""
        if self.playing:
            mixer.music.pause()
            self.playing = False
        else:
            mixer.music.unpause()
            self.playing = True
