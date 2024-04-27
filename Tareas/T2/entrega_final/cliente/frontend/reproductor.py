from PyQt6.QtCore import QObject, QUrl
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
import parametros as p

class Reproductor(QObject):

    def __init__(self):
        super().__init__()
        self.media_player_mp3 = QMediaPlayer(self)
        self.media_player_mp3.setAudioOutput(QAudioOutput(self))
    

    def reproducir_victoria(self):
        file_url = QUrl.fromLocalFile(p.PATH_VICTORIA)
        self.media_player_mp3.setSource(file_url)
        self.media_player_mp3.play()


    def reproducir_derrota(self):
        file_url = QUrl.fromLocalFile(p.PATH_DERROTA)
        self.media_player_mp3.setSource(file_url)
        self.media_player_mp3.play()
        
         