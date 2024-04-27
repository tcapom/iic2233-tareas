from funciones_servidor import separar_mensaje, codificar_mensaje, encriptar_mensaje, serializar_mensaje, usuario_permitido

def obtener_int(entrada: bytearray):
    '''
    Cambia bytes a int en formato big endian.
    '''
    return int.from_bytes(entrada, "big")

def obtener_qty_mensajes(entrada: int):
    '''
    Utilizar la función para saber cuantos mensajes se recibirán después
    de obtener el largo del mensaje a reestructurar.
    '''
    if entrada % 36 == 0:
        return entrada // 36
    return entrada // 36 + 1

def separa_encripta_codifica(entrada):
    '''
    Toma un mensaje y realiza todos los pasos para enviarlo encriptado
    '''
    return codificar_mensaje(encriptar_mensaje(serializar_mensaje(entrada)))

def decodificar_mensaje(entrada: list):
    '''
    Función inversa a separa_encripta_codifica
    '''
    largo = entrada[0]
    bytes_de_interes = bytearray()
    for i in range(2,len(entrada),2):
        bytes_de_interes.extend(entrada[i])
    bytes_de_interes = bytes_de_interes[:largo]
    desordenado = bytes_de_interes.decode("UTF-8")
    orden = desordenado[0]
    desordenado = desordenado[1:]
    largo = largo - 1
    lotes = None
    if largo % 6 in [0,3]:
        lotes = [desordenado[:largo // 3], desordenado[largo // 3:largo * 2 // 3], 
                 desordenado[largo * 2 // 3:]]
    elif largo % 6 == 1 and orden == "1":
        lotes = [desordenado[:largo // 3 + 1], desordenado[largo // 3 + 1:largo * 2 // 3 + 1], 
                 desordenado[largo * 2 // 3 + 1:]]
    elif largo % 6 == 1 and orden == "0":
        lotes = [desordenado[:largo // 3], desordenado[largo // 3:largo * 2 // 3 + 1], 
                 desordenado[largo * 2 // 3 + 1:]]
    elif largo % 6 == 2 and orden == "1":
        lotes = [desordenado[:largo // 3 + 1], desordenado[largo // 3 + 1:largo * 2 // 3], 
                 desordenado[largo * 2 // 3:]]
    elif largo % 6 == 2 and orden == "0":
        lotes = [desordenado[:largo // 3 + 1], desordenado[largo // 3 + 1:largo * 2 // 3 + 1], 
                 desordenado[largo * 2 // 3 + 1:]]
    elif largo % 6 == 4 and orden == "1":
        lotes = [desordenado[:largo // 3], desordenado[largo // 3 :largo * 2 // 3 + 2], 
                 desordenado[largo * 2 // 3 + 1:]]
    elif largo % 6 == 4 and orden == "0":
        lotes = [desordenado[:largo // 3], desordenado[largo // 3:largo * 2 // 3], 
                 desordenado[largo * 2 // 3:]]
    elif largo % 6 == 5 and orden == "1":
        lotes = [desordenado[:largo // 3 + 2], desordenado[largo // 3 :largo * 2 // 3 + 1], 
                 desordenado[largo * 2 // 3:]]
    elif largo % 6 == 5 and orden == "0":
        lotes = [desordenado[:largo // 3 + 1], desordenado[largo // 3 + 1:largo * 2 // 3], 
                 desordenado[largo * 2 // 3:]]
    if orden == "1":
        lotes = [lotes[0], lotes[2], lotes[1]]
    else:
        lotes = [lotes[1], lotes[0], lotes[2]]
    contador = 0
    final = ""
    while contador < largo:
        if contador % 6 in [0, 5]:
            final += lotes[0][0]
            lotes[0] = lotes[0][1:]
        if contador % 6 in [1, 4]:
            final += lotes[1][0]
            lotes[1] = lotes[1][1:]
        if contador % 6 in [2, 3]:
            final += lotes[2][0]
            lotes[2] = lotes[2][1:]
        contador += 1
    return final


