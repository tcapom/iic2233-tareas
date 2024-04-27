from PyQt6.QtCore import QObject, pyqtSignal, QTimer
import parametros as p


class LogicaConejo(QObject):
    def __init__(self, pos: tuple[int, int], id: int):
        super().__init__()
        self.tipo = "C"
        self.pos = pos
        self.id = id
        self.dir = "s"


class LogicaLoboH(QObject):
    senal_try_mover_lobo = pyqtSignal(object)
    senal_intercalar_lobo = pyqtSignal(object)
    def __init__(self, pos: tuple[int, int], id: int, nivel: int):
        super().__init__()
        self.tipo = "LH"
        self.pos = pos
        self.id = id
        self.dir = "d"
        self.timer = QTimer() #Timer para moverse entre casillas
        intervalo = int(1000 * p.POND_ACUMULADOS[nivel - 1] // p.VELOCIDAD_LOBO)
        self.timer.setInterval(intervalo)
        self.timer.start()
        self.timer.timeout.connect(self.probar_moverse)
        self.timer_chico = QTimer() #Timer para intercalar sprites
        self.timer_chico.setInterval(int(intervalo // p.INTERCALADO_LOBO))
        self.timer_chico.start()
        self.timer_chico.timeout.connect(self.intercalar)
    
    def probar_moverse(self):
        self.senal_try_mover_lobo.emit(self)

    def intercalar(self):
        self.senal_intercalar_lobo.emit(self)

    def pausar(self):
        self.timer.stop()
        self.timer_chico.stop()
    
    def reanudar(self):
        self.timer.start()
        self.timer_chico.start()


class LogicaLoboV(QObject):
    senal_try_mover_lobo = pyqtSignal(object)
    senal_intercalar_lobo = pyqtSignal(object)
    def __init__(self, pos: tuple[int, int], id: int, nivel: int):
        super().__init__()
        self.tipo = "LV"
        self.pos = pos
        self.id = id
        self.dir = "w"
        self.timer = QTimer() #Timer para moverse entre casillas
        intervalo = int(1000 * p.POND_ACUMULADOS[nivel - 1] // p.VELOCIDAD_LOBO)
        self.timer.setInterval(intervalo)
        self.timer.start()
        self.timer.timeout.connect(self.probar_moverse)
        self.timer_chico = QTimer() #Timer para intercalar sprites
        self.timer_chico.setInterval(int(intervalo // p.INTERCALADO_LOBO))
        self.timer_chico.start()
        self.timer_chico.timeout.connect(self.intercalar)

    def probar_moverse(self):
        self.senal_try_mover_lobo.emit(self)
    
    def intercalar(self):
        self.senal_intercalar_lobo.emit(self)

    def pausar(self):
        self.timer.stop()
        self.timer_chico.stop()
    
    def reanudar(self):
        self.timer.start()
        self.timer_chico.start()


class LogicaCanon(QObject):
    senal_spawnear_zanahoria = pyqtSignal(object)
    def __init__(self, pos: tuple[int, int], id: int, direccion: str):
        super().__init__()
        self.tipo = "C" + direccion
        self.pos = pos
        self.id = id
        self.dir = p.INGLES_A_TECLA[direccion]
        self.timer = QTimer()
        self.timer.setInterval(int(1000 // p.FRECUENCIA_CANON))
        self.timer.start()
        self.timer.timeout.connect(self.probar_disparar)
    
    def probar_disparar(self):
        self.senal_spawnear_zanahoria.emit(self)
    
    def pausar(self):
        self.timer.stop()
    
    def reanudar(self):
        self.timer.start()


class LogicaAppleNormal(QObject):
    '''
    No se implementó. Permanece como placeholder
    '''
    def __init__(self, pos: tuple[int, int], id: int):
        super().__init__()
        self.tipo = "BM"
        self.pos = pos
        self.id = id


class LogicaAppleHielo(QObject):
    '''
    No se implementó. Permanece como placeholder
    '''
    def __init__(self, pos: tuple[int, int], id: int):
        super().__init__()
        self.tipo = "BC"
        self.pos = pos
        self.id = id


class LogicaZanahoria(QObject):
    senal_try_mover_zanahoria = pyqtSignal(object)
    def __init__(self, pos: tuple[int, int], id: int, direccion: str):
        super().__init__()
        self.tipo = "Z"
        self.pos = pos
        self.id = id
        self.dir = direccion
        self.timer = QTimer()
        self.timer.setInterval(1000 // p.VELOCIDAD_ZANAHORIA)
        self.timer.start()
        self.timer.timeout.connect(self.probar_moverse)

    def probar_moverse(self):
        self.senal_try_mover_zanahoria.emit(self)
    
    def pausar(self):
        self.timer.stop()
    
    def reanudar(self):
        self.timer.start()