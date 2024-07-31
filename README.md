
![BannerHenry](src/Henry/HEADER-BLOG-NEGRO-01.jpg)

---


# 🚀 Proyecto-Individual-Piparo-Federico

####  ¡Bienvenido al repositorio del proyecto individual de Federico Piparo! 🎉 Aquí encontrarás toda la información necesaria para entender y explorar el proyecto.

---

#### 📚 Descripción del Proyecto
al tratarse este proyecto de una evaluación más allá de un proyecto real, explicaré las decisiones y problemas que me hayan surgido a lo largo de este, aparte de aclaraciones sobre el funcionamiento de este, dividiendolo en las diferentes "partes" del mismo.



#### Aclaraciones generales 

la carpeta src cuenta con imagenes, configuraciones, entre otras cosas, no cuenta con información relevante para el proyecto, por lo que se recomienda no entrar en esta.

 El archivo `.gitattributes`  en general se utiliza para configurar cómo Git maneja ciertos archivos en tu repositorio. En este caso `.csv filter=lfs diff=lfs merge=lfs -text` indica que todos los archivos .csv deben ser gestionados por Git LFS y se excluyen de las diferencias y fusiones normales de texto.

---

# Transformaciones


🛠️ Desafíos y Soluciones

Aun que sea algo obvio, en caso de querer 
Formato CSV: el formato CSV no admite tipos de datos "compuestos" como lo son diccionarios o columnas, por lo cual fue necesario implementar una función que analice la estructura de los datos, y en caso de cumplir con la de una lista o un diccionario los transforme en uno de estos. El trabajo sufrio muchos cambios a lo largo del desarrollo del mismo, al final terminamos quedando con un archivo "transformados.parquet" el cual incorpora tambien series de "credits" para utilizarlas en nuestra API. La mayoría de cambios 


---

# API
Fue un desafío al comienzo la incorporación de FastAPI y tambien deployarla después, pero salvo por las complicaciones iniciales las funciones a excepcion de la ultima no eran muy complicadas de realizar. Como se puede ver esta tambien cuenta con un apartado gráfico, puede verse en ``API\web``.


---

# Sistema de recomendación

A pesar de que el sistema de recomendación basado en similitud del coseno cuenta con la lógica y funciones correctas, no está produciendo resultados precisos. La razón principal detrás de este problema es la limitación de memoria impuesta por la restricción de "peso" de 512Mb. Debido a esta limitación, fue necesario reducir significativamente el tamaño de la matriz de similitud, lo que resultó en una matriz con solo series de valores numéricos y un número reducido de filas.

Esta reducción del tamaño de la matriz afecta negativamente el funcionamiento del sistema de recomendación, ya que no puede capturar la complejidad y la riqueza de los datos originales. Sin embargo, si se pudiera aumentar el tamaño de la matriz a su tamaño óptimo, que sería de varios gigabytes, el sistema funcionaría correctamente y produciría resultados precisos.

En resumen, la limitación de memoria es el principal obstáculo que impide que el sistema de recomendación basado en similitud del coseno funcione correctamente. Al aumentar el tamaño de la matriz y permitir que el sistema utilice más datos, se podrían obtener resultados más precisos y útiles. Pero la logica del mismo es correcta. 

---

# EDA
---
el notebook con el Análisis exploratorio de los datos: (Exploratory Data Analysis-EDA) se encuentra dentro de la carpeta Transformaciones.  En cuanto al mismo diría que fue lo más sencillo del trabajo, ya que no se pedía una gran profundidad en el mismo. 

## links

video: https://www.youtube.com/watch?v=v5wsr5jfKno&t=2s

deploy:https://proyecto-individual-piparo-federico.onrender.com
