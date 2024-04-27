from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QPixmap
import parametros as p
import os

class SpriteConejo(QLabel):

    def __init__(self, pos: tuple):
        super().__init__()
        self.pos = pos
        self.dir = "s"
        self.intercalado = 0
        ruta = os.path.join("assets", "sprites", p.SPRITES_CONEJO["s"][self.intercalado % 3])
        self.setPixmap(QPixmap(ruta))
        self.setScaledContents(True)
        self.setFixedSize(p.DIM_CASILLA, p.DIM_CASILLA)

    def redireccionar(self, dir: str):
        '''
        Coloca el nuevo sprite; no necesariamente sólo redirecciona.
        '''
        self.dir = dir
        ruta = os.path.join("assets", "sprites", p.SPRITES_CONEJO[dir][self.intercalado % 3])
        self.setPixmap(QPixmap(ruta))
    

class SpriteLoboH(QLabel):
    def __init__(self, pos: tuple):
        super().__init__()
        self.pos = pos
        self.dir = "d"
        self.intercalado = 0
        ruta = os.path.join("assets", "sprites", p.SPRITES_LOBOS["d"][self.intercalado % 3])
        self.setPixmap(QPixmap(ruta))
        self.setScaledContents(True)
        self.setFixedSize(p.DIM_CASILLA, p.DIM_CASILLA)
    
    def redireccionar(self, dir: str):
        '''
        Coloca el nuevo sprite; no necesariamente sólo redirecciona.
        '''
        self.dir = dir
        ruta = os.path.join("assets", "sprites", p.SPRITES_LOBOS[dir][self.intercalado % 3])
        self.setPixmap(QPixmap(ruta))

class SpriteLoboV(QLabel):
    def __init__(self, pos: tuple):
        super().__init__()
        self.pos = pos
        self.dir = "w"
        self.intercalado = 0
        ruta = os.path.join("assets", "sprites", p.SPRITES_LOBOS["w"][self.intercalado % 3])
        self.setPixmap(QPixmap(ruta))
        self.setScaledContents(True)
        self.setFixedSize(p.DIM_CASILLA, p.DIM_CASILLA)
    
    def redireccionar(self, dir: str):
        '''
        Coloca el nuevo sprite; no necesariamente sólo redirecciona.
        '''
        self.dir = dir
        ruta = os.path.join("assets", "sprites", p.SPRITES_LOBOS[dir][self.intercalado % 3])
        self.setPixmap(QPixmap(ruta))

class SpriteCanon(QLabel):
    def __init__(self, pos: tuple, direccion: str):
        super().__init__()
        self.pos = pos
        ruta = os.path.join("assets", "sprites", p.SPRITES_CANON[p.INGLES_A_TECLA[direccion]])
        self.setPixmap(QPixmap(ruta))
        self.setScaledContents(True)
        self.setFixedSize(p.DIM_CASILLA, p.DIM_CASILLA)

class SpriteAppleNormal(QLabel):
    def __init__(self, pos: tuple):
        super().__init__()
        self.pos = pos
        ruta = os.path.join("assets", "sprites", "manzana.png")
        self.setPixmap(QPixmap(ruta))
        self.setScaledContents(True)
        self.setFixedSize(p.DIM_CASILLA, p.DIM_CASILLA)

class SpriteAppleHielo(QLabel):
    def __init__(self, pos: tuple):
        super().__init__()
        self.pos = pos
        ruta = os.path.join("assets", "sprites", "manzana_burbuja.png")
        self.setPixmap(QPixmap(ruta))
        self.setScaledContents(True)
        self.setFixedSize(p.DIM_CASILLA,p.DIM_CASILLA)

class SpriteZanahoria(QLabel):
    def __init__(self, pos: tuple, direccion: str):
        super().__init__()
        self.pos = pos
        ruta = os.path.join("assets", "sprites", p.SPRITES_ZANAH[direccion])
        self.setPixmap(QPixmap(ruta))
        self.setScaledContents(True)
        self.setFixedSize(p.DIM_CASILLA, p.DIM_CASILLA)
    
