from utilidades import Funciones, Peliculas
from collections import Counter

def aux_titulo_mas_largo(x: Peliculas, y: Peliculas) -> Peliculas:
    '''
    Para Test 03. Se encarga de comparar las tuplas de las películas "x" e "y", retornando una
    película según si tiene el título más largo, sino se retorna por tener id más grande.
    '''
    if len(x[1]) > len(y[1]):
        return x
    if len(x[1]) < len(y[1]):
        return y
    if x[3] > y[3]:
        return x
    return y


def aux_normalizar_fechas(x) -> Funciones:
    '''
    Para test 04. Crea las nuevas namedtuples del tipo Funciones, cambiando el formato de la 
    fecha al llamar a subaux_normalizar_fechas.
    '''
    new_namedtuple = Funciones(*(subaux_normalizar_fechas(i) for i in x))
    return new_namedtuple

def subaux_normalizar_fechas(x: str) -> str:
    '''
    Para test 04. Toma un argumento y si este es un string,
    hace la conversión de DD-MM-AA a AAAA-MM-DD.
    '''
    if type(x) == int:
        return x
    if int(x[-2:]) >= 24:
        new_fecha = "19" + x[-2:] + "-" + x[3:5] + "-" + x[:2]
    else:
        new_fecha = "20" + x[-2:] + "-" + x[3:5] + "-" + x[:2]
    return new_fecha

def key_entrada_0(x):
    '''
    Para test 07. key para sort tal que ordena por la primera entrada de la tupla
    '''
    return x[0]

def key_entrada_3(x):
    '''
    Para test 07. key para sort tal que ordena por la primera entrada de la tupla
    '''
    return x[3] * -1

def aux_peli_mayor_rating(x: Peliculas, y: Peliculas) -> Peliculas:
    '''
    Para Test 08. Se encarga de comparar las tuplas de las películas "x" e "y", retornando
    cual tiene mayor rating, sino la que esté más a la izquierda"
    '''
    if x[3] < y[3]:
        return y
    return x

def aux_genero_comun(lista_personas_validas):
    '''
    Para test 16. Recibe una lista de personas y calcula 
    cual o cuales son los géneros más comunes.
    '''
    counter_generos =  Counter([i[2] for i in lista_personas_validas])
    valor_mas_alto = max([i for i in counter_generos.values()])
    generos_mas_comunes = filter(lambda x: counter_generos[x] == valor_mas_alto, counter_generos)
    return [i for i in generos_mas_comunes]

def aux_mayor_rating(funciones, peliculas):
    '''
    Para test 18
    '''
    id_peliculas = {i[2] for i in funciones}
    peliculas_validas = [i for i in filter(lambda x: x[0] in id_peliculas, peliculas)]
    lista_ratings = [i[3] for i in peliculas_validas]
    print(lista_ratings)
    max_rating = max(lista_ratings)
    return [i[0] for i in filter(lambda x: x[3] == max_rating, peliculas_validas)]


def aux_pond_fecha(fecha: str):
    '''
    Para test 19. Utiliza un ponderador para darle un valor entero a cada fecha. Este valor se
    calcula tal que <ano * 372 + mes * 31 + dia>, lo cual cuando el objetivo es simplemente
    comparar qué día va antes o después, sirve.
    '''
    dia = int(fecha[:2])
    mes = int(fecha[3:5])
    ano = int(fecha[-2:])
    if ano < 24:
        ano += 100
    return ano * 372 + mes * 31 + dia