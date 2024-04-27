class PiezaExplosiva:
    def __init__(self, alcance: int, tipo: str, posicion: list) -> None:
        self.alcance = alcance
        self.tipo = tipo
        self.posicion = posicion

    def __str__(self) -> str:
        fila, columna = self.posicion
        texto = f"Soy la pieza {self.tipo}{self.alcance}\n"
        texto += f"\tEstoy en la fila {fila} y columna {columna}\n"
        return texto

    def verificar_alcance(self, fila: int, columna: int) -> bool:
        if self.tipo == "H":
            if self.posicion[0] == fila:
                return True
        if self.tipo == "V":
            if self.posicion[1] == columna:
                return True
        if self.tipo == "R":
            if self.posicion[1] == columna or self.posicion[0] == fila:
                return True
            if abs(self.posicion[1] - columna) == abs(self.posicion[0] - fila):
                return True
        return False



if __name__ == "__main__":
    """
    Ejemplos:

    Dado el siguiente tablero
    [
        ["--", "V2", "PP", "--", "H2"],
        ["H3", "--", "--", "PP", "R11"]
    ]

    """
    # Ejemplo 1 - Pieza R11
    pieza_1 = PiezaExplosiva(11, "R", [1, 4])
    print(str(pieza_1))

    # Ejemplo 2 - Pieza V2
    pieza_2 = PiezaExplosiva(2, "V", [0, 1])
    print(str(pieza_2))
