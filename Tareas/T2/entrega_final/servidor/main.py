'''
Al llamarse como __main__, se ejecuta el ciclo del servidor
'''
import sys
import socket
import json
from threading import Thread, Lock
from funciones_servidor import usuario_permitido
from aux_servidor import (separa_encripta_codifica, obtener_int, obtener_qty_mensajes,
                          decodificar_mensaje)

def thread_con_cliente(socket_thread: socket.socket, address):
    '''
    Abre un thread para comunicarse con cada cliente
    '''
    hi_scores = conseguir_hs()
    for chunk in separa_encripta_codifica(hi_scores):
        socket_thread.sendall(chunk)
    while True: #Ciclo que recibe información de un cliente
        try:
            data = socket_thread.recv(4)
            if not data: #Desconecta al usuario
                print(address, "ha salido del juego")
                socket_thread.close()
                break
            mensaje_codificado = [obtener_int(data)]
            for chunk in range(obtener_qty_mensajes(mensaje_codificado[0])):
                data = socket_thread.recv(4)
                mensaje_codificado.append(data)
                data = socket_thread.recv(36)
                mensaje_codificado.append(data)
            mensaje = decodificar_mensaje(mensaje_codificado)
            if mensaje[0:4] == "USER": #Ingreso de username
                user_ingresando = mensaje[5:]
                leer = open("bloqueados.txt", "r")
                bloqueados = leer.readline()
                leer.close()
                bloqueados = bloqueados.strip("\n").split(",")
                if not usuario_permitido(user_ingresando, bloqueados): #Username bloqueado
                    for chunk in separa_encripta_codifica("LOGN.true"):
                        socket_thread.sendall(chunk)
                    print(address,"intento ingresar con username baneado", user_ingresando)
                else: #Buscar información del usuario en puntajes
                    puntaje_lock.acquire()
                    leer = open("puntaje.txt", "r")
                    puntajes = leer.readlines()
                    leer.close()
                    puntaje_lock.release()
                    user_encontrado = False
                    for user in puntajes:
                        user = user.strip("\n").split(",")
                        if user_ingresando in user:
                            print(user[0],"ingresa al juego,", 
                                  "siendo su ultimo nivel completado", user[1])
                            enviar = ",".join(user)
                            for chunk in separa_encripta_codifica("LOGN." + enviar):
                                socket_thread.sendall(chunk)
                            user_encontrado = True
                    if not user_encontrado:
                        print(user_ingresando,"esta ingresando por primera vez")
                        for chunk in separa_encripta_codifica("LOGN.new," + user_ingresando):
                            socket_thread.sendall(chunk)
            if mensaje[0:4] == "SAVE": #Se reciben datos para guardarlos en puntaje.txt
                datos_a_guardar = mensaje[5:]
                datos_en_lista = datos_a_guardar.split(",")
                if datos_en_lista[1] == "3":
                    print(datos_en_lista[0], "ha superado el juego con", 
                          datos_en_lista[2], "puntos")
                else:
                    print(datos_en_lista[0], "pasó al nivel", datos_en_lista[1], "con",
                          datos_en_lista[2], "puntos")
                username = datos_a_guardar.split(",")[0]
                puntaje_lock.acquire()
                leer = open("puntaje.txt", "r")
                puntajes = leer.readlines()
                leer.close()
                nuevo_user = True
                for i in range(len(puntajes)):
                    puntajes[i] = puntajes[i].strip("\n")
                    revisando_usuario = puntajes[i].split(",")[0]
                    if revisando_usuario == username:
                        nuevo_user = False
                        puntajes[i] = datos_a_guardar
                        break
                if nuevo_user:
                    puntajes.append(datos_a_guardar)
                escribir = "\n".join(puntajes)
                leer = open("puntaje.txt", "w")
                leer.write(escribir)
                leer.close()
                puntaje_lock.release()
            

        except ConnectionError:
            print("Se perdió conexión con:",address)


def conseguir_hs():
    '''
    Abre puntaje.txt y retorna los 5 puntajes más altos
    '''
    puntaje_lock.acquire()
    leer = open("puntaje.txt","r")
    puntajes = leer.readlines()
    leer.close()
    puntaje_lock.release()
    for i in range(len(puntajes)):
        puntajes[i] = puntajes[i].strip("\n").split(",")
    hi_scores = "HISC"
    for i in range(5):
        max_puntaje = 0
        max_index = -1
        for j in range(len(puntajes)):
            if len(puntajes[j]) > 1:
                if float(puntajes[j][2]) > max_puntaje:
                    max_puntaje = float(puntajes[j][2])
                    max_index = j
        found_score = puntajes.pop(max_index)
        hi_scores += "," + found_score[0] + "," + found_score[2]
    return hi_scores

if __name__ == "__main__":
    puntaje_lock = Lock() #Lock para que solo un thread abra puntaje.txt a la vez
    port = sys.argv
    file = open("server_ip.json", "rb")
    loaded_file = json.load(file)
    file.close()
    if len(port) == 1:
        print("No se ingresó puerto en la consola")
        sys.exit()
    sock_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_server.bind((loaded_file["host"], int(port[1])))
    print("Servidor inicializado en " + loaded_file["host"] + ":" + str(int(port[1])))
    sock_server.listen(5)
    while True:
        try:
            socket_cliente, address = sock_server.accept()
            print(address,"se ha conectado al servidor")
            nuevo_thread = Thread(target= thread_con_cliente, args= (socket_cliente, address),
                                 daemon= True)
            nuevo_thread.start()
        except KeyboardInterrupt:
            print("\nEl Servidor ha sido detenido")
            sock_server.close()
            break