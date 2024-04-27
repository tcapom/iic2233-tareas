import sys
import funciones_cliente as fn_clientes
import parametros as p
from PyQt6.QtWidgets import (QWidget, QLabel, QLineEdit, QPushButton, 
                             QGridLayout, QVBoxLayout, QHBoxLayout)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import pyqtSignal

class VentanaLogin(QWidget):
    '''
    Ventana de Login del programa
    '''
    senal_username_ingresado = pyqtSignal(str)
    senal_mal_formato = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_gui()


    def init_gui(self):
        self.setGeometry(0, 0, 800, 600)
        self.setFixedSize(800,600)
        self.setWindowTitle("Ingreso")
        self.background = QLabel(self)
        self.background.setStyleSheet("background: pink")
        self.background.setGeometry(0, 0, 800, 600) 
        self.logo = QLabel(self)
        self.logo.setGeometry(0, 50, 100, 100)
        self.logo.setPixmap(QPixmap(p.PATH_LOGO))
        self.logo.setScaledContents(True)
        self.rellenar_usuario = QLineEdit('', self)
        self.ingresa_tu_usuario = QLabel('Ingresa tu usuario:', self)
        self.ingresa_tu_usuario.move(10, 250)
        boton_salir = QPushButton('Salir', self)
        boton_salir.clicked.connect(self.click_salir)
        boton_ingresar = QPushButton('Ingresar', self)
        boton_ingresar.clicked.connect(self.click_ingresar)
        self.hbox = QHBoxLayout()
        self.hbox.addWidget(boton_salir)
        self.hbox.addWidget(boton_ingresar)
        self.top_puntajes = QLabel('Mejores puntajes:', self)
        self.top_puntajes.move(10, 330)


    def mostrarse(self):
        self.show()
    

    def ocultarse(self):
        self.hide()


    def click_salir(self):
        sys.exit()


    def click_ingresar(self):
        '''
        Manda la solicitud con el usuario para ingresar
        '''
        username_ingresado = self.rellenar_usuario.text()
        if fn_clientes.validacion_formato(username_ingresado):
            self.senal_username_ingresado.emit(username_ingresado)
        else:
            self.senal_mal_formato.emit()
    

    def anadir_hs(self, hi_scores: list[str]):
        '''
        Actualiza la información de los hi-scores
        '''
        grilla = QGridLayout()
        posiciones = [(i, j) for i in range(5) for j in range(2)]

        for posicion, valor in zip(posiciones, hi_scores):
            nuevo_label = QLabel(valor, self)
            grilla.addWidget(nuevo_label, *posicion)

        vbox = QVBoxLayout()
        vbox.addWidget(self.logo)
        vbox.addWidget(self.rellenar_usuario)
        vbox.addLayout(self.hbox)
        vbox.addLayout(grilla)
        self.setLayout(vbox)


class VentanaMalFormato(QWidget):
    '''
    Ventana que aparece en caso de que el username tenga mal formato
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_gui()


    def init_gui(self):
        self.setGeometry(0, 0, 250, 100)
        self.setMaximumWidth(250)
        self.setMaximumHeight(100)
        self.setWindowTitle("Mal formato :(")
        self.recuerda_que = QLabel('Recuerda que tu usuario debe tener:', self)
        self.recuerda_que.move(0, 0)
        self.rec1 = QLabel('Al menos una mayúscula', self)
        self.rec1.move(20, 20)
        self.rec2 = QLabel('Al menos un número', self)
        self.rec2.move(20, 40)
        self.rec3 = QLabel('Entre 3 y 16 caracteres', self)
        self.rec3.move(20, 60)


    def mostrarse(self):
        self.show()


class VentanaServerCaido(QWidget):
    '''
    Ventana que aparece en caso que el server se caiga
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_gui()


    def init_gui(self):
        self.setGeometry(0, 0, 400, 100)
        self.setMaximumWidth(400)
        self.setMaximumHeight(100)
        self.setWindowTitle("Server Caido")
        self.label_caido = QLabel('El server se cayó :(     Tu progreso no será guardado', self)
        self.label_caido.move(0, 20)
        self.boton_cerrar = QPushButton('Cerrar programa', self)
        self.boton_cerrar.setGeometry(260, 60, 120, 30)
        self.boton_cerrar.clicked.connect(self.cerrar_programa)
    

    def mostrarse(self):
        self.show()


    def cerrar_programa(self):
        sys.exit()

class VentanaBaneado(QWidget):
    '''
    Ventana que aparece cuando el username está baneado
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_gui()


    def init_gui(self):
        self.setGeometry(0, 0, 400, 100)
        self.setMaximumWidth(400)
        self.setMaximumHeight(100)
        self.setWindowTitle("Baneado >:(")
        self.label_caido = QLabel('Este nombre de usuario se encuentra bloqueado.', self)
        self.label_caido.move(0, 20)


    def mostrarse(self):
        self.show()

class VentanaGanador(QWidget):
    '''
    Ventana que aparece al ganar el tercer nivel.
    '''
    senal_audio_victoria = pyqtSignal()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_gui()


    def init_gui(self):
        self.setGeometry(0, 0, 400, 100)
        self.setMaximumWidth(400)
        self.setMaximumHeight(100)
        self.setWindowTitle("GANASTE!!!")
        self.label_felicidades = QLabel("Felicidades! Pudiste pasar el tercer nivel!", self)
        self.label_felicidades.move(10, 20)
    

    def mostrarse(self, score):
        self.senal_audio_victoria.emit()
        self.label_score = QLabel("Tuviste un score de: " + score, self)
        self.label_score.move(10, 40)
        self.show()

class VentanaPerdedor(QWidget):
    '''
    Ventana que aparece cuando pierdes en el juego.
    '''
    senal_audio_derrota = pyqtSignal()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_gui()


    def init_gui(self):
        self.setGeometry(0, 0, 400, 100)
        self.setMaximumWidth(400)
        self.setMaximumHeight(100)
        self.setWindowTitle("PERDISTE :(")
        self.label_motivacion = QLabel("Siempre lo puedes intentar otra vez :D", self)
        self.label_motivacion.move(10, 20)
    
    
    def mostrarse(self):
        self.senal_audio_derrota.emit()
        self.show()