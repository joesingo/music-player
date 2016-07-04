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


class Command(object):

    @classmethod
    def run(cls, data):
        """Check all required fields are present in data"""

        for field in cls.required_fields:
            if field not in data:
                raise InvalidCommandException("Required field '{}' was missing".format(field))


class PlayCommand(Command):

    required_fields = ["song"]

    @classmethod
    def run(cls, data):
        """Play the song"""
        super().run(data)

        print("Playing {}".format(data["song"]))


class NextSongCommand(Command):

    required_fields = []

    @classmethod
    def run(cls, data):
        super().run(data)

        print("Skipping to the next song")


COMMAND_INDEX = {
    "play": PlayCommand,
    "next": NextSongCommand
}