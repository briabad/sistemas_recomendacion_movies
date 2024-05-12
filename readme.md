

TODO: 
- Definir tipos de usuarios en el sistema de recomendacion demografico. Extraer los perfiles tomando los comportamientos
- app streamlit
- modelo de recomendacion 


- demografico, toma datos y asigna una recomendacion. 
- basado en contenido (el resultado es un vector de preferencias). para movie lens dada las peliculas qe ya estan puntuadas obtener prefrencias. preferencias por gustos. siempre recomienda lo mismo
- colaborativo. datos de todos los usarios del sistema. tecnicas mas complejas. vecinos knn (mas simple) es la que tenemos qu eimplementar en el trabajo. 

vecinos segun preferencias, vecinos segun items, posibles implementaciones. 

## clasificacion basados en memoria (colaborativo)
### basados en similitud

- basada en susuarios (veciinos). Buscamos vecinos y  recomendamos. basado en alguna distancia entre vectores. en este se va a basar el trabajo. Se asigna un treshold del numero de vecinos.  Los vecinos de los usuarios se calcularan de acuerdo a los gustos del usuario, estos pueden cambiar con el tiempo. Para cada usuario tendremos por columna cada pelicula y los reglones los registros de las calificaciones para cada eplicula de cada usuario (esto seria buscar por items ), esto mismo se puede repetir por preferencias, demograficos....etc. 

calculamos el ratio de similutud por el item la calificacion del item a recomendar de cada usuario. se divide la suma de los ratios del item por la suma de las afinidades de los usarios. 
ratios del item = calificacion de cada usuario por la afinidad 
una forma de calcular la distancia, similitud entre usuarios es a traves de la correlacion de pearson. nos quedamos con los n mayores, esto depende de la implementacion.
el ratio de la recomenacion puede estar dado por la afinidad o por el numero de vecinos que comparten essta recomendacion. 
una forma de evitar datos falseados es eliminar registros en donde en caracteristicas tengan 0s
es mejor usar la clasificacion basada en items. 



- basado en items (se hacen similitudes cada vez). computacionalmente costosa, no hay mejora significativa respecto a basada en usuarios. 

### Basados en modelos (colaborativo)


problema de nuevo usuario, problema de nuevo item, problema de oveja negra, 

### trabajo
para cada vecino tener la recomendacion del vecino, id del vecino y su ratio de afinidad. Si un uusario se registra y no nos da preferencias no podemos calcular el colaborativo. hay que desactivar la casilla o mandar un mensaje de error si este es el caso. 
optativo
busqueda de usuario por items. 

1 crear un vector de preferencias este va a estar basado en las calificaciones que cada usuario ha hecho para cada genero, se podria ocupar el promedio para calcular el valor de afinidad para cada genero. podriamos tomar solamente valores (ratings) mayores a 3. para el basado en contenido tomar solamente los mayores. 



### TEMA 6


## TEMA 9 
metricas a tomar en cuenta
- precision
- utiliad : capacidad del sistema de obtener una buena recomendacion
- cobertura: que proporcion de items podemos recomndar
- novedad y sorpresa 
- latencia: el tiempo cuenta. no ocupar algoritmos muy pesados
- error absoluto medio, error entre radios, ya no depende el tamano del conjunto, en donde se resta el ratio dado por el recomendador con el ratio verdadero. 

la idea es tener cojuntos de recomendados y recomendaciones de tamaano adecuado. 