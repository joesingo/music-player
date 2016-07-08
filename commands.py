from exceptions import InvalidCommandException
from song import Song


class requires(object):
    """
    A decorator to check that the data provided to a command contains all the fields it requires,
    e.g:
        @requires("foo", "bar")
        def my_command(data, player):
            # Do stuff with data["foo"] and data["bar"]
    If any of the required fields are missing then an InvalidCommandException is raised
    """
    def __init__(self, *required_fields):
        self.required_fields = required_fields

    def check_fields(self, data):
        """Check that the dictionary data contains each field in self.required_fields"""
        for field in self.required_fields:
            if field not in data:
                raise InvalidCommandException("Required field '{}' is missing".format(field))

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            # We are assuming the data is passed as the first argument
            self.check_fields(args[0])
            # Call the actual function
            func(*args, **kwargs)

        return wrapper


@requires(*Song.REQUIRED_FIELDS)
def play_command(data, player):
        song = Song(data)
        player.play_song(song)


def toggle_pause_command(data, player):
    player.toggle_pause()


def stop_command(data, player):
    player.stop()


def list_command(data, player):
    """Return a list containing a dictionary for each song in the library, with fields for song
    name, album and artist"""
    songs = []
    for song in player.list_songs():
        songs.append(song.to_dict())
    return songs

@requires("songs")
def add_to_queue_command(data, player):
    """Add a song to the play queue"""
    if type(data["songs"]) != list:
        raise InvalidCommandException("No songs specified")

    for s in data["songs"]:
        # Check that each item in data["songs"] actual describes a song
        checker = requires(*Song.REQUIRED_FIELDS)
        checker.check_fields(s)

        player.add_to_queue(Song(s))


def next_song_command(data, player):
    """Skip to the next song in the queue"""
    player.next_song()


COMMANDS = {
    "play": play_command,
    "toggle-pause": toggle_pause_command,
    "stop": stop_command,
    "list": list_command,
    "add-to-queue": add_to_queue_command,
    "next": next_song_command
}
