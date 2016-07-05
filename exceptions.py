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

class SongNotFoundException(MusicPlayerException):
    """The specified song was not found"""