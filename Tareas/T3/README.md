# Tarea 3: DCCine 🎬🎥


## Consideraciones generales :octocat:

Todo funciona a la perfección. Espero no haberme equivocado al crear las estructuras por compresión 🙂

### Cosas implementadas y no implementadas :white_check_mark: :x:


####  Programación funcional
##### ✅ Utiliza 1 generador
##### ✅ Utiliza 2 generadores
##### ✅ Utiliza 3 o más generadores
####  API
##### ✅ Obtener información
##### ✅ Modificar información

## Ejecución :computer:
No existe módulo directo de ejecución para la tarea. Es necesario añadir un archivo adicional que utilice las distintas funciones existentes en ```consultas.py``` y ```peli.py``` para comprobar su buen funcionamiento.


## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```Collections```: ```Counter```
2. ```functools```: ```reduce```
3. ```requests```: ```get```, ```post```, ```patch```, ```delete```
4. ```api```
5. ```typing```: ```Generator```

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

- ```consultas```: Contiene a las funciones exigidas por el enunciado para extraer información al tener información de namedtuples y otros argumentos. Cada función extensa tiene comentado su paso a paso de qué se hace. La utilidad de cada función aparece descrita en el enunciado
- ```auxiliar```: Contiene a distintas funciones auxiliares que son utilizadas en ```consultas.py```. Cada función tiene descrito lo que retorna dentro del mismo ```auxiliar.py```.
- ```peli```: Contiene a la clase ```Peliculas``` con sus atributos y métodos exigidos por el enunciado para interactuar con la API. La utilidad de cada método aparece descrito en el enunciado

## Consideraciones adicionales :thinking:
Las consideraciones que tuve durante la tarea son las siguientes:

1. Tal como declara la issue #429, para el test_04 (dentro de la función aux_normalizar_fechas) se pueden crear namedtuples por comprensión.
2. Tal como declara la issue #410, se pueden crear estructuras datos vacías usando compresión
3. Tal como declara la issue #410 y #444, para se pueden crear diccionarios del tipo Counter y crear una lista usando most_common()




## Descuentos
La guía de descuentos se encuentra [link](https://github.com/IIC2233/Syllabus/blob/main/Tareas/Bases%20Generales%20de%20Tareas%20-%20IIC2233.pdf).