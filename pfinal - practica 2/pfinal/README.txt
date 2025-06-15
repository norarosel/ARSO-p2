README:
COSAS IMPORTANTES A TENER EN CUENTA SOBRE EL FUNCIONAMIENTO DE CÓDIGO:

Cuando el usuario quiera ejecutar la orden "CREAR":

1.Primero se borrará el lxdbr0 que se crea por defecto y luego se volverá a crear, de esa manera evitamos fallos de asignación de ipv4.
2.Si no se escribe otro argumento seguido de la palabra crear, por defecto se crearán dos servidores (s1 y s2). Si ya había algún servidor antes, no se creará ninguno por defecto.
3.La primera vez que se creen servidores, si ponemos crear x (siendo x un número del 1 al 5), x será el número de servidores que se creen. Nuestro programa empezará a contar por 1
(creará s1), asi que por defecto se llamarán s1, s2... hasta un límite de 5 máximo.
4.Si por ejemplo hay tres servidores creados, si queremos crear más servidores usando el método de crear x, (siendo x un numero) y usamos 'crear 4', intentará crear el s1, s2, s3 (no se 
duplicarán porque el programa detecta que se han creado, asi que solo creara el s4. (Es decir, que empieza siempre a crear desde el 1 si usamos este método) 
5.Si se escribe crear x, siendo x una palabra tal como s1, s2, etc, no se ejecutará la orden de crear.
5.La otra forma de crear nuevos servidores teniendo otros ya creados antes, será enviando la orden de 'crear' a secas, y después, siguiendo las instrucciones de varios inputs, se nos 
permitirá añadir el nuevo servidor con el nombre específico.


Cuando el usuario quiera ejecutar la orden "ARRANCAR":

1.No se deberá especificar el número de servidores que se quiere arrancar, únicamente se debe mandar la orden 'arrancar'. A continuación, a partir de unos inputs se podrá decidir si se desea
arrancar un servidor determinado. En caso contrario, se arrancarán todos los servidores que estaban creados.

Cuando el usuario quiera ejecutar la orden "PARAR":

1.Para parar todos los servidores se deberá especificar 'parar todo'al ejecutar la orden en el terminal.
2.Si se quiere ejecutar un servidor en concreto, se deberá indicar 'parar x', siendo x un caracter cualquiera y a continuación se elegirá el nombre del servidor que se quiera parar. 

Cuando el usuario quiera ejecutar la orden "DESTRUIR":

1.Para destruir todos los servidores, se deberá especificar 'destruir todo'. 
2.Si se quiere destruir uno en concreto, indicar 'destruir x', siendo x un caracter cualquiera, y a continuacion se elegira el nombre del servidor que se quiera destruir.


INSTRUCCIONES Y PASOS PARA CÓDIGO PARTE REMOTO:

#antes de nada se debe destruir todo en el ordenador B para que no quede nada
Para esta parte, se hará uso de los ficheros python de remotoA y remotoB.
Se realizará siguiendo los pasos que pone como argumentos de cada archivo, es decir:
Los pasos 1, 3 y 6 se encuentran en el ordenador remoto. Para ejecutarlos habrá que indicar en la terminal: "pyhton3 remotoB.py 1" y lo mismo con el resto de pasos cuando procedan.
Por otra parte, los pasos 2, 4, 5 y 7 se encuentran en el ordenador A. Para ejecutarlos habrá que indicar en la terminal: "pyhton3 remotoA.py 2" y lo mismo con el resto de pasos.

(Estos pasos corresponderían a la orden "configurar")

1.Primero el ordenador B establece conexión con el A
2.El ordenador A crea imagen del db y lo elimina de su equipo.
3.El ordenador B configura los bridges.
4.El ordenador A configura ips
5.Después el ordenador A crea la base de datos db en el ordenador remoto B
6.El ordenador B une el lxdbr0 a la base de datos.
7.El ordenador A modifica los ficheros Nodejs
 
