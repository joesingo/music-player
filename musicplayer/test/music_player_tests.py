import unittest
import os

from server.music_player import MusicPlayer, States
from server.song import Song

class MusicPlayerTests(unittest.TestCase):

    LIBRARY = os.path.join(os.path.dirname(__file__), "test-library")

    def get_test_song(self, name):
        """Helper method to return a Song object for the test song with the
        given name"""
        return Song({"artist": "test artist", "album": "test album",
                            "song": name})

    def test_play_and_stop(self):
        """Test playing and stopping a song"""
        m = MusicPlayer(self.LIBRARY)
        song = self.get_test_song("1.mp3")

        # Check that the player starts off stopped
        self.assertEqual(m.state, States.stopped)

        # Play the song and check state is 'playing'
        m.play_song(song)
        self.assertEqual(m.state, States.playing)
        m.stop()
        self.assertEqual(m.state, States.stopped)

    def test_pause(self):
        """Test pausing and unpausing a song"""
        m = MusicPlayer(self.LIBRARY)
        song = self.get_test_song("1.mp3")

        # Check that toggling pause when stopped has no effect
        m.toggle_pause()
        self.assertEqual(m.state, States.stopped)

        # Test pausing
        m.play_song(song)
        m.toggle_pause()
        self.assertEqual(m.state, States.paused)
        m.toggle_pause()
        self.assertEqual(m.state, States.playing)

        # Test stopping whilst paused
        m.toggle_pause()
        m.stop()
        self.assertEqual(m.state, States.stopped)

    def test_add_to_queue(self):
        """Test adding a song through the MusicPlayer"""
        m = MusicPlayer(self.LIBRARY)
        song = self.get_test_song("1.mp3")

        # Add a song to the queue whilst playback is stopped and check that
        # the song is played straight away
        m.add_to_queue([song])
        self.assertEqual(m.state, States.playing)
