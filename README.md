# Proyecto DGT

## Descripción del proyecto

En este proyecto se aplican los conocimientos aprendidos a lo largo de todo el programa. Se realiza un análisis exploratorio de datos (EDA) sobre datos de la Dirección General de Tráfico de España (DGT), utilizando Python y las principales librerías para análisis de datos. Además, se presentan los principales resultados en un dashobard en Power BI.


En el repositorio constan:

- Archivo README.md, que recoge los pasos seguidos durante el proyecto y el informe del análisis.
- Una carpeta de datos donde se encuentran los archivos (ya unificados) de datos generales municipales, datos de siniestros y puntos por municipios y datos de sanciones por municipios, para el periodo 2014-2024. En esta carpeta también están los ficheros de datos guardados después de las transformaciones (processed). 
- Una carpeta con los scripts de Python que se han desarrollado para:
    - unificar los ficheros de datos descargados de la DGT (carga_DGT.py)
    - realizar un análisis inicial del fichero y primera depuración, esto es, la transformación y limpieza profunda de los datos (analisis_DGT.ipynb)
    - realizar el análisis exploratorio de datos (análisis descriptivo y estadístico de los datos)
- Una carpeta con los metadatos de los tres conjuntos de datos con los que se trabaja (datos municipales, sanciones y puntos, siniestros)
- Una carpeta de imágenes donde se han guardado los resultados de los gráficos procesados en el notebook.
- Una carpeta con el dashboard en Power BI.


## Tecnologías utilizadas

- El análisis EDA se ha llevado a cabo en código Python 3.13.15, en un documento de Python y otro Jupyter Notebook.
- Se han utilizado librerías como Pandas, Path, NumPy, Matplotlib, Seaborn.
- Visual Studio Code ha sido el visor utilizado para el desarrollo.
- El dashboard se ha desarrollado en Power BI.
- Los ficheros del proyecto se entregan en GitHub.


## Requisitos

- Transformación y limpieza profunda de los datos.
- Análisis descriptivo de los datos.
- Análisis estadístico de los datos.
- Visualización de los datos.
- Dashboard operativo.
- Informe explicativo del análisis.
- Readme del proyecto.


## Pasos del proyecto

### Datos

Los datos con los que se realiza el proyecto están disponibles en la página web de la DGT: https://www.dgt.es/menusecundario/dgt-en-cifras/
En concreto, los datos de este proyecto provienen de tres productos: 
- datos de las fichas municipales.
- datos de las saciones y puntos a nivel municipal.
- datos de los siniestros a nivel municipal.

Estos tres productos, a su vez, vienen con una ficha de metadatos para cada año. En este proyecto se descargan los datos para la serie 2014-2024, y a modo de ejemplo, las fichas de los años 2024.

Contamos inicialmente con 33 excels: 
- DatosMunicipalesGeneral_{20XX}.xlsx (para los años 2014-2024)
- DatosMunicipalesSancionesPuntos_{20XX}.xlsx (para los años 2014-2024)
- DatosMunicipalesSiniestralidad_{20XX}.xlsx (para los años 2014-2024)


### Unificación de los ficheros

La obtención de un fichero de datos definitivos se desarrolla en el script carga_DGT.py.

En todos los excels hay una variable, "Código INE", que es el código oficial establecido por el INE para cada municipio, que podría permitir la unión. Para poder hacer un merge, se necesita una clave "Año", "Código INE". Se introduce la variable "Año" en la unificación de los ficheros de cada estadística 

Una vez unificados los ficheros de datos de cada una de las estadísticas, se obtienen los tres datasets:
- generales_2014_2024.xlsx (90.156 filas y 58 columnas)
- sanciones_2014_2024.xlsx (90.144 filas y 26 columnas)
- siniestros_2014_2024.xlsx (90.144 filas y 36 columnas)




### Limpieza de datos

El análisis explotario inicial de los ficheros, antes de realizar el merge, y la unificación en un único excel, se lleva a cabo en carga_DGT.py,

- Tratamiento de duplicados. Como en los ficheros originales no hay filas duplicadas, no hay que hacer ninguna modificación.
- Exploración inicial del fichero de datos definitivo. Antes de realizar el merge, se observa una diferencia en las filas: mientras que el excel con datos generales contiene 90.156 filas, los otros dos de sanciones y puntos y siniestros tienen, cada uno, 90.144 filas. Se detecta la diferencia en el año 2024, por lo que se extraen y comparan los códigos INE de los municipios solo de este año, en los tres ficheros de datos por separado.
    - Hay 15 códigos que están en el fichero de datos municipales generales pero no están en los otros dos: [7991, 7992, 7993, 7994, 7995, 7996, 35991, 35992, 35993, 36011, 36012, 38991, 38992, 38993, 38994]. No se pierde la información de estas filas.
    - Hay 3 códigos que están el los excels de sanciones y puntos y siniestros, pero no están en el fichero de datos generales: [48916, 51000, 52000]. Estos tres códigos corresponden a los municipios Usansolo (Bizkaia), Ceuta (municipio sin especificar) y Melilla (municipio sin especificar). Los códigos 51000 y 52000 son similares a 51001 y 52001, respectivamente. Los tres están vacíos, luego se puede hacer un left join y perder estas filas vacías.

Así queda explicada la diferencia de 12 filas, sin pérdida de información.
- Creación de un único fichero de datos. Se lleva a cabo un procedimiento para unificar los tres ficheros de datos en uno solo.
A partir del par "Año" y "Código INE", se crea un nuevo fichero de datos, data_complete_DGT_2014_2024.xlsx. Se realiza un merge (left join) con los datos del fichero generales_2014_2024.xlsx, al que se añaden las columnas de los excels sanciones_2014_2024.xlsx y siniestros_2014_2024.xlsx. El fichero resultante, data_complete_DGT_2014_2024.xlsx, contiene 90.156 filas y 116 columnas.


La limpieza de los datos, así como el análisis exploratorio y estadístico de todos los datos, se lleva a cabo en el script analisis_DGT.ipynb.

- Selección de las columnas de interés para el análisis. El fichero cuenta con 116 columnas, algunas de las cuales están repetidas (información de municipios) o no son necesarias para el estudio que se va a desarrollar. Finalmente, el fichero de datos con el que se lleva a cabo el estudio es data_DGT_2014_2024.xlsx, que cuenta con 90.156 filas y 90 columnas.
- Tratamiento de los valores nulos. Se observa el fichero no tiene valores nulos.
- Los tipos de datos de las variables del fichero son int64, str y float64. No hay que hacer ninguna corrección en los tipos de datos.


### Análisis exploratorio

Se lleva a cabo un primer análisis de los datos del fichero. Dado que están disponibles los datos de numerosas variables para el periodo 2014-2024 y todos los municipios, un buen comienzo es analizar algunos indicadores clave a nivel nacional y a nivel de Comunidades Autónomas.

#### Nivel 1: España por años

¿Cómo ha evolucionado la población, la movilidad y la seguridad vial en España entre 2014 y 2024? Para responder esta pregunta, se agregan los datos municipales para cada año. Además, se crean nuevas columnas, con indicadores relacionados con los accidentes con víctimas, los fallecidos, las sanciones, y el parque de vehículos:
- Vehículos por cada 1.000 habitantes
- Accidentes por cada 1.000 habitantes
- Fallecidos por cada 100.000 habitantes,
- Sanciones por cada 1.000 conductores
- Porcentaje de parque electrificado

Estos indicadores se presentan en formato tabla y se crean dos gráficos de línea. Uno de ellos refleja la evolución conjunta de los accidentes por cada 1.000 habitantes en el periodo de estudio y los fallecidos por cada 100.000 habitantes, en el ámbito nacional. El segundo gráfico muestra la evolución en el periodo de las sanciones por cada 1.000 conductores.

Em ambos gráficos se observa una clara ruptura de la serie en el año 2020, condicionado por el COVID-19 y el confinamiento, lo que produjo una reducción significativa en el uso de los vehículos y, por tanto, en todas las variables relacionadas (accidentes, fallecimientos, sanciones,...). A partir de 2021 aumentan estos indicadores, y en 2023 se observan niveles similares a los años previos a la pandemia. 

Con el fin de analizar las diferencias entre los extremos del periodo, se crea una tabla donde se comparan las variaciones de los años 2014 y 2024. Aumenta el parque de vehículos por 1.000 habitantes, los accidentes por 1.000 habitantes, los fallecidos por 100.000 habitantes (aunque en menor medida que los accidentes) y disminuyen las sanciones cada 1.000 conductores. 

Es significativo el aumento en el porcentaje de vehículos electrificados, y junto con la gráfica de la evolución, se aprecia un crecimiento continuo desde 2024, alcanzando caso un 1% del parque en 2024.



#### Nivel 2: Comunidades Autónomas

¿Existen diferencias territoriales entre comunidades autónomas? Antes de profundizar a nivel municipal, analizamos si existen diferencias entre las comunidades autónomas a lo largo de los años.
En esta ocasión los datos se agrupan por año y CCAA (están incluidas Ceuta y Melilla), y se selecciona un número de variables más reducido. Se realiza un análisis similar al previo a nivel nacional, estudiando los mismos indicadores.

A modo resumen se crea una tabla con los indicadores mencionados previamente, por año (a modo de ejemplo se selecciona el año 2024).
Para analizar los datos de este año, se calculan dos tablas a partir de esta:
- top 5: para cada indicador, se selecciona el top 5 de CCAA.
- bottom 5: para cada indicador, se selecciona el bottom 5 de CCAA.

Se observa lo siguiente:
- En Baleares hay casi un coche por habitante. Destacan Canarias y Melilla en el top5, teniendo en cuenta el menor espacio de esta comunidad autónoma y ciudad autónoma.
- En el top 5 también destacan los accidentes y sanciones en Ceuta y Melilla, así como los fallecimientos en Murcia, La Rioja y Asturias. 
- Las únicas comunidades autónomas donde se supera el 1% de vehículos electrificados son Madrid, Cataluña y Baleares.
- Teniendo en cuenta el número de vehículos por 1.000 habitantes, destaca en el bottom 5 el bajo número de accidentes y sanciones en Canarias.
- El País Vasco es la CCAA con el menor número de vehículos por 1.000 habitantes, seguido de Cataluña y Aragón. 
- Donde menor es el porcentaje de electrificados es en Ceuta, seguido de Extremadura, Castilla y León, Melilla y Galicia.

Por último, se obtiene un heatmap con las 19 CCAA y los 5 indicadores, donde está representada la diferencia con respecto a la media de cada uno de ellos. Hay que tener en cuenta que se han normalizado los indicadores para que pueda ser comparable, dado que los indicadores tienen escalas diferentes.



#### Nivel 3: Municipios. 

¿Qué características tienen los municipios con mayor/menor siniestralidad? ¿Cómo varían las diferencias entre los municipios a lo largo de los años? 



### Análisis descriptivo

El objetivo del análisis descriptivo llevado a cabo es conocer el dataset antes de buscar relaciones.
¿Qué características tienen los municipios con mayor/menor siniestralidad? ¿Cómo varían las diferencias entre los municipios a lo largo de los años? 
Para responder algunas preguntas acerca de los municipios, creamos nuevas variables agrupando las sanciones, indicadores relativos para poder comparar municipios y tablas con estadísticos descriptivos para algunas variables clave a lo largo de los años. Obtenemos un fichero con 90156 filas y 102 columnas.

Se crean nuevas variables, que tienen en cuenta los distintos tipos de sanciones, agrupando los puntos que quitan cada sanción.
Se seleccionan las siguientes variables, para analizar con más detalle: "Población Total", "Censo Conductores", "Parque Total", "Antigüedad Media del Parque (<25 años)", "Electrificado", "Total Puntos Detraídos", "Total Sanciones con Puntos", "Sanciones_Velocidad", "Sanciones_Alcohol", "Sanciones_Drogas", "Sanciones_Proteccion", "Sanciones_Movil", "Sanciones_Semaforo", "Sanciones_Otras", "Nº Accidentes con Víctimas", "Fallecidos". Para analizar estas variables, se crean tablas descriptivas, teniendo en cuenta todos los municipios.

- La característica principal del análisis de las tablas es que existe una gran desviación en los datos, en todas las variables. Esto se debe a las grandes diferencias que existen entre los municipios de España.
- El 75% de los municipios tiene como máximo entre 1.400 y 1.500 conductores, aproximadamente, durante el periodo analizado. En la tabla se observa que la media está alrededor de 300 conductores, mientras que la media está por encima de 3.200. Esto es un claro indicativo de que se trata de una distribución muy asimétrica. Existen municipios de gran tamaño que elevan considerablemente el promedio.
- Se puede hacer un análisis similar del "Parque Total", con una media entre 4.000-5.000 vehículos, una mediana que está entre 510-570 vehículos y donde el 75% de los municipios tiene 2.000-2.400 vehículos.
- La antigüedad media del parque sí tiene una distribución bastante simétrica, con una media y mediana entre 11-14 años, y donde el 75% de los municipios tiene como máximo vehículos con 12,5-1,5 años de antigüedad, a lo largo de los años analizados. Esto es, se trata de un parque bastante antiguo.
- En cuanto a los coches electrificados, se observa una clara evolución entre 2014-2024, con máximo de 43.607 vehículos, frente a los 1-947 en 2014.
- Hay mucha asimetría también en el total de puntos detraídos y el total de sanciones con puntos, variables en las que se observa una gran diferencia entre la media y la mediana. Los mínimos se obsrevan en 2020, condicionado por el COVID-19. A pesar de que hay un aumento de puntos y sanciones entre 2014 y 2024, el año 2024 presenta valores mínimos desde 2022. Hay que tener en cuenta en este análisis que durante la década de 2014 a 2024 se introdujeron nuevas sanciones y se modificaron sustancialmente las cuantías y la retirada de puntos en España.
- Las variables de distintos tipos de sanciones también presentan gran asimetría. Se grafican los totales anuales de los distintos tipos, de 2014 y 2024. En el gráfico se observa que han aumentado todos los tipos de sanciones menos las de velocidad. Algunas de estas diferencias pueden estar justificadas por el aumento de controles, endurecimiento de la normativa, mayor uso de teléfonos móviles. El mayor número de sanciones se sigue registrando en "Semáforos".


Se contempló la opción de tener en cuenta para el análisis los municipios con más de 5.000 habitantes, o con más de 1.000 habitantes, para evitar los outliers. Sin embargo, finalmente se optó por no dejar fuera ningún municipio. Podría tratarse de una futura línea de mejora.


#### Análisis bivariante y correlaciones. Principales visualizaciones

¿Qué relación hay entre las sanciones y la siniestralidad?
Para llevar a cabo este análisis se trabaja con variables relativas, dado que hay mucha diferencia entre los municipios. Estas diferencias pueden condicionar los resultados.

Se tienen en cuenta las siguientes variables:
- Antigüedad Media del Parque (<25 años)
- Vehiculos_por_1000_hab
- Accidentes_por_1000_hab
- Fallecidos_por_100000_hab
- Sanciones_por_1000_conductores
- Puntos_por_sancion
- Pct_Electrificado

En un primer análisis con Heatmap, se observa que no hay mucha correlación entre las variables. Se analizan 2014 y 2024, y la mayor diferencia se presenta en la correlación (negativa, como cabría esperar) entre la antigüedad media del parque y el porcentaje de electrificados. Esto es, a un mayor porcentaje de vehículos electrificados, menor es la antigüedad del parque.




- Electrificación y antigüedad del parque: la correlación pasa de −0,43 en 2014 a −0,58 en 2024. La asociación negativa se hace más marcada: los municipios con un parque más antiguo tienden a tener un porcentaje menor de vehículos electrificados; los que tienen un parque más reciente tienden a tener un porcentaje mayor.
- Electrificación y accidentes por 1.000 habitantes: baja de 0,41 en 2014 a 0,30 en 2024. La asociación positiva sigue presente, pero es más débil en 2024. No significa que electrificar los vehículos provoque más accidentes.
- Antigüedad del parque y accidentes por 1.000 habitantes. La relación entre la antigüedad media del parque y los accidentes por 1.000 habitantes cambia de signo entre 2014 y 2024. En 2014 se observa una asociación negativa (ρ = −0,34), mientras que en 2024 la asociación es positiva (ρ = 0,37). Este cambio indica que la relación descriptiva entre ambas variables no se mantiene estable durante el periodo. No permite, por sí solo, atribuir el cambio a la antigüedad de los vehículos.


En los gráficos de dispersión se ven reflejadas ligeramente estas asociaciones, aunque existe una dispersión considerable entre las observaciones y municipios con valores outliers.

Es probable que, debido a las diferencias de tamaño de los municipios, el análisis que se ha llevado a cabo hasta el momento es muy genérico. Conviene profundizar en los diversos grupos para ver si presentan comportamientos diferentes. Para ello, se crean 4 grupos en función del tamaño: "< 500", "500–5.000", "5.000–20.000", "> 20.000".

En el año 2014, la composición de los grupos es: 47,76%, 36,17%, 11,15% y 4,92%. En el heatmap del primer grupo, "< 500", no se observa correlación entre las variables, y sí hay variables sin datos. En el segundo grupo, "500–5.000" se presenta la correlación negativa entre la electrificación y la antigüedad del parque, -0,32. En el tercer grupo, "5.000–20.000", se observa la correlación entre estas dos variables, la mayor de los cuatro grupos, -0,45, y aparece también correlación positiva entre las sanciones por 1.000 conductores y accidentes por 1.000 habitantes, 0,28, sanciones por 1.000 conductores y la electrificación del parque, -0,27. Por último, en el grupo de "> 20.000", destaca la correlación negativa entre la electrificación y la antigüedad del parque, -0,36, la correlación positiva entre la antigüedad y los vehículos por 1.000 habitantes, 0,33, y la correlación positiva entre las sanciones por 1.000 conductores y accidentes por 1.000 habitantes, 0,30. 

En el año 2024, la composición de los grupos es: 48,90%, 34,83%, 10,99% y 5,28%. En líneas generales, una de las diferencias principales respecto a 2014 es la correlación negativa en todos los grupos de tamaños entre la electrificación y la antigüedad (-0,33, -0,68, -0,82, -0,83). Al analizar todos los municipios juntos inicialmente la correlación no era tan fuerte. Al igual que en 2014, en el grupo de "> 20.000", destaca la correlación positiva entre la antigüedad y los vehículos por 1.000 habitantes, 0,30, y la correlación positiva entre las sanciones por 1.000 conductores y accidentes por 1.000 habitantes, 0,30. En los grupos de tamaño intermedio, "500–5.000" y "5.000–20.000", no destacan más correlaciones. Sin embargo, en el grupo de menor tamaño municipal, "< 500", además de la relación entre electrificación y antigüedad del parque aparece una correlación positiva elevada entre la antigüedad del parque y los puntos por sanción (0,77) y las sanciones por 1.000 conductores y los puntos por sanción (0,77). Esto es, hay relación entre clara entre las sanciones y los puntos retirados, y la antigüedad del parque en estos municipios es influyente.


### Power BI




### Conclusiones

En base al análisis que se ha llevado a cabo, se pueden responder algunas cuestiones acerca de la siniestralidad y las sanciones. En estas conclusiones hay que tener en cuenta que el análisis es exclusivamente exploratorio y no permite establecer relaciones de causalidad. 


- ¿Se relacionan las sanciones con la siniestralidad? La relación entre sanciones y accidentes está más presente en los municipios de mayor tamaño ("> 20.000"), al igual que la relación entre los accidentes y los fallecidos. Hay que tener en cuenta que más sanciones no significan necesariamente más infracciones reales; también pueden reflejar más controles, campañas o capacidad de vigilancia.

- ¿Influye la antigüedad del parque? Es una de las variables más influyentes, relacionada con la electrificación y con los accidentes. En el año 2024 también destaca la relación con las sanciones y los puntos retirados.

- ¿Son distintos los resultados según el tamaño municipal? El profundizar en el análisis teniendo en cuenta diferentes agrupaciones por tamaño municipal es fundamental para entender el diferente comportamiento de los municipios. Se observa que con los grupos formados, las relaciones entre las variables de los años 2014 y 2024 aportan mucha más información.

- ¿Hay diferencias a nivel autonómico? En el análisis del nivel 2 se observan claras diferentes entre las comunidades autónomas, sobre todo en el número de accidentes por 1.000 habitantes, sanciones por 1.000 conductores y el porcentaje de electrificados.




### Futuras líneas de investigación

Estas son algunas líneas de investigación que surgen a raíz del trabajo realizado:
- Profundizar en el análisis descriptivo de los municipios, haciendo más grupos por tamaños.
- Analizar con mayor detalle cada uno de los años, no solo 2014 y 2024.
- Mejorar el análisis de las sanciones (velocidad, alcohol, drogas) en relación con los accidentes o los fallecidos.
- Análisis multivariante: clústers de municipios y componentes principales
