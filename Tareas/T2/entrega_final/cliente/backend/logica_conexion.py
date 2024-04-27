import socket
import sys
import json
from threading import Thread
from PyQt6.QtCore import QObject, pyqtSignal
from aux_cliente import separa_encripta_codifica, obtener_int, obtener_qty_mensajes, decodificar_mensaje

class LogicaConexion(QObject):
    '''
    Backend del cliente para manejar la ventana de Login y las conexiones 
    con el servidor, incluidas las de cambio de nivel y game over.
    '''

    senal_server_caido = pyqtSignal()
    senal_abrir_login = pyqtSignal()
    senal_anadir_hs = pyqtSignal(list)
    senal_baneado = pyqtSignal()
    senal_abrir_juego = pyqtSignal(str)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def conectar_a_servidor(self) -> None:
        '''
        Hace el intento de conexion a servidor. 
        En caso de lograrse, se ejecuta conectado a servidor.
        '''
        try:
            port = sys.argv
            file = open("server_ip.json", "rb")
            loaded_file = json.load(file)
            file.close()
            self.sock_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock_cliente.connect((loaded_file["host"], int(port[1])))
            print("Conectado a servidor")
            self.senal_abrir_login.emit()
            thread_conectado_a_servidor = Thread(target=self.conectado_a_servidor,
                                                args = (self.sock_cliente,),
                                                daemon = True)
            thread_conectado_a_servidor.start() #Conexión lograda
            
        except ConnectionError: #Cuando el server no está prendido
            print("No se conectó a servidor :(")
            sys.exit()
        

    def conectado_a_servidor(self, sock: socket.socket) -> None:
        '''
        Se llama como thread, ya no me acuerdo por qué xd.
        '''
        while True:
            try:
                data = self.sock_cliente.recv(4)
                if not data: #El server se cerró
                    print("Se perdio la conexión con el servidor")
                    self.senal_server_caido.emit()
                    break
                mensaje_codificado = [obtener_int(data)]
                #Se recibe el mensaje codificado y de decodifica
                for chunk in range(obtener_qty_mensajes(mensaje_codificado[0])):
                    data = self.sock_cliente.recv(4)
                    mensaje_codificado.append(data)
                    data = self.sock_cliente.recv(36)
                    mensaje_codificado.append(data)
                mensaje = decodificar_mensaje(mensaje_codificado)

                if mensaje[:4] == "HISC": #Añade los hi-scores a la ventana de login
                    hi_scores = mensaje[5:].split(",")
                    self.senal_anadir_hs.emit(hi_scores)
                elif mensaje[:4] == "LOGN": #Cuando se ingresa un nombre válido
                    if mensaje[5:] == "true": #Está baneado
                        self.senal_baneado.emit()
                    elif mensaje[5:8] == "new": #No tiene progreso guardado
                        vidas = "3"
                        self.senal_abrir_juego.emit(mensaje[9:] + ",1,0," + vidas)
                    else: #Tiene progreso guardado
                        cambiar_nivel = mensaje[5:].split(",")
                        if cambiar_nivel[1] == "3":
                            cambiar_nivel[1] = "1"
                            vidas = "3"
                        elif cambiar_nivel[1] == "1":
                            cambiar_nivel[1] = "2"
                            vidas = "2"
                        elif cambiar_nivel[1] == "2":
                            cambiar_nivel[1] = "3"
                            vidas = "1"
                        cambiado_nivel = ",".join(cambiar_nivel)
                        self.senal_abrir_juego.emit(cambiado_nivel + "," + vidas)

            except ConnectionError:
                print("Se perdió la conexión con el servidor")


    def validar_usuario(self, username: str) -> None:
        '''
        Cuando el username cumple el formato, se envía al server
        para saber si está baneado
        '''
        for chunk in separa_encripta_codifica("USER." + username):
            self.sock_cliente.sendall(chunk)
    

    def guardar_score(self, data: str):
        '''
        Envía el username y score a la base de datos del server para guardarlos. data se ve como:
            [0]      [1]   [2]             [3]   [4:]
            username,nivel,score_acumulado,vidas,*poderes
        '''
        data = data.split(",")
        for chunk in separa_encripta_codifica("SAVE." + data[0] + "," + data[1] + "," + data[2]):
            self.sock_cliente.sendall(chunk)
