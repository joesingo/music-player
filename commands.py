from exceptions import InvalidCommandException


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

# Required fields common to multiple commands
SONG_REQUIRED_FIELDS = ["song", "album", "artist"]


@requires(*SONG_REQUIRED_FIELDS)
def play_command(data, player):
        player.play_song(data["song"], data["album"], data["artist"])
        print("Playing {} by {}".format(data["song"], data["artist"]))


def toggle_pause_command(data, player):
    player.toggle_pause()


def stop_command(data, player):
    player.stop()


COMMANDS = {
    "play": play_command,
    "toggle-pause": toggle_pause_command,
    "stop": stop_command
}
