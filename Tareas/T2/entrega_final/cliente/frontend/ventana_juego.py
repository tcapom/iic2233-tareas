import sys
import parametros as p
from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QGridLayout
from PyQt6.QtGui import QPixmap, QKeyEvent
from PyQt6.QtCore import pyqtSignal
from frontend.sprites_entes import (SpriteConejo, SpriteLoboH, SpriteLoboV, 
                                    SpriteCanon, SpriteAppleNormal, SpriteAppleHielo,
                                    SpriteZanahoria)

class VentanaJuego(QWidget):
    '''
    Ventana de juego del programa
    '''
    senal_tecla_wasd = pyqtSignal(str) 
    senal_print_mapa = pyqtSignal()
    senal_pausar = pyqtSignal()
    senal_kil = pyqtSignal()
    senal_inf = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_gui()
    

    def init_gui(self):
        '''
        Crea los elementos que no necesitan información del jugador
        '''
        self.setGeometry(0, 0, p.JUEGO_ANCHO, p.JUEGO_ALTO)
        self.setFixedSize(p.JUEGO_ANCHO,p.JUEGO_ALTO)
        self.setWindowTitle("JUGANDO AHORA A DCCONEJO")
        self.grilla = QGridLayout()
        self.setLayout(self.grilla)
        for i in range(16):
            for j in range(8,24):
                nuevo_label = QLabel(str(i) + "," + str(j), self)
                nuevo_label.setFixedSize(p.DIM_CASILLA,p.DIM_CASILLA)
                self.grilla.addWidget(nuevo_label, i, j)
        logo = QLabel(self)
        logo.setPixmap(QPixmap(p.PATH_LOGO))
        logo.setScaledContents(True)
        self.grilla.addWidget(logo, 0, 0, 2, 8)
        label_static_vidas = QLabel("Vidas restantes:", self)
        self.grilla.addWidget(label_static_vidas, 2, 1, 1, 3)
        label_static_tiempo = QLabel("Tiempo restante:", self)
        self.grilla.addWidget(label_static_tiempo, 3, 1, 1, 3)
        label_static_score = QLabel("Puntaje acumulado:", self)
        self.grilla.addWidget(label_static_score, 4, 1, 1, 3)
        boton_salir = QPushButton('Salir', self)
        boton_salir.clicked.connect(self.click_salir)
        self.grilla.addWidget(boton_salir, 5, 0, 1, 4)
        boton_pausar = QPushButton('Pausar', self)
        boton_pausar.clicked.connect(self.pausar)
        self.grilla.addWidget(boton_pausar, 5, 4, 1, 4)
        self.current_sequence = ["placeholder","placeholder","placeholder"]
        self.label_dinamic_score = QLabel("placeholder", self)
        self.label_dinamic_tiempo = QLabel("placeholder", self)


    def ingresar_nivel(self,entrada):
        '''
        Crea los elementos que necesitan información del jugador.
        Ciertos labels ya fueron creados antes y sólo se actualiza su info.
        '''
        entrada = entrada.split(",")
        self.nivel = entrada[1]
        self.show()
        self.tiempo_restante = int(120 * p.POND_ACUMULADOS[int(self.nivel) - 1])
        self.label_dinamic_tiempo.setText(str(self.tiempo_restante))
        self.grilla.addWidget(self.label_dinamic_tiempo, 3, 5, 1, 1)
        self.label_dinamic_vidas = QLabel(entrada[3], self)
        self.grilla.addWidget(self.label_dinamic_vidas, 2, 5, 1, 1)
        if entrada[1] == "1":
            self.label_dinamic_score.setText("0")
        else:
            self.label_dinamic_score.setText(entrada[2])
        self.grilla.addWidget(self.label_dinamic_score, 4, 5, 1, 1)
    

    def pasar_seg(self, nueva_hora):
        self.label_dinamic_tiempo.setText(nueva_hora)
    

    def actualizar_vidas(self,vidas):
        self.label_dinamic_vidas.setText(vidas)
    

    def actualizar_score(self, score):
        self.label_dinamic_score.setText(score)


    def background_tablero(self, tablero: list[list[str]]):
        '''
        Genera los bloques de fondo y guarda el tablero como variable.
        También crea la lista de elementos del mapa inicialmente vacía.
        '''
        self.matriz_tablero = tablero
        self.lista_entes = []
        for i in range(16):
            for j in range(16):
                bloque_add = QLabel(self)
                if self.matriz_tablero[i][j] == "P":
                    bloque_add.setPixmap(QPixmap(p.PATH_B_PARED))
                else:                    
                    bloque_add.setPixmap(QPixmap(p.PATH_B_FONDO))
                bloque_add.setScaledContents(True)
                bloque_add.setFixedSize(p.DIM_CASILLA,p.DIM_CASILLA)
                cambiandose = self.grilla.itemAtPosition(i, j + 8).widget()
                self.grilla.removeWidget(cambiandose)
                self.grilla.addWidget(bloque_add, i, j + 8)


    def anadir_entes_al_cargar(self, tipo: str, pos: tuple, id: int):
        '''
        Crea sprites conectados a los entes con la misma id en el backend.
        '''
        if tipo == "C":
            self.id_conejo = len(self.lista_entes)
            self.lista_entes.append(SpriteConejo(pos))
        elif tipo == "LH":
            self.lista_entes.append(SpriteLoboH(pos))
        elif tipo == "LV":
            self.lista_entes.append(SpriteLoboV(pos))
        elif tipo in ["CU","CD","CL","CR"]:
            self.lista_entes.append(SpriteCanon(pos,tipo[1]))
        elif tipo == "BM":
            self.lista_entes.append(SpriteAppleNormal(pos))
        elif tipo == "BC":
            self.lista_entes.append(SpriteAppleHielo(pos))
        self.grilla.addWidget(self.lista_entes[-1], self.lista_entes[-1].pos[0],
                                self.lista_entes[-1].pos[1] + 8)
    

    def anadir_zanahoria(self, pos: tuple, dir: str):
        '''
        Crea nuevos sprites, puntualmente para las zanahorias.
        '''
        self.lista_entes.append(SpriteZanahoria(pos, dir))
        self.grilla.addWidget(self.lista_entes[-1], pos[0], pos[1] + 8)


    def redibujar_ente(self, id: int, new_pos: tuple, dir: str):
        '''
        Requiere los datos de un ente en el backend para borrarlo y redibujarlo
        en une nueva posición.
        '''
        cambiandose = self.lista_entes[id]
        if hasattr(cambiandose, "redireccionar"):
            cambiandose.redireccionar(dir)
        self.grilla.removeWidget(cambiandose)
        self.grilla.addWidget(self.lista_entes[id], new_pos[0], new_pos[1] + 8)


    def refrescar_sprite(self, id: int):
        '''
        Cambia el sprite actual.
        '''
        cambiandose = self.lista_entes[id]
        if hasattr(cambiandose, "intercalado"):
            cambiandose.intercalado += 1
            cambiandose.redireccionar(cambiandose.dir)
    

    def sprite_base(self, id: int):
        '''
        Vuelve al sprite base; usado sólo en el conejo
        '''
        cambiandose = self.lista_entes[id]
        if hasattr(cambiandose, "intercalado"):
            cambiandose.intercalado = 0
            cambiandose.redireccionar(cambiandose.dir)
    

    def matar_sprite(self, id: int):
        '''
        Hace invisible a un sprite de un ente que esté considerado muerto
        '''
        self.lista_entes[id].setFixedSize(0, 0)
    

    def click_salir(self):
        sys.exit()
    

    def pausar(self):
        self.senal_pausar.emit()
    

    def keyPressEvent(self, evento: QKeyEvent):
        '''
        Detecta los presionamiento de teclas
        '''
        tecla = evento.text().lower()
        if tecla == "p":
            self.pausar()
        if tecla in ["w", "a", "s", "d"]:
            self.senal_tecla_wasd.emit(tecla)
        if tecla == "m":
            self.request_mapa()
        self.current_sequence.append(tecla)
        self.current_sequence.pop(0)
        if self.current_sequence == ["k", "i", "l"]:
            self.kil_method()
        if self.current_sequence == ["i", "n", "f"]:
            self.inf_method()


    def kil_method(self):
        self.senal_kil.emit()


    def inf_method(self):
        self.senal_inf.emit()
    

    def request_mapa(self):
        self.senal_print_mapa.emit()
    
    
    def ocultarse(self):
        self.hide()