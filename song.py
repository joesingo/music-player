class Song(object):
    """Class to represent a song"""

    REQUIRED_FIELDS = ["artist", "album", "song"]

    def __init__(self, data):
        """Create a Song instance from the data in 'data' dictionary"""
        self.artist = data["artist"]
        self.album = data["album"]
        self.name = data["song"]

    def __str__(self):
        return "{} by {}".format(self.name, self.artist)