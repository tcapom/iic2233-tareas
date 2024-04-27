def usuario_permitido(nombre: str, usuarios_no_permitidos: list[str]) -> bool:
    if nombre in usuarios_no_permitidos:
        return False
    return True

def serializar_mensaje(mensaje: str) -> bytearray:
    encoded = mensaje.encode("UTF-8")
    return bytearray(encoded)


def separar_mensaje(mensaje: bytearray) -> list[bytearray]:
    lista = [bytearray(b""), bytearray(b""), bytearray(b"")]
    for i in range(len(mensaje)):
        if i % 6 in [0, 5]:
            lista[0].extend(mensaje[i: i + 1])
        if i % 6 in [1, 4]:
            lista[1].extend(mensaje[i: i + 1])
        if i % 6 in [2, 3]:
            lista[2].extend(mensaje[i: i + 1])
    return lista


def encriptar_mensaje(mensaje: bytearray) -> bytearray:
    lista = separar_mensaje(mensaje)
    valor = lista[0][0] + lista[1][-1] + lista[2][0]
    if valor % 2 == 0:
        return bytearray(b"1" + lista[0] + lista[2] + lista[1])
    return bytearray(b"0" + lista[1] + lista[0] + lista[2])


def codificar_mensaje(mensaje: bytearray) -> list[bytearray]:
    largo = len(mensaje)
    lista = [bytearray(largo.to_bytes(length = 4, byteorder = "big"))]
    if largo % 36 == 0:
        iteraciones = largo // 36
    else:
        iteraciones = largo // 36 + 1
        for i in range(36 - (largo % 36)):
            mensaje.extend(b"\x00")
    for i in range(iteraciones):
        lista.append(bytearray((i + 1).to_bytes(length = 4, byteorder = "big")))
        lista.append(mensaje[i * 36: (i + 1) * 36])
    return lista
