class MusicPlayerException(Exception):
    """Base class for other custom exceptions"""

class InvalidJSONException(MusicPlayerException):
    """The provided JSON is invalid"""

class InvalidCommandException(MusicPlayerException):
    """Some required fields are missing"""


class UnknownCommandException(MusicPlayerException):
    """The command is unknown"""


class NoCommandSpecifiedException(MusicPlayerException):
    """No command was specified in the request"""

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

    def __call__(self, func):
        def wrapper(data, player, *args, **kwargs):
            # Check all fields in required_fields are in data
            for field in self.required_fields:
                if field not in data:
                    raise InvalidCommandException("Required field '{}' is missing".format(field))

            # Call the actual function
            func(data, player, *args, **kwargs)

        return wrapper

@requires("song")
def play_command(data, player):
        player.play_song(data["song"])
        print("Playing {}".format(data["song"]))

def toggle_pause_command(data, player):
    player.toggle_pause()

@requires("foo", "bar")
def test_command(data, player):
    print("foo, bar = {}, {}".format(data["foo"], data["bar"]))


COMMANDS = {
    "play": play_command,
    "toggle-pause": toggle_pause_command,
    "test": test_command
}
