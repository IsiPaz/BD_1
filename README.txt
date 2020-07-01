
# Tarea 1 :  Oracle

Tarea 1 para el ramo Bases de Datos, primer semestre 2020.

Isidora Ubilla Zavala
201804581-0

## Para Comenzar

Para el desarrollo de esta tarea se solicita aprender sobre SQL y como realizar Querys para interactuar con la base de datos mediante Python.

Los detalles de la tarea se encuentran en el archivo **Tarea 1.pdf** y los datos para llenar una de las tablas se obtienen del archivo **pokemon.csv**.
### Prerequisitos

Para correr el archivo **create_tables.py** es necesario instalar :
- Oracle  Express edition (XE)
> **Nota:** Es recomendable instalar **Oracle SQL Developer** para tener un mayor control  sobre la BD.




## Consideraciones

Es necesario tener en consideración algunos puntos que se asumieron para realizar alguna de las funcionalidades y no son detallados en el **.pdf** .

### Llenado de la tabla Sansanito

La tabla Sansanito se llena aleatoriamente a partir de un input entregado por el usuario, esto es para facilitar el testeo del programa y una inserción rápida.

### CRUD

- Para la función **Create**, al usuario solo se le solicita ingresar información que no se encuentra en la tabla POYO, a excepción del nombre, es decir, hp actual y estado del Pokémon.
- **Read** imprime toda la información de cada Pokémon registrado en la tabla  Sansanito.
- En el caso de **Update**, está solo permite realizar cambios en el hp actual o en el estado de un Pokémon.
- **Delete** fue implementada de tal forma que se puede optar por dos opciones, borrar toda la información de la tabla o eliminar una fila en particular a partir del ID de un Pokémon que se le entregue como input. 

 > **Nota:** En caso de que Delete borre toda la tabla, la secuencia de ID no se reinicia, por favor, estar seguros de elegir esta opción+.
> 
> **Nota:** En todos aquellos inputs que se soliciten ingresar el Nombre del Pokémon es necesario escribirlo tal y como se encuentra registrados en **pokemon.csv**, en otras palabras, **es necesario que se ingresen con la primera letra en mayúscula y bien escrito**.
> 

### Mostrar nombre del Pokémon más repetido en la base de datos.

En caso de no existir más de un Pokémon con el mismo nombre, se imprime un nombre aleatorio dentro de los que se encuentren registrados en la tabla.

### Capacidad actual de la tabla.
Esta función no es solicitada en la tarea, sin embargo, en el Menu principal queda como opción porque fue muy útil durante el proceso de testear el programa.

## Reiniciar el Programa

Para reiniciar el programa se deben descomentar las lineas de la 910-919 y volver a correr por consola.

Si las tablas, trigger, vistas y secuencias no se encuentran previamente creadas y estas lineas están descomentadas se producirá un error. 



