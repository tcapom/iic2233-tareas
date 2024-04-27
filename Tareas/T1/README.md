# Tarea 1: DCChexxploding 💥♟️


## Consideraciones generales :octocat:

El uso de ```tablero.solucionar``` busca todas las combinatorias de peones posibles en los espacios vacíos hasta encontrar una válida, por lo que cada recuadro vacío presente adicional duplica el tiempo máximo de búsqueda de solución. Como referencia, una matriz que no tiene solución y con 17 celdas vacías me demoró alrederor de 5 segundos, mientras con 22 se demoró 3 minutos.

### Cosas implementadas y no implementadas :white_check_mark: :x:
Por lo percibido, se pudo implementar todo lo pedido correctamente
#### Menú: 18 pts (30%)
##### ✅ Consola
##### ✅ Menú de Acciones
##### ✅ Modularización
- No fue necesaria la creación de otros archivos adicionales a los del enunciado para cumplir la modularización
##### ✅ PEP8


## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```main.py```.

## Librerías :books:
### Librerías externas utilizadas
La librería externa que utilicé fue la siguiente:

1. ```sys```: ```argv```,```close```

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```tablero```: Contiene a la clase ```Tablero```
2. ```pieza_explosiva```: contiene a la clase ```PiezaExplosiva```
3. ```imprimir_tablero```: contiene la función ```imprimir_tablero```

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. Se asume que en la consola se recibe un argumento para el nombre de usuario y otro para el nombre del tablero, no más ni menos. Esto aparece en el enunciado en la parte 3.2.
2. Se asume que para los nombres de usuario, la ñ no se considera parte del alfabeto, ya que en programación se considera el abecedario en inglés.



-------
