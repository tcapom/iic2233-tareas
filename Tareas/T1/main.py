import sys
from tablero import Tablero
from imprimir_tablero import imprimir_tablero

if __name__ == "__main__":
    argumentos_por_consola = sys.argv

    #Se comprueba la primera condicion de ingreso
    c_ingreso1 = True
    for i in argumentos_por_consola[1]:
        if i not in "qwertyuiopasdfghjklzxcvbnm":
            c_ingreso1 = False
    if len(argumentos_por_consola[1]) < 4:
        c_ingreso1 = False

    #Se extrae el archivo txt y se comprueba la segunda condicion
    abrir = open("tableros.txt","r")
    tableros = abrir.readlines()
    abrir.close()
    c_ingreso2 = False
    for i in range(len(tableros)):
        tableros[i] = tableros[i].strip("\n").split(",")
        if tableros[i][0] == argumentos_por_consola[2]:
            c_ingreso2 = True
            tablero_a_crear = tableros[i]

    #Se imprimen los mensajes correspondientes
    if (not c_ingreso1):
        print("--- EL NOMBRE DE USUARIO NO ES VALIDO ---")
    if (not c_ingreso2):
        print("--- EL TABLERO INDICADO NO EXISTE ---")
    if not (c_ingreso1 and c_ingreso2):
        print("Saliendo del programa")
        sys.exit()

    #A partir de aca uno solo sigue en el programa si ingreso los datos bien
    print("Que bueno verte de vuelta",argumentos_por_consola[1]+"! :D")

    #Creamos el tablero como objeto
    tablero_creandose = [] 
    contador = 3
    for i in range(int(tablero_a_crear[1])):
        tablero_creandose.append([])
        for j in range(int(tablero_a_crear[2])):
            tablero_creandose[i].append(tablero_a_crear[contador])
            contador += 1
    tablero = Tablero(tablero_creandose)

    #Usamos un ciclo while True, cosa que solo sea interrumpido con sys.exit() al ingresar un "4"
    while True:
        print("\n--- Acciones disponibles ---\n")
        print("[1] Mostrar tablero")
        print("[2] Limpiar tablero")
        print("[3] Solucionar tablero")
        print("[4] Salir del programa\n")
        entrada = input("Seleccione una opcion: ")
        if entrada not in ["1","2","3","4"]: #Da un mensaje cuando se da un input invalido
            print("\nPor favor intenta colocar una accion valida\n")
        if entrada == "1":
            print("\nEste es el tablero actual:")
            imprimir_tablero(tablero.tablero)
        if entrada == "2":
            print("\nEliminando todos los peones...")
            tablero.limpiar()
        if entrada == "3":
            print("\n Veamos si este tablero se puede solucionar...\n...")
            solucion_encontrada = tablero.solucionar()
            if solucion_encontrada == []:
                print("\nNuestro tablero actual no tiene solucion :(")
            else:
                print("\n Nuestra solución encontrada es la siguiente:")
                imprimir_tablero(solucion_encontrada)
                print("\nSe te habria ocurrido?")
        if entrada == "4":
            print("\nOjala vernos pronto")
            sys.exit() #Se sale del programa