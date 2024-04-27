from PyQt6.QtCore import QObject, pyqtSignal, QTimer
import parametros as p
from backend.logica_entes import (LogicaConejo, LogicaLoboH, LogicaLoboV, LogicaCanon,
    LogicaAppleHielo, LogicaAppleNormal, LogicaZanahoria)
from aux_cliente import mover_enemigo, invertir_dir, mover_conejo_posible
from threading import Lock
from funciones_cliente import calcular_puntaje
class LogicaJuego(QObject):
    '''
    Lógica de juego del programa
    '''
    senal_bg_tablero = pyqtSignal(list)
    senal_anadir_entes_al_cargar = pyqtSignal(str, tuple, int)
    senal_anadir_zanahoria = pyqtSignal(tuple, str)
    senal_mover_sprite = pyqtSignal(int,tuple, str)
    bunny_lock = Lock()
    senal_matar_sprite = pyqtSignal(int)
    senal_actualizar_reloj = pyqtSignal(str)
    senal_actualizar_vidas = pyqtSignal(str)
    senal_actualizar_score = pyqtSignal(str)
    senal_pasar_juego = pyqtSignal(str)
    senal_cero_vidas = pyqtSignal()
    senal_ocultar_juego = pyqtSignal()
    senal_guardar_score = pyqtSignal(str)
    senal_refrescar_sprite = pyqtSignal(int)
    senal_sprite_base = pyqtSignal(int)

    #Generación de nivel

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.restar_tiempo = QTimer(self)
        self.restar_tiempo.setInterval(1000)
        self.restar_tiempo.timeout.connect(self.pasar_seg)
        self.inf_activo = False
        self.juego_finalizado = False
    

    def cargar_nivel(self, user_data: str):
        '''
        Manda la solicitud para cargar el nivel correspondiente.
        User_data se ve como:

            [0]      [1]   [2]             [3]   [4:]
            username,nivel,score_acumulado,vidas,*poderes
        '''
        user_data = user_data.split(",")
        self.user_data = user_data
        if user_data[1] == "1":
            self.user_data[2] = "0"
            self.senal_actualizar_score.emit("0")
            leer = open(p.PATH_TABLERO_1, "r")
        elif user_data[1] == "2":
            leer = open(p.PATH_TABLERO_2, "r")
        elif user_data[1] == "3":
            leer = open(p.PATH_TABLERO_3, "r")
        tablero = leer.readlines()[:16] #Se lee el tablero para el nivel correspondiente
        leer.close()
        for i in range(16):
            tablero[i] = tablero[i].strip("\n").split(",")
        self.senal_bg_tablero.emit(tablero)
        self.matriz_tablero = tablero
        self.lobos_eliminados = 0
        self.pausa = False
        bunny_intervalo = 1000 // p.VELOCIDAD_CONEJO
        self.bunny_move_time = QTimer() #Timer del movimiento del conejo
        self.bunny_move_time.setInterval(bunny_intervalo)
        self.bunny_move_time.timeout.connect(self.mover_conejo)
        self.bunny_refresh_time = QTimer() #Timer del intercalado del conejo
        self.bunny_refresh_time.setInterval(int(bunny_intervalo // p.INTERCALADO_CONEJO))
        self.bunny_refresh_time.timeout.connect(self.intercalar_conejo)
        self.tiempo_restante = int(120 * p.POND_ACUMULADOS[int(self.user_data[1]) - 1])
        self.senal_actualizar_reloj.emit(str(self.tiempo_restante))
        self.restar_tiempo.start()
        self.spawnear_entes()

    
    def spawnear_entes(self):
        '''
        Genera los entes cuando se entra por primera vez al nivelo se ha perdido una vida. 
        Los entes tendrán un objeto asignado que realizará lógica por ellos (como su timer).
        '''
        self.lista_entes = []
        self.contador_id = 0
        for i in range(16):
            for j in range(16):
                casilla = self.matriz_tablero[i][j]
                if casilla == "C":
                    self.conejo = LogicaConejo((i, j), self.contador_id)
                    self.lista_entes.append(self.conejo)
                if casilla == "LH":
                    self.lista_entes.append(LogicaLoboH((i, j), self.contador_id, 
                                                        int(self.user_data[1])))
                    self.conectar_lobo(self.lista_entes[-1])
                if casilla == "LV":
                    self.lista_entes.append(LogicaLoboV((i, j), self.contador_id,
                                                        int(self.user_data[1])))
                    self.conectar_lobo(self.lista_entes[-1])
                if casilla in ["CU", "CD", "CL", "CR"]:
                    self.lista_entes.append(LogicaCanon((i, j), self.contador_id, casilla[1]))
                    self.conectar_canon(self.lista_entes[-1])
                if casilla == "BM":
                    self.lista_entes.append(LogicaAppleNormal((i, j), self.contador_id))
                if casilla == "BC":
                    self.lista_entes.append(LogicaAppleHielo((i, j), self.contador_id))
                if not self.matriz_tablero[i][j] in "-PES":
                    self.senal_anadir_entes_al_cargar.emit(casilla, (i, j), self.contador_id)
                    self.contador_id += 1

    #Lógica de cañones y zanahorias

    def conectar_canon(self, canon: LogicaCanon):
        canon.senal_spawnear_zanahoria.connect(self.spawnear_zanahorias)


    def spawnear_zanahorias(self, canon: LogicaCanon):
        '''
        Self explanatory
        '''
        ypos = canon.pos[0]
        xpos = canon.pos[1]
        if canon.dir == "w":
            ypos -= 1
        elif canon.dir == "a":
            xpos -= 1
        elif canon.dir == "s":
            ypos += 1
        elif canon.dir == "d":
            xpos += 1
        if self.matriz_tablero[ypos][xpos] == "C":
            self.perder_vida()
            return
        self.lista_entes.append(LogicaZanahoria((ypos, xpos), self.contador_id, canon.dir))
        self.conectar_zanahoria(self.lista_entes[-1])
        self.senal_anadir_zanahoria.emit((ypos, xpos), canon.dir)
        self.matriz_tablero[ypos][xpos] = "Z"
        self.contador_id += 1


    def conectar_zanahoria(self, zanahoria: LogicaZanahoria):
        zanahoria.senal_try_mover_zanahoria.connect(self.mover_zanahoria)
    

    def mover_zanahoria(self, zanah: LogicaZanahoria):
        '''
        Self explanatory
        '''
        mov = mover_enemigo(self.matriz_tablero, zanah.pos, zanah.dir)
        if mov[0] == "free":
            self.matriz_tablero[zanah.pos[0]][zanah.pos[1]] = "-"
            zanah.pos = (mov[1], mov[2])
            self.matriz_tablero[zanah.pos[0]][zanah.pos[1]] = "Z"
        elif mov[0] == "blocked":
            self.matar_ente(zanah)
        elif mov[0] == "kill":
            self.perder_vida()
            return
        self.senal_mover_sprite.emit(zanah.id, zanah.pos, zanah.dir)

    #Logica de lobos

    def conectar_lobo(self, lobo: LogicaLoboH | LogicaLoboV):
        lobo.senal_try_mover_lobo.connect(self.mover_lobo)
        lobo.senal_intercalar_lobo.connect(self.intercalar_lobo)


    def mover_lobo(self, lobo: LogicaLoboH | LogicaLoboV):
        '''
        Self explanatory
        '''
        mov = mover_enemigo(self.matriz_tablero, lobo.pos, lobo.dir)
        if mov[0] == "free":
            self.matriz_tablero[lobo.pos[0]][lobo.pos[1]] = "-"
            lobo.pos = (mov[1], mov[2])
            self.matriz_tablero[lobo.pos[0]][lobo.pos[1]] = lobo.tipo
        elif mov[0] == "blocked":
            lobo.dir = invertir_dir(lobo.dir)
        elif mov[0] == "kill":
            self.perder_vida()
            return
        self.senal_mover_sprite.emit(lobo.id, lobo.pos, lobo.dir)
    

    def intercalar_lobo(self, lobo: LogicaLoboH | LogicaLoboV):
        self.senal_refrescar_sprite.emit(lobo.id)
    
    #Logica del conejo

    def empezar_movimiento_conejo(self, tecla):
        '''
        Lock para restringir al conejo de llegar lo más lejos posible
        '''
        if not self.bunny_lock.locked():
            self.bunny_lock.acquire()
            self.conejo.dir = tecla
            self.bunny_move_time.start()
            self.bunny_refresh_time.start()

    def mover_conejo(self):
        '''
        Self explanatory.
        '''
        mov = mover_conejo_posible(self.matriz_tablero, self.conejo.pos, self.conejo.dir)
        if mov[0] == "kill":
            self.bunny_move_time.stop()
            self.bunny_refresh_time.stop()
            self.bunny_lock.release()
            self.perder_vida()
            return
        elif mov[0] == "blocked":
            self.bunny_move_time.stop()
            self.bunny_refresh_time.stop()
            self.sprite_base()
            self.bunny_lock.release()
        elif mov[0] == "win":
            self.pasar_nivel()
        else:
            self.matriz_tablero[self.conejo.pos[0]][self.conejo.pos[1]] = "-"
            self.conejo.pos = (mov[1], mov[2])
            self.matriz_tablero[self.conejo.pos[0]][self.conejo.pos[1]] = "C"
            self.senal_mover_sprite.emit(self.conejo.id, self.conejo.pos, self.conejo.dir)
            if not self.juego_finalizado:
                mov = mover_conejo_posible(self.matriz_tablero, self.conejo.pos, self.conejo.dir)

    def intercalar_conejo(self):
        self.senal_refrescar_sprite.emit(self.conejo.id)
    
    def sprite_base(self):
        self.senal_sprite_base.emit(self.conejo.id)

    #Lógica de manejo de tiempo

    def pasar_seg(self):
        '''
        Hace pasar un segundo en el backend
        '''
        if self.inf_activo or self.pausa:
            return
        self.tiempo_restante -= 1
        self.senal_actualizar_reloj.emit(str(self.tiempo_restante))
        if self.tiempo_restante == 0:
            self.perder_vida()


    def pausar(self):
        '''
        Detiene todos los timers
        '''
        if self.pausa:
            if self.pausado_en_movimiento:
                self.bunny_move_time.start()
                self.bunny_refresh_time.start()
            else:
                self.bunny_lock.release()
            for ente in self.lista_entes:
                if ente.tipo in ["LH", "LV", "CU", "CD", "CL", "CR", "Z"]:
                    ente.reanudar()
            self.pausa = False
        else:
            if self.bunny_lock.locked():
                self.pausado_en_movimiento = True
                self.bunny_move_time.stop()
                self.bunny_refresh_time.stop()
            else:
                self.pausado_en_movimiento = False
                self.bunny_lock.acquire()
            for ente in self.lista_entes:
                if ente.tipo in ["LH", "LV", "CU", "CD", "CL", "CR", "Z"]:
                    ente.pausar()
            self.pausa = True

    #Cheatcodes

    def ejecutar_kil(self):
        '''
        Pausará a todos los cañones y eliminará a los lobos y zanahorias
        '''
        for ente in self.lista_entes:
            if ente.tipo == "Z":
                self.matar_ente(ente)
            elif ente.tipo in ["LV", "LH"]:
                self.lobos_eliminados += 1
                self.matar_ente(ente)
            elif ente.tipo in ["CU", "CD", "CL", "CR"]:
                ente.pausar()


    def matar_ente(self, ente):
        '''
        Pausa el timer de cada ente y lo elimina del mapa (pierde colisión).
        '''
        ente.pausar()
        self.senal_matar_sprite.emit(ente.id)
        self.matriz_tablero[ente.pos[0]][ente.pos[1]] = "-"


    def ejecutar_inf(self):
        self.inf_activo = not self.inf_activo
    
    #Lógica de cambio de nivel, y pérdida de vidas

    def perder_vida(self):
        '''
        Realiza el reinicio de nivel y las acciones relacionadas a la pérdida de vidas.
        '''
        if self.bunny_lock.locked():
            self.bunny_lock.release()
        if not self.inf_activo:
            self.user_data[3] = str(int(self.user_data[3]) - 1)
        self.senal_actualizar_vidas.emit(str(self.user_data[3]))
        user_data = ",".join(self.user_data)
        if int(self.user_data[3]) > 0:
            self.cargar_nivel(user_data)
        else:
            self.pausar()
            self.senal_ocultar_juego.emit()
            self.senal_cero_vidas.emit()


    def pasar_nivel(self):
        '''
        Recopila la información para poder cargar el siguiente nivel
        y guardar la info en el server.
        '''
        if self.juego_finalizado:
            return
        if self.inf_activo:
            add_score = p.PUNTAJE_INF
        elif self.lobos_eliminados == 0:
            add_score = 0
        else:
            add_score = calcular_puntaje(self.tiempo_restante, int(self.user_data[3]),
                                         self.lobos_eliminados, p.PUNTAJE_LOBO)
        self.user_data[2] = str(round(float(self.user_data[2]) + add_score, 2))
        self.senal_actualizar_score.emit(self.user_data[2])
        user_data = ",".join(self.user_data)
        self.senal_guardar_score.emit(user_data)
        if self.bunny_lock.locked():
            self.bunny_lock.release()
        if self.user_data[1] == "3":
            self.juego_finalizado = True
            self.senal_pasar_juego.emit(self.user_data[2])
            self.senal_ocultar_juego.emit()
            return
        self.user_data[1] = str(int(self.user_data[1]) + 1)
        user_data = ",".join(self.user_data)
        self.cargar_nivel(user_data)
    
    #Método remanente

    def print_mapa(self):
        for i in self.matriz_tablero:
            imprimible = ""
            for j in i:
                imprimible += j + "   "[len(j):]
            print(imprimible)