# Tarea 2: DCConejoChico 🐇💨


## Consideraciones generales :octocat:

Como resumen, los únicos elementos que no están presentes en la tarea es la implementación de los dos tipos de bombas, la recolección de estas, y animaciones "fluidas" (sí hay intercalación de sprites). En la seción de cosas implementadas y no implementadas se hará una revisión medianamente exhaustiva de cada punto de la rúbrica, con tal de facilitar la corrección.

Además, se hablará repetidamente del atributo ```self.user_data```, que pertenece a la clase ```LogicaJuego```. Este almacena la distinta información importante para el usuario en forma de lista, con formato de ```[username, nivel, score_acumulado, vidas, *poderes]```.

### Cosas implementadas y no implementadas :white_check_mark: :x:
- ❌ Incompleto
- 🟠 Faltó implementar la animación continua
- ✅ Totalmente completo

#### Entrega Final: 46 pts (75%)
##### ✅ Ventana Inicio
La ventana de inicio es completamente funcional
- ✅Los elementos se pueden ver con claridad, aunque la estética sea claramente fea 😭. IMPORTANTE: la distribución de la ventana se puede romper dependiendo cómo se modifique ```puntaje.txt```. Mas detalles en la observación #1
- ✅Las vadilaciones de los criterios de nombre de usuario se realizan llamando a la función ```validacion_formato``` en la línea 63 de la ventana de login. Para revisar si un usuario está baneado, el servidor lo procesa en ```main.py``` entre las líneas 33 y 41.
- ✅Ocupar el botón de salir cierra el programa usando ```sys.exit()```, tal que si hay otras ventanas abiertas presentes (como la de usuario baneado, etc), estas serán cerradas también.
##### ✅ Ventana Juego
 Los elementos mínimos de la ventana de juego son completamente funcionales.
- ✅Entre la línea 43 y 51 de ```logica_juego``` se carga y guarda el mapa dependiendo el nivel. En la línea 51 se envía esta información a ```ventana_juego```
- ✅Se cargan todos los elementos correctamente, donde se llama primero a ```background_tablero``` en ```ventana_juego``` para crear el fondo, y posteriormente se llama a ```spawnear_entes```, para que el jugador y enemigos estén por encima del fondo
- ✅En las líneas 78 a 90 de ```logica_conexion``` se hacen los cálculos correspondientes para el número de vidas con que se ingresa.
- ✅Al manipular la información de ```self.user_data``` de ```LogicaJuego```, se hacen y guardan entre niveles los distintos cálculos para el puntaje y vidas, mientras que el tiempo se actualiza con el método ```pasar_seg```. En la ventana de juego, los métodos```pasar_seg```, ```actualizar_vidas```, y ```actualizar_scores``` reciben señales para mostrar la información visualmente.
- ✅Ocupar el botón de salir cierra el programa usando ```sys.exit()```, tal que si hay otras ventanas abiertas presentes (como la de usuario baneado, etc), estas serán cerradas también.
##### 🟠 ConejoChico
- ✅ Los métodos que empiezan con "```mover_```" para ```LogicaJuego``` realizan los cálculos correspondientes para detectar colisiónes. El método ```perder_vida``` decide qué hacer en caso de colisión
- 🟠 Los métodos ```empezar_movimiento_conejo``` y ```mover_conejo``` en la lógica de juego utilizan un lock para impedir que el conejo pueda cambiar de dirección una vez se empezó a mover a una dirección. El método ```intercalar_conejo``` permite intercambiar los distintos sprites que tiene. Lo que faltó implementar fue el movimiento fluído entre una casilla y otra
- ❓Tal como declara la issue #350, el aumento de velocidad debería ser para los lobos.
- ✅ Las teclas para movimiento, pausa y cheatcodes están correctamente asignadas y funcionan independiente de si se ocupa la mayúscula o minúscula de cada tecla. La detección de teclas está en el método ```keyPressEvent``` de la ventana de juego.
- ✅ El método ```pasar_seg``` emite la señal de pérdida de vida en caso de que se acabe el tiempo
##### 🟠 Lobos
- 🟠 Entre las líneas 91 y 98 cada lobo es instanciado como su propio objeto y agregado a la lista de entes del nivel para que cada uno pueda realizar sus propios cálculos (estos cálculos también consideran la velocidad creciente por nivel). Con respecto a su movimiento, falta agregar el movimiento continuo.
- ✅ Los lobos horizontales y los lobos verticales tienen cada uno su propia clase en ```logica_entes``` que presentan métodos de mismo nombre pero con distinta funcionalidad dependiendo su dirección individual.
##### 🟠 Cañón de Zanahorias
- ✅ El método ```spawnear_zanahorias``` en la lógica del juego genera las zanahorias con parámetros correctos dependiendo de los parámetros del cañón.
- 🟠 Cada zanahoria funciona de manera independiente al instanciarse cada una como su propio objeto en la línea 133 de ```logica_juego```. Con respecto a su movimiento, falta agregar el movimiento continuo.
##### ❌ Bomba Manzana
- ❌ La funcionalidad de la bomba de manzana no está presente. Existen ciertos elementos como la existencia de los objetos ```LogicaAppleNormal``` y ```SpriteAppleNormal``` que permitirían la implementación de sus funcionalidades, además que el formato de ```self.user_data``` permitiría su conservación entre niveles.
##### ❌ Bomba Congeladora
- ❌ Refiérase al punto anterior de Bomba Manzana.
##### ✅ Fin del nivel
- ✅ En ```LogicaJuego```, los métodos ```perder_vida``` y ```pasar_nivel``` modifican la información de ```self.user_data``` y vuelven a cargar el nivel con ```cargar_nivel```.
- ✅ La señal ```senal_guardar_score``` de la lógica del juego emite una señal con ```self.user_Data``` a ```guardar_score``` de ```LogicaConexion``` para guardar en el servidor la nueva información del usuario.
- ✅ Las líneas 62 hasta la 90 del main del servidor almacenan la información enviada desde el cliente para sobreescribir puntajes de jugadores ya existentes o añadirlos en caso de que no estén.
##### ✅ Fin del Juego
- ✅ Las señales ```senal_cero_vidas``` y ```senal_pasar_juego``` en caso de derrota o victoria respectivamente activarán las ventanas y sonidos correspondientes.
##### ❌ Recoger (G)
- ❌ Absolutamente no implementado.
##### ✅ Cheatcodes (Pausa, K+I+L, I+N+F)
Para los cheats que ocupan una sucesión de teclas, está el atributo ```current_sequence``` de la ventana de juego, el cual guarda las últimas tres teclas presionadas
- ✅ La pausa funciona correctamente y detiene todos los timers presentes. Existe un detalle con los cañones presente en la observación #6.
- ✅ El cheat KIL eliminará a todos los lobos y zanahorias, mientras que también pausa los cañones eternamente, eliminando así los enemigos presentes y los que se pueden generar. Aparecerán perfectamente los enemigos del siguiente nivel y volverán a aparecer en el mismo si por alguna razón pierdes por tiempo (XD?).
- ✅ el cheat INF modifica el atributo ```inf_activo``` de la lógica de juego para impedir la pérdida de vidas y tiempo, aparte de otorgar su puntaje. Se puede activar y desactivar tal como se indica en la observación #4.
##### ✅ Networking
- ✅ Siempre que se crea un socket se ocupa los parámetros AF_INET y SOCK_STREAM.
- ✅ Se crean threads en el servidor, tal que se puedan conectar múltiples clientes y no se atraviese la información.
- ✅ Las líneas 56 a 59 en ```logica_conexion``` notifican al usuario de la pérdida de conexión con el servidor.
- ✅ Cliente y servidor funcionan completamente aparte. Se detalla más en la observación 7.
- ✅ Se ocupan locks para cuando se abre el archivo ```puntajes.txt```, para que un thread del servidor no lo ocupe si otro está modificando su información.
- ✅ Se ocupan logs para indicar: cuando un cliente se conecta, cuando un cliente se desconecta, cuando un usuario logra hacer login, cuando un usuario pasa de nivel, y cuando un usuario supera el último nivel. Cuando es pertinente, aparece el puntaje del usuario.
- ✅ Aparecerá un mensaje de error en caso de que no se ingrese puerto como argumento a la consola. Si el cliente ingresa un puerto, pero este es incorrecto (o el server no está activo), también se notificará.

##### ✅ Decodificación
- ✅ En la línea 55 de ```logica_conexion``` y en la 20 del ```main.py``` del servidor, se espera siempre que llegue primero un mensaje de largo 4. Este posteriormente se decodifica usando la función ```obtener_int``` declarada en ambos ```aux_cliente``` y ```aux_servidor```.
- ✅ En las líneas 62 a 67 de ```logica_conexion``` y en las 26 a 31 del ```main.py``` del servidor, se recibe el mensaje en chunks. Los bytes de relleno los elimina la función ```decodificar_mensaje``` de ```aux_cliente``` y ```aux_servidor```.
##### ✅ Desencriptación
- ✅ La función ```decodificar_mensaje``` de ```aux_cliente``` y ```aux_servidor``` logra decodificar correctamente la totalidad del mensaje.
##### ✅ Archivos
- ✅ Los pocos archivos que no se ocupan (con su justificación) son los siguientes
  - ```conejo.png```: es el mismo sprite que ```conejo_abajo_1.png```, que sí se utiliza
  - ```explosion.png```, ```congelacion_burbuja.png```, y ```congelacion.png```: no se implementó los efectos de las manzanas.
  - ```victoria.mp3``` y ```derrota.mp3```: se usó su contraparte de ```.wav```.
##### ✅ Funciones
- Tal como se declara en la issue #319, se pueden reestructurar las funciones de la entrega intermedia y con eso considerar que se usan, pudiendo haber una faltante. Acá se detalla su uso/reestructuración.
  - ```separar_mensaje```: es llamada por ```encriptar_mensaje```
  - ```serializar_mensaje```, ```encriptar_mensaje```, y ```codificar_mensaje```: son llamadas por ```decodificar_mensaje``` de ```aux_cliente``` y ```aux_servidor```.
  - ```usuario_permitido```: en la línea 23 del ```main.py``` del servidor
  - ```validacion_formato``` llamado por ```click_ingresar``` de ```VentanaLogin```
  - ```riesgo_mortal``` y ```validar_dirección```: se reestructuran en ```mover_conejo_posible``` y ```mover_enemigo``` de ```aux_cliente```
  - ```calcular_puntaje```: línea 332 de ```ventana_login```
- La única función que no se utiliza ni se rescatan elementos de ella es ```usar_item``` (por la no implementación de las manzanas).

## Ejecución :computer:
El cliente puede ingresar al programa ingresando a ```main.py``` desde la carpeta ```cliente```, añadiendo un argumento de consola correspondiente al puerto desde el que se abrió el server. Por esto mismo, el servidor tiene que estar abierto antes que el cliente ingresando a ```main.py``` desde la carpeta ```servidor```, añadiendo como argumento el puerto que se quiere abrir para la conexión. En caso de que se deseen conectar clientes y servidores que estén en distintos computadores, entonces el archivo ```server_ip.json``` presente tanto en la carpeta ```cliente``` como en ```servidor``` tienen que tener la ip que va a usar el servidor.

Es de suma importancia colocar la carpeta ```assets/``` dentro de la carpeta inmediata de ```cliente/```. En caso de querer tenerla en otra posición, se tendrán que cambiar los paths que aparecen en ```parametros.py``` y ```sprites_entes.py```.

El cliente tiene la siguiente estructura:
- Carpeta base
  - ``main.py``
  - ``aux_cliente.py``
  - ``funciones_cliente.py``
  - ``funciones_servidor.py``
  - ``parametros.py``
  - ``assets/``
  - ``server_ip.json``
- backend
  - ``logica_conexion.py``
  - ``logica_entes.py``
  - ``logica_juego.py``
- frontend
  - ``reproductor.py``
  - ``sprites_entes.py``
  - ``ventana_juego.py``
  - ``ventana_login.py``

El servidor tiene la siguiente estructura:
- Carpeta base
  - ``main.py``
  - ``aux_servidor.py``
  - ``funciones_servidor.py``
  - ``bloqueados.txt``
  - ``puntaje.txt``
  - ``server_ip.json``

## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```socket```
2. ```sys```
3. ```json```
4. ```threading```
5. ```PyQt6```
6. ```os```

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:
1. ```funciones_servidor```: funciones para  ```aux_servidor```.
2. ```aux_servidor```: funciones para encriptar y desencriptar.
3. ```funciones_cliente```: funciones para ```aux_cliente```.
4. ```aux_cliente```: funciones de ```aux_servidor```, más otras para realizar cálculos reiterativos del backend.
5. ```backend.logica_entes```: lógica individual para cada entidad del juego.
6. ```backend.logica_conexion```: lógica para la conexión con el servidor y con la ventana de login.
7. ```backend.logica_juego```: lógica para la ventana principal del juego.
8. ```frontend.sprites_entes```: sprites para cada entidad del juego.
9. ```frontend.reproductor```: reproductor de archivos de sonido.
10. ```frontend.ventana_juego```: ventana principal del juego.
11. ```frontend.ventana_login```: resto de ventanas necesarias.

## Observaciones :thinking:
En caso de que te hayas saltado mi maravillosa revisión exhaustiva, considerar por favor las siguientes observaciones.

1. Recalco que es importante que el archivo ```puntaje.txt``` tenga al menos 5 jugadores con la información en su formato correcto. De no ser así, la ventana de login es inutilizable. Mientras se siga su formato, se puede modificar a discresión
2. Como la frecuencia de disparo del cañón no está especificada, decidí arbitrariamente que su frecuencia fuera  ```VELOCIDAD_ZANAHORIA/20```
3. El spawn del conejo será siempre en la casilla de Conejo, tal como se permitió en la issue #307.
4. Tal como se permitió en la issue #358, El cheatcode INF puede permanecer entre niveles. Por esta razón decidí implementarlo como un switch, osea se puede activar y desactivar usando la sucesión de teclas.
5. Como las bombas no están implementadas, las únicas maneras de conseguir puntaje serán superando el nivel habiendo usado cualquiera de los dos cheatcodes. En cualquier caso, los cálculos correspondientes están presentes de las líneas 327 a 334 en ```logica_juego```.
6. Como el botón de pausa detiene a todos los timers, cuando se reanudan, estos timers empiezan desde cero, por lo que es posible abusar del botón para que el cañón de zanahorias nunca dispare.
7. Varios archivos fueron movidos de posición, tal que si uno toma las carpetas del cliente y servidor y las arrastra a cualquier directorio, estas puedan ser ejecutadas de manera completamente independiente. Para esto, me basé en la issue #258 y dupliqué el archivo de ```funciones_cliente.py``` y lo coloqué en la carpeta ```cliente```, mientras que el archivo ```funciones_servidor.py``` se encuentra tanto en la carpeta ```cliente``` y ```servidor```
8. En caso de que se ejecute el cliente y servidor desde dos computadores distintos, se tiene que modificar ```server_ip.json``` para contener la nueva IP del servidor.
9. El archivo ```bloqueados.txt``` se puede modificar mientras mantenga el mismo formato. Se pueden tener usuarios bloqueados que no cumplan las características del formato de validación, pero a estos sólo aparecería el error de formato de validación.
10. El hall de la fama mostrará los 5 mejores puntajes independiente del último nivel al que hayan llegado, por lo que un jugador podría aún no terminar el juego y aparecer en el hall de otro jugador si tiene suficiente puntaje
11. De la manera en que está implementada la "muerte" de los enemigos, simplemente oculta los sprites que tiene, pero estos objetos seguirán existiendo dentro del atributo ```lista_entes``` de la ventana de juego y la lógica del juego. Es por esto que si se activa el cheatcode INF y se deja correr el juego por un tiempo indefinidamente largo, este pueda empezarse a lagear. Aún así, no lo he intentado comprobar, por lo que no puedo dar un estimado de cuanto tiempo debería pasar para que fuera notorio.

PD: < Gracias >


-------


