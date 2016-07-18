import unittest

from server.song_queue import SongQueue

class QueueTests(unittest.TestCase):

    def test_add_songs(self):
        """Test adding songs to the queue"""
        q = SongQueue()

        # Add 5 'songs'
        for i in range(5):
            q.add(i)

        # Check the length is now 5
        self.assertEqual(q.get_length(), 5)

    def test_dequeue(self):
        """Test dequeing"""
        q = SongQueue()
        # Add songs a and b
        q.add("a")
        q.add("b")
        self.assertEqual(q.dequeue(), "a")
        self.assertEqual(q.get_length(), 1)
        self.assertEqual(q.dequeue(), "b")
        self.assertEqual(q.dequeue(), None)

    def test_shuffle(self):
        q = SongQueue()
        songs = list(range(10))
        for i in songs:
            q.add(i)

        # Turn shuffle on and dequeue
        q.toggle_shuffle()
        d = q.dequeue()

        # Turn shuffle off...
        q.toggle_shuffle()
        # ...and check that songs are now back in numeric order (excluding d)
        songs.remove(d)
        for i in songs:
            self.assertEqual(q.dequeue(), i)
