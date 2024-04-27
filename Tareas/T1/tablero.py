from pieza_explosiva import PiezaExplosiva

class Tablero:
    def __init__(self, tablero: list) -> None:
        # filas         #columnas
        self.dimensiones = [len(tablero), len(tablero[0])]
        self.tablero = tablero


    @property
    def desglose(self) -> list:
        explosivas = 0
        peones = 0
        vacias = 0

        for i in self.tablero:
            for j in i:
                if "H" == j[0] or "R" == j[0] or "V" == j[0]:
                    explosivas += 1
                elif "PP" == j:
                    peones += 1
                else:
                    vacias +=1

        return [explosivas, peones, vacias]


    @property
    def peones_invalidos(self) -> int:
        suma_peones_invalidos = 0

        for i in range(self.dimensiones[0]):
            for j in range(self.dimensiones[1]):
                suma_vecinos = 0
                if self.tablero[i][j] == "PP":
                    if j - 1 >= 0: # vecino izquierdo
                        if self.tablero[i][j - 1] == "PP":
                            suma_vecinos += 1
                    if j + 1 < self.dimensiones[1]: # vecino derecho
                        if self.tablero[i][j + 1] == "PP":
                            suma_vecinos += 1
                    if i - 1 >= 0: # vecino superior
                        if self.tablero[i - 1][j] == "PP":
                            suma_vecinos += 1
                    if i + 1 < self.dimensiones[0]: # vecino inferior
                        if self.tablero[i + 1][j] == "PP":
                            suma_vecinos += 1
                    if suma_vecinos > 1:
                        suma_peones_invalidos += 1

        return suma_peones_invalidos


    @property
    def piezas_explosivas_invalidas(self) -> int:
        suma_expl_invalidas = 0

        for i in range(self.dimensiones[0]):
            for j in range(self.dimensiones[1]):
                if self.tablero[i][j][0] == "H":
                    if int(self.tablero[i][j][1:]) > self.dimensiones[1]:
                        suma_expl_invalidas += 1
                if self.tablero[i][j][0] == "V": 
                    if int(self.tablero[i][j][1:]) > self.dimensiones[0]:
                        suma_expl_invalidas += 1
                if self.tablero[i][j][0] == "R":
                    suma_dimensiones = self.dimensiones[0] + self.dimensiones[1]
                    alcance = min(self.dimensiones) + suma_dimensiones - 2
                    if int(self.tablero[i][j][1:]) > alcance:
                        suma_expl_invalidas +=1

        return suma_expl_invalidas


    @property
    def tablero_transformado(self) -> list:
        copia_tablero = self.tablero[:]

        for i in range (self.dimensiones[0]):
            for j in range (self.dimensiones[1]):
                pieza_type = copia_tablero[i][j][0]
                if pieza_type != "P" and pieza_type != "-":
                    alcance = self.tablero[i][j][1:]
                    copia_tablero[i][j] = PiezaExplosiva(int(alcance), pieza_type, [i, j])

        return copia_tablero

    def celdas_afectadas(self, fila: int, columna: int) -> int:
        altura = self.dimensiones[0]
        ancho = self.dimensiones[1]

        if self.tablero[fila][columna] == "PP" or self.tablero[fila][columna] == "--":
            return -1
        
        #Cada variable del tipo c_* determina cuantas casillas se pueden avanzar en esa direccion
        c_up = 0 #celdas afectadas hacia arriba
        i = fila
        if i >= 1:
            while i >= 1 and self.tablero[i - 1][columna] != "PP":
                c_up += 1
                i -= 1

        c_down = 0 #celdas afectadas hacia abajo
        i = fila
        if i < altura - 1:
            while i < altura - 1 and self.tablero[i + 1][columna] != "PP":
                c_down += 1
                i += 1

        vertical = c_up + c_down
        if self.tablero[fila][columna][0] == "V":
            return 1 + vertical # hay info suficiente para retornar V
        
        c_left = 0 #celdas afectadas hacia la izquierda
        i = columna
        if i >= 1:
            while i >= 1 and self.tablero[fila][i - 1] != "PP":
                c_left += 1
                i -= 1

        c_right = 0 #celdas afectadas hacia abajo
        i = columna
        if i < ancho - 1:
            while i < ancho - 1 and self.tablero[fila][i + 1] != "PP":
                c_right += 1
                i += 1

        horizontal = c_left + c_right
        if self.tablero[fila][columna][0] == "H":
            return 1 + horizontal # hay info suficiente para retornar H
        
        c_left_up = 0 # hacia izquierda arriba
        i = fila
        j = columna
        if i >= 1 and j >= 1:
            while i >= 1 and j >= 1 and self.tablero[i - 1][j - 1] != "PP":
                c_left_up += 1
                i -= 1
                j -= 1

        c_left_down = 0 # hacia izquierda abajo
        i = fila
        j = columna
        if i < altura - 1 and j >= 1:
            while i < altura - 1 and j >= 1 and self.tablero[i + 1][j - 1] != "PP":
                c_left_down += 1
                i += 1
                j -= 1

        c_right_up = 0 # hacia derecha arriba
        i = fila
        j = columna
        if i >= 1 and j < ancho - 1:
            while i >= 1 and j < ancho - 1 and self.tablero[i - 1][j + 1] != "PP":
                c_right_up += 1
                i -= 1
                j += 1

        c_right_down = 0 #hacia derecha abajo
        i = fila
        j = columna
        if i < altura - 1 and j < ancho - 1:
            while i < altura - 1 and j < ancho - 1 and self.tablero[i + 1][j + 1] != "PP":
                c_right_down += 1
                i += 1
                j += 1

        return 1 + vertical + horizontal + c_left_up + c_left_down + c_right_up + c_right_down

    def limpiar(self) -> int:
        for i in range(self.dimensiones[0]):
            for j in range(self.dimensiones[1]):
                if self.tablero[i][j] == "PP":
                    self.tablero[i][j] = "--"

    def reemplazar(self, nombre_nuevo_tablero: str) -> bool:
        abrir = open("tableros.txt", "r")
        tableros = abrir.readlines()
        abrir.close()

        for i in range(len(tableros)):
            tableros[i] = tableros[i].strip("\n").split(",")
            if tableros[i][0] == nombre_nuevo_tablero:
                self.tablero = []
                contador = 3
                self.dimensiones = [int(tableros[i][1]), int(tableros[i][2])]
                for j in range(int(tableros[i][1])):
                    self.tablero.append([])
                    for k in range(int(tableros[i][2])):
                        self.tablero[j].append(tableros[i][contador])
                        contador += 1
                return True
        return False


    def solucionar(self) -> list:
        #comprobamos si hay piezas explosivas invalidas
        print(self.piezas_explosivas_invalidas)
        if self.piezas_explosivas_invalidas!=0:
            return []

        celdas_vacias = [] # guardaremos la info de celdan en donde se pueda poner un peon.
        for i in range(self.dimensiones[0]):
            for j in range(self.dimensiones[1]):
                if self.tablero[i][j] == "--":
                    celdas_vacias.append([i, j])

        # probaremos todas las combinatorias de peones hasta encontrar una solucion.
        for i in range(2**len(celdas_vacias)):
            for j in range(len(celdas_vacias)):
                if not i % 2 ** (j+1) < 2 ** (j):
                    self.tablero[celdas_vacias[j][0]][celdas_vacias[j][1]] = "PP"
            # con esto habremos colocado todas las combinatorias de peones
            # verificar regla 1
            regla1 = True
            for j in range(self.dimensiones[0]):
                for k in range(self.dimensiones[1]):
                    if self.tablero[j][k][0] in ["V","H","R"]:
                        if int(self.tablero[j][k][1:]) != self.celdas_afectadas(j, k):
                            regla1 = False

            # regla 2 no se puede romper por como es el codigo

            # verificar regla 3
            regla3 = self.peones_invalidos == 0
            # restauramos tablero original
            retornable = []
            for j in range(self.dimensiones[0]):
                retornable.append([])
                for k in range(self.dimensiones[1]):
                    retornable[j].append(self.tablero[j][k])
            for j in range(len(celdas_vacias)):
                self.tablero[celdas_vacias[j][0]][celdas_vacias[j][1]] = "--"
            if regla1 and regla3:
                return retornable
        return []
    