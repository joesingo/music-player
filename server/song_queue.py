class SongQueue(object):
    """Class to represent a queue of songs to be played"""

    def __init__(self, songs=[]):
        self.songs = songs

    def add(self, song):
        """Add a song to the back of the queue"""
        print("Adding {} to queue".format(song))
        self.songs.append(song)

    def dequeue(self):
        """Return the song at the front of the queue, or None is queue is empty"""
        if len(self.songs) > 0:
            s = self.songs[0]
            self.songs.remove(s)
            return s
        else:
            return None

    def get_length(self):
        """Get the number of songs currently in the queue"""
        return len(self.songs)

    def __str__(self):
        """String representation of the queue"""
        return ", ".join(self.songs)