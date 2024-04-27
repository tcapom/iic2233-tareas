from collections import Counter
from functools import reduce
from typing import Generator
from auxiliar import aux_titulo_mas_largo, aux_normalizar_fechas, key_entrada_0, key_entrada_3, \
                      aux_peli_mayor_rating, aux_genero_comun, aux_pond_fecha, aux_mayor_rating

def peliculas_genero(generador_peliculas: Generator, genero: str):
    #Filtra películas por género
    return filter(lambda x: x[2] == genero, generador_peliculas)

def personas_mayores(generador_personas: Generator, edad: int):
    #Filtra ´personas por edad
    return filter(lambda x: x[3] >= edad, generador_personas)

def funciones_fecha(generador_funciones: Generator, fecha: str):
    #Extraemos los carácteres de fecha para que estén en el mismo formato que en
    # el generador de funciones
    fecha = fecha[:6] + fecha[-2:]
    #Filtramos funciones por fecha
    return filter(lambda x: x[4] == fecha, generador_funciones)

def titulo_mas_largo(generador_peliculas: Generator) -> str:
    #Comparamos pares de películas para llegar a sólo una con el título más largo
    tupla_pelicula = reduce(lambda x, y: aux_titulo_mas_largo(x, y), generador_peliculas)
    return tupla_pelicula[1]

def normalizar_fechas(generador_funciones: Generator):
    #Cambiamos los formatos de cada fecha
    return map(aux_normalizar_fechas, generador_funciones)

def personas_reservas(generador_reservas: Generator):
    #Extraemos sin repetición todas las personas con reserva
    return {i[0] for i in generador_reservas}

def peliculas_en_base_al_rating(generador_peliculas: Generator, genero: str, 
                                rating_min: int, rating_max: int):
    #Filtramos las películas según las condiciones de género y rating
    return filter(lambda peli: peli[2] == genero and rating_min <= peli[3] <= rating_max
                  ,generador_peliculas)

def mejores_peliculas(generador_peliculas: Generator):
    lista_peliculas = [i for i in generador_peliculas]
    if len(lista_peliculas) < 20:
        #Retornamos inmediatamente si la cantidad de películas es inferior a 20
        return lista_peliculas
    #Filtramos las películas para que queden ordenadas según rating, y en caso de empate según id
    lista_peliculas.sort(key = key_entrada_0)
    lista_peliculas.sort(key = key_entrada_3)
    #Retornamos las 20 mejores según este órden
    return [lista_peliculas[i] for i in range(20)]

def pelicula_genero_mayor_rating(generador_peliculas: Generator, genero: str) -> str:
    #Usamos la función anteriormente definica de peliculas_genero
    generador_genero = peliculas_genero(generador_peliculas, genero)
    try:
        #Comparamos pares de películas hasta llegar a la de mayor rating
        tupla_pelicula = reduce(lambda x, y: aux_peli_mayor_rating(x, y), generador_genero)
    except TypeError:
        #Cuando el generador no tiene ninguna película
        return ""
    return tupla_pelicula[1]


def fechas_funciones_pelicula(generador_peliculas: Generator, 
                              generador_funciones: Generator, titulo: str):
    #Filtramos el generador de películas para encontrar la del título correcto
    peli = filter(lambda x: x[1] == titulo, generador_peliculas)
    lista_peli = [i for i in peli]
    if len(lista_peli) == 0:
        #Cuando el título asociado no tiene película disponible
        return (i for i in range(0))
    #Filtramos las funciones tal que el id de la película coincida
    lista_funciones = filter(lambda x: x[2] in lista_peli[0], generador_funciones)
    #Retornamos las fechas
    retornable = [funcion[4] for funcion in lista_funciones]
    return retornable

def genero_mas_transmitido(generador_peliculas: Generator, generador_funciones: Generator, 
                           fecha: str) -> str:
    #Usamos la función definida anteriormente de funciones_fecha para obtener
    # las funciones en la fecha correspondiente
    funciones_en_fecha = funciones_fecha(generador_funciones, fecha)
    lista_funciones = [i for i in funciones_en_fecha]
    if len(lista_funciones) == 0:
        #Retornamos inmediatamente si no hay funciones en la fecha
        return ""
    #Creamos una lista con cada id de cada función
    ids_validas_funciones = [x[2] for x in lista_funciones]
    #Creamos un diccionario que relacione ids con géneros
    dict_ids_a_genero = {i[0]: i[2] for i in generador_peliculas}
    #Creamos un diccionario tipo Counter para contar cada género
    counter_solo_generos = Counter([dict_ids_a_genero[i] for i in ids_validas_funciones])
    #Retornamos el género más común
    return [i for i in counter_solo_generos.most_common(1)][0][0]
    
def id_funciones_genero(generador_peliculas: Generator, 
                        generador_funciones: Generator, genero: str):
    #Filtramos las películas según el género deseado
    pelis_del_genero = filter(lambda x: x[2] == genero, generador_peliculas)
    #Usamos las ids de las películas del género para encontrar las funciones con el género
    ids_pelis_del_genero = [i[0] for i in pelis_del_genero]
    funciones_del_genero = filter(lambda x: x[2] in ids_pelis_del_genero, generador_funciones)
    #Retornamos las ids de las funciones
    return [i[0] for i in funciones_del_genero]

def butacas_por_funcion(generador_reservas: Generator, generador_funciones: 
                        Generator, id_funcion: int) -> int:
    #Encontramos la namedtuple según la id de la función 
    # (esto es reduntante, ya que ya tenemos la id deseada)
    gen_funcion = filter(lambda x: x[0] == id_funcion, generador_funciones)
    funcion = [i for i in gen_funcion][0]
    #Buscamos las butacas según la id de la función
    gen_butacas = filter(lambda x: x[1] == funcion[0], generador_reservas)
    #Retornamos la cantidad de butacas que nos sirven
    return len([i for i in gen_butacas])

def salas_de_pelicula(generador_peliculas: Generator, generador_funciones: Generator, 
                      nombre_pelicula: str):
    #Buscamos la namedtuple de la película deseada según su id
    gen_pelicula = filter(lambda x: x[1] == nombre_pelicula, generador_peliculas)
    pelicula = [i for i in gen_pelicula]
    if len(pelicula) == 0:
        #Si no existe la película, retornamos lista vacía
        return [i for i in range(0)]
    #Buscamos las funciones que tengan la misma id de película que nuestra película deseada
    gen_validas_funciones = filter(lambda x: x[2] == pelicula[0][0], generador_funciones)
    #Retornamos un generador con el número de cada sala válida
    gen_validas_salas = map(lambda x: x[1], gen_validas_funciones)
    return gen_validas_salas

def nombres_butacas_altas(generador_personas: Generator, generador_peliculas: Generator, 
                          generador_reservas: Generator, generador_funciones: Generator, 
                          titulo: str, horario: int):
    #Buscamos la película con el título deseado
    gen_pelis_titulo_bueno = filter(lambda x: x[1] == titulo, generador_peliculas)
    pelicula = [i for i in gen_pelis_titulo_bueno][0]
    #Buscamos las funciones que tengan la misma id de película que nuestra película deseada
    # y el horario deseado
    gen_validas_funciones = filter(lambda x: x[2] == pelicula[0] and x[3] == horario, 
                                   generador_funciones)
    #Hacemos una lista con las ids de las funciones deseadas
    ids_validas_funciones = [i[0] for i in gen_validas_funciones]
    #Filtramos las reservas según tengan la id de una función válida
    gen_validas_reservas = filter(lambda x: x[1] in ids_validas_funciones, generador_reservas)
    #Hacemos una lista con las ids de las personas de las reservas válidas
    ids_validas_personas = [i[0] for i in gen_validas_reservas]
    #Filtramos las personas según tengan su id en la lista anterior
    personas_validas = filter(lambda x: x[0] in ids_validas_personas, generador_personas)
    #Retornamos un set para borrar nombres repetidos
    return {i[1] for i in personas_validas}

def nombres_persona_genero_mayores(generador_personas: Generator, generador_peliculas: Generator,
                                   generador_reservas: Generator, generador_funciones: Generator,
                                   nombre_pelicula: str, genero: str, edad: int):
    #Buscamos la id de la película a la cual se nos brinda su título
    gen_pelis_titulo_bueno = filter(lambda x: x[1] == nombre_pelicula, generador_peliculas)
    pelicula = [i for i in gen_pelis_titulo_bueno][0]
    #Buscamos las ids de las funciones que contengan la id de la película deseada
    gen_validas_funciones = filter(lambda x: x[2] == pelicula[0], generador_funciones)
    ids_validas_funciones = [i[0] for i in gen_validas_funciones]
    #Buscamos las ids de las personas que tengan una reserva para las funciones deseadas
    gen_validas_reservas = filter(lambda x: x[1] in ids_validas_funciones, generador_reservas)
    ids_validas_personas = [i[0] for i in gen_validas_reservas]
    #Filtramos las personas según su edad y género
    personas_validas = filter(lambda x: x[0] in ids_validas_personas and x[3] >= edad 
                              and x[2] == genero, generador_personas)
    #Retornamos un set para borrar nombres repetidos
    return {i[1] for i in personas_validas}

def genero_comun(generador_personas: Generator, generador_peliculas: Generator, 
                 generador_reservas: Generator, generador_funciones: Generator, 
                 id_funcion: int) -> str:
    #Buscamos las ids de las personas con reservas en la función con la id_funcion brindada
    gen_validas_reservas = filter(lambda x: x[1] == id_funcion, generador_reservas)
    ids_validas_personas = [i[0] for i in gen_validas_reservas]
    #Buscamos las namedtuples de las personas con las ids de personas válidas
    personas_validas = filter(lambda x: x[0] in ids_validas_personas, generador_personas)
    lista_personas_validas = [i for i in personas_validas]
    #Buscamos la id de la película deseada con la id de la función
    gen_funcion_id_buena = filter(lambda x: x[0] == id_funcion, generador_funciones)
    id_pelicula = [i[2] for i in gen_funcion_id_buena][0]
    #Buscamos el título de la película deseada con la id de la película
    gen_peli_id_buena = filter(lambda x: x[0] == id_pelicula, generador_peliculas)
    titulo = [i[1] for i in gen_peli_id_buena][0]
    #Llamamos a aux_genero_comun que se encarga de retornar una lista con 
    # el o los géneros más comunes
    mas_comunes = aux_genero_comun(lista_personas_validas)
    #Imprimimos el mensaje adecuado según la cantidad de argumentos
    if len(mas_comunes) == 1:
        return "En la función " + str(id_funcion) + " de la película " + titulo + \
        " la mayor parte del público es " + mas_comunes[0] + "."
    if len(mas_comunes) == 2:
        return "En la función " + str(id_funcion) + " de la película " + titulo + \
        " se obtiene que la mayor parte del público es de " + mas_comunes[0] + " y " + \
        mas_comunes[1] + " con la misma cantidad de personas."
    return "En la función " + str(id_funcion) + " de la película " + titulo + \
    " se obtiene que la cantidad de personas es igual para todos los géneros."

def edad_promedio(generador_personas: Generator, generador_peliculas: Generator, 
                  generador_reservas: Generator, generador_funciones: Generator, 
                  id_funcion: int) -> str:
    #Buscamos la id de la película correspondiente a id_función
    gen_funcion_id_buena = filter(lambda x: x[0] == id_funcion, generador_funciones)
    id_pelicula = [i[2] for i in gen_funcion_id_buena][0]
    #Buscamos el título de la película correspondiente a id_pelicula
    gen_peli_id_buena = filter(lambda x: x[0] == id_pelicula, generador_peliculas)
    titulo = [i[1] for i in gen_peli_id_buena][0]
    #Creamos la lista de ids de personas que asistieron a id_funcion
    gen_validas_reservas = filter(lambda x: x[1] == id_funcion, generador_reservas)
    ids_validas_personas = [i[0] for i in gen_validas_reservas]
    #Creamos una lista con las edades de las personas con reserva a la función
    personas_validas = filter(lambda x: x[0] in ids_validas_personas, generador_personas)
    lista_edades_validas = [i[3] for i in personas_validas]
    #Calculamos el promedio de edades
    promedio = reduce(lambda x, y: x + y, lista_edades_validas) / len(lista_edades_validas)
    if promedio % 1 != 0:
        #Aproximamos hacia arriba en caso de decimal
        promedio = promedio + 1
    #Eliminamos los decimales
    promedio = int(promedio)
    #Retornamos el mensaje pertinente
    return "En la función " + str(id_funcion) + " de la película " + titulo + \
    " la edad promedio del público es " + str(promedio) + "."

def obtener_horarios_disponibles(generador_peliculas: Generator, generador_reservas: Generator,
                                 generador_funciones: Generator, fecha_funcion: str, 
                                 reservas_maximas: int):
    lista_reservas = [i for i in generador_reservas]
    #Creamos una lista con todas las funciones en una fecha específica
    funciones_en_fecha = [i for i in filter(lambda x: x[4] == fecha_funcion, generador_funciones)]
    #Revisamos para cada función en la fecha si es que la cantidad de reservas es menor a las
    # reservas máximas
    funciones_con_espacio = filter(lambda x: reduce(lambda y, z: y + 1 if z[1] == x[0] else y, 
                                                    lista_reservas, 0) < reservas_maximas,
                                                    funciones_en_fecha)
    lista_validas_funciones = [i for i in funciones_con_espacio]
    if len(lista_validas_funciones) == 0:
        #Si no hay funciones válidas retornamos inmediatamente una lista vacía
        return [i for i in range(0)]
    #Llamamos a aux_mayor_rating para que retorne las ids de las películas con mayor
    # rating entre las funciones válidas
    lista_peliculas = [i for i in generador_peliculas]
    ids_max_rating = aux_mayor_rating(lista_validas_funciones,lista_peliculas)
    #Retornamos un set con los horarios de las funciones válidas que tengan el mayor rating
    return {i[3] for i in filter(lambda x: x[2] in ids_max_rating, lista_validas_funciones)}
    
def personas_no_asisten(generador_personas: Generator, generador_reservas: Generator,
                        generador_funciones: Generator, fecha_inicio: str, fecha_termino: str):
    #Usamos un ponderador para darle un valor entero a la fecha de inicio y la de término
    pond_inicio = aux_pond_fecha(fecha_inicio)
    pond_termino = aux_pond_fecha(fecha_termino)
    #Buscamos las ids de las funciones que tengan su emisión durante las fechas
    gen_funciones_validas = filter(lambda x: pond_inicio <= aux_pond_fecha(x[4]) <= pond_termino,
                                   generador_funciones)
    ids_validas_funciones = [i[0] for i in gen_funciones_validas]
    #Buscamos las reservas que contengan las ids de las funciones válidas
    gen_validas_reservas = filter(lambda x: x[1] in ids_validas_funciones, generador_reservas)
    ids_validas_personas = [i[0] for i in gen_validas_reservas]
    #Creamos una lista con todas las personas que asistieron a alguna de las funciones válidas
    lista_total_personas = [i for i in generador_personas]
    personas_asistentes = filter(lambda x: x[0] in ids_validas_personas, lista_total_personas)
    lista_personas_asistentes = [i for i in personas_asistentes]
    #Retornamos las personas que no pertenecen a la lista anterior
    personas_no_asistentes = filter(lambda x: not x in lista_personas_asistentes,
                                    lista_total_personas)
    return personas_no_asistentes
