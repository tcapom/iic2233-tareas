def validacion_formato(nombre:str) -> bool:
    if not nombre.isalnum():
        return False
    if len(nombre) < 3 or len(nombre) > 16:
        return False
    num_condition = False
    caps_condition = False
    for i in nombre:
        if i in "1234567890":
            num_condition = True
        if i in "QWERTYUIOPASDFGHJKLZXCVBNM":
            caps_condition = True
    if num_condition and caps_condition:
        return True
    return False

def riesgo_mortal(laberinto: list[list]) -> bool:
    for i in range(len(laberinto)):
        for j in range(len(laberinto)):
            if laberinto[i][j] == "C":
                y_pos = i
                x_pos = j
    wall_bump = False
    steps = 1
    while not wall_bump: #verificar hacia abajo
        casilla_evaluada = laberinto[y_pos + steps][x_pos]
        if casilla_evaluada in ["LV", "CU"]:
            return True
        elif casilla_evaluada in ["E", "S", "P", "CD", "CL", "CR"]:
            wall_bump = True
        steps += 1
    wall_bump = False
    steps = 1
    while not wall_bump: #verificar hacia arriba
        casilla_evaluada = laberinto[y_pos - steps][x_pos]
        if casilla_evaluada in ["LV", "CD"]:
            return True
        elif casilla_evaluada in ["E", "S", "P", "CU", "CL", "CR"]:
            wall_bump = True
        steps += 1
    wall_bump = False
    steps = 1
    while not wall_bump: #verificar hacia la derecha
        casilla_evaluada = laberinto[y_pos][x_pos + steps]
        if casilla_evaluada in ["LH", "CL"]:
            return True
        elif casilla_evaluada in ["E", "S", "P", "CD", "CU", "CR"]:
            wall_bump = True
        steps += 1
    wall_bump = False
    steps = 1
    while not wall_bump: #verificar hacia la izquierda
        casilla_evaluada = laberinto[y_pos][x_pos - steps]
        if casilla_evaluada in ["LH", "CR"]:
            return True
        elif casilla_evaluada in ["E", "S", "P", "CD", "CU", "CL"]:
            wall_bump = True
        steps += 1
    return False


def usar_item(item: str, inventario: list) -> tuple[bool, list]:
    if item in inventario:
        inventario.remove(item)
        return (True, inventario)
    return (False, inventario)


def calcular_puntaje(tiempo: int, vidas: int, cantidad_lobos: int, PUNTAJE_LOBO: int) -> float:
    if cantidad_lobos == 0:
        return float(0)
    return round((tiempo * vidas)/(cantidad_lobos * PUNTAJE_LOBO), 2)


def validar_direccion(laberinto: list[list], tecla: str) -> bool:
    for i in range(len(laberinto)):
        for j in range(len(laberinto)):
            if laberinto[i][j] == "C":
                if tecla == "S":
                    if laberinto[i + 1][j] in ["P", "CU", "CD", "CL", "CR"]:
                        return False
                if tecla == "W":
                    if laberinto[i - 1][j] in ["P", "CU", "CD", "CL", "CR"]:
                        return False
                if tecla == "A":
                    if laberinto[i][j - 1] in ["P", "CU", "CD", "CL", "CR"]:
                        return False
                if tecla == "D":
                    if laberinto[i][j + 1] in ["P", "CU", "CD", "CL", "CR"]:
                        return False
                return True
