import vlc

class MusicPlayer(object):

    def __init__(self):
        self.vlc = vlc.Instance()
        self.vlc_player = self.vlc.media_player_new()

    def play_song(self, filename):
        media = self.vlc.media_new(filename)
        self.vlc_player.set_media(media)
        self.vlc_player.play()

    def toggle_pause(self):
        self.vlc_player.pause()
