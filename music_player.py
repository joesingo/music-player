import os
import os.path
import pygame
import pygame.event
import pygame.mixer as mixer
from enum import Enum

from exceptions import SongNotFoundException
from song import Song
from song_queue import SongQueue


class States(Enum):
    """An enum to represent the possible states of a MusicPlayer"""
    stopped = 1
    playing = 2
    paused = 3

class MusicPlayer(object):

    SUPPORTED_FORMATS = ("mp3", "ogg")

    def __init__(self, music_directory):
        """Initialise pygame mixer and set attributes"""

        # Start pygame stuff
        mixer.init()
        self.SONG_FINISHED_EVENT = pygame.USEREVENT + 1
        mixer.music.set_endevent(self.SONG_FINISHED_EVENT)
        pygame.init()

        self.state = States.stopped
        self.music_directory = music_directory

        self.play_queue = SongQueue()


    def main_loop(self):
        """Check for pygame events for when a song ends"""
        for event in pygame.event.get():
            if event.type == self.SONG_FINISHED_EVENT:
                print("Playback finished")
                self.state = States.stopped
                self.next_song()

    def play_song(self, song):
        """Play the specified song"""
        filename = self.get_song_filename(song)
        try:
            mixer.music.load(filename)
        except pygame.error:
            raise SongNotFoundException("File '{}' is not an audio file or does not exist"
                                        .format(filename))

        mixer.music.play()
        self.state = States.playing

        print("Playing {} ".format(song))

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
        print("Stopping playback")

        if self.state != States.stopped:
            mixer.music.stop()
            self.state = States.stopped

    def get_song_filename(self, song):
        """Return the filename for a given song"""
        return os.path.join(self.music_directory, song.artist, song.album, song.name)

    def list_songs(self):
        """A generator to give a list of songs under the music directory"""
        for artist in os.listdir(self.music_directory):
            artist_dir = os.path.join(self.music_directory, artist)

            for album in os.listdir(artist_dir):
                album_dir = os.path.join(artist_dir, album)

                for file in os.listdir(album_dir):
                    for extension in MusicPlayer.SUPPORTED_FORMATS:
                        if file.endswith("." + extension):
                            song = Song({"song": file, "album": album, "artist": artist})
                            yield song

    def next_song(self):
        """Skip to the next song in the queue if there is one, and stop playback otherwise"""
        next_song = self.play_queue.dequeue()
        if next_song:
            self.play_song(next_song)
        else:
            self.stop()