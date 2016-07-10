import os
import os.path
import pygame
import pygame.event
import pygame.mixer as mixer
from enum import Enum

from server.exceptions import SongNotFoundException
from server.song import Song
from server.song_queue import SongQueue


class States(Enum):
    """An enum to represent the possible states of a MusicPlayer"""
    stopped = "Stopped"
    playing = "Playing"
    paused = "Paused"

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
        self.current_song = None
        self.music_directory = music_directory

        self.play_queue = SongQueue()


    def main_loop(self):
        """Check for pygame events for when a song ends"""
        for event in pygame.event.get():
            if event.type == self.SONG_FINISHED_EVENT:
                print("Playback finished")
                self.stop()
                self.next_song()

    def play_song(self, song):
        """Play the specified song"""
        self.stop()

        filename = self.get_song_filename(song)
        try:
            mixer.music.load(filename)
        except pygame.error:
            raise SongNotFoundException("File '{}' is not an audio file or does not exist"
                                        .format(filename))

        mixer.music.play()
        self.state = States.playing
        self.current_song = song

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
        if self.state != States.stopped:
            print("Stopping playback")
            mixer.music.stop()
            self.state = States.stopped
            self.current_song = None

    def get_song_filename(self, song):
        """Return the filename for a given song"""
        return os.path.join(self.music_directory, song.artist, song.album, song.name)

    def list_songs(self):
        """A generator to give a list of songs under the music directory"""
        library = {}
        for artist in os.listdir(self.music_directory):
            artist_dir = os.path.join(self.music_directory, artist)
            library[artist] = {}

            for album in os.listdir(artist_dir):
                album_dir = os.path.join(artist_dir, album)
                library[artist][album] = []

                for file in os.listdir(album_dir):
                    for extension in MusicPlayer.SUPPORTED_FORMATS:
                        if file.endswith("." + extension):
                            library[artist][album].append(file)

        return library

    def next_song(self):
        """Skip to the next song in the queue if there is one, and stop playback otherwise"""
        self.stop()

        next_song = self.play_queue.dequeue()
        if next_song:
            self.play_song(next_song)

    def add_to_queue(self, song):
        """Add the provided song to the play queue"""
        self.play_queue.add(song)

        # If no song is playing and we have just added something to the front of the queue, then
        # play it now
        if self.state == States.stopped and self.play_queue.get_length() == 1:
            self.next_song()

    def get_info(self):
        """Return the current state, and if a song is playing return its info and elapsed time"""
        info = {
            "state": self.state.value
        }

        # If a song is playing (or has been paused), add info about it
        if self.current_song is not None:
            info["song"] = self.current_song.to_dict()
            info["time"] = MusicPlayer.minutes_and_seconds(mixer.music.get_pos())

        return info

    @staticmethod
    def minutes_and_seconds(time_in_ms):
        """Convert an amount of time in milliseconds to minutes and seconds, rounded to the nearest
        second, e.g. 83211 -> 1:23"""
        total_seconds = round(time_in_ms / 1000)
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        return "{}:{:0>2}".format(minutes, seconds)
