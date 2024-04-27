from PyQt6.QtWidgets import QApplication
from backend.logica_conexion import LogicaConexion
from backend.logica_juego import LogicaJuego
from frontend.ventana_login import VentanaLogin
from frontend.ventana_login import VentanaMalFormato
from frontend.ventana_login import VentanaServerCaido
from frontend.ventana_login import VentanaBaneado
from frontend.ventana_login import VentanaGanador
from frontend.ventana_login import VentanaPerdedor
from frontend.ventana_juego import VentanaJuego
from frontend.reproductor import Reproductor
import sys

class InstanciaDeJuego():
    def __init__(self) -> None:
        #Instanciamos todas las ventanas
        self.l_conexion = LogicaConexion()
        self.v_login = VentanaLogin()
        self.v_mal_formato = VentanaMalFormato()
        self.v_server_caido = VentanaServerCaido()
        self.v_baneado = VentanaBaneado()
        self.v_juego = VentanaJuego()
        self.l_juego = LogicaJuego()
        self.v_ganador = VentanaGanador()
        self.v_perdedor = VentanaPerdedor()
        self.reproductor = Reproductor()
        #Creamos las señales
        self.conectar_senales()
        #Empezamos el programa
        self.l_conexion.conectar_a_servidor()
    

    def conectar_senales(self):
        #No tiene ningún orden en particular, aparecen las conexiones en orden cronologico
        #Tampoco se me ocurre como ponerlas para hacerlo legible
        self.l_conexion.senal_abrir_login.connect(self.v_login.mostrarse)
        self.v_login.senal_username_ingresado.connect(self.l_conexion.validar_usuario)
        self.v_login.senal_mal_formato.connect(self.v_mal_formato.mostrarse)
        self.l_conexion.senal_server_caido.connect(self.v_server_caido.mostrarse)
        self.l_conexion.senal_anadir_hs.connect(self.v_login.anadir_hs)
        self.l_conexion.senal_baneado.connect(self.v_baneado.mostrarse)
        self.l_conexion.senal_abrir_juego.connect(self.v_login.ocultarse)
        self.l_conexion.senal_abrir_juego.connect(self.l_juego.cargar_nivel)
        self.l_conexion.senal_abrir_juego.connect(self.v_juego.ingresar_nivel)
        self.l_juego.senal_bg_tablero.connect(self.v_juego.background_tablero)
        self.l_juego.senal_anadir_entes_al_cargar.connect(self.v_juego.anadir_entes_al_cargar)
        self.l_juego.senal_mover_sprite.connect(self.v_juego.redibujar_ente)
        self.l_juego.senal_anadir_zanahoria.connect(self.v_juego.anadir_zanahoria)
        self.v_juego.senal_tecla_wasd.connect(self.l_juego.empezar_movimiento_conejo)
        self.v_juego.senal_print_mapa.connect(self.l_juego.print_mapa)
        self.l_juego.senal_matar_sprite.connect(self.v_juego.matar_sprite)
        self.v_juego.senal_pausar.connect(self.l_juego.pausar)
        self.l_juego.senal_actualizar_reloj.connect(self.v_juego.pasar_seg)
        self.l_juego.senal_actualizar_vidas.connect(self.v_juego.actualizar_vidas)
        self.l_juego.senal_actualizar_score.connect(self.v_juego.actualizar_score)
        self.l_juego.senal_pasar_juego.connect(self.v_ganador.mostrarse)
        self.l_juego.senal_ocultar_juego.connect(self.v_juego.ocultarse)
        self.v_juego.senal_kil.connect(self.l_juego.ejecutar_kil)
        self.v_juego.senal_inf.connect(self.l_juego.ejecutar_inf)
        self.l_juego.senal_guardar_score.connect(self.l_conexion.guardar_score)
        self.v_ganador.senal_audio_victoria.connect(self.reproductor.reproducir_victoria)
        self.v_perdedor.senal_audio_derrota.connect(self.reproductor.reproducir_derrota)
        self.l_juego.senal_cero_vidas.connect(self.v_perdedor.mostrarse)
        self.l_juego.senal_refrescar_sprite.connect(self.v_juego.refrescar_sprite)



if __name__ == '__main__':
    def hook(type, value, traceback):
        print(type)
        print(value)
        print(traceback)
    sys.__excepthook__ = hook
    app = QApplication([])
    instancia = InstanciaDeJuego()
    sys.exit(app.exec())