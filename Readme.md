<p align=center><img src=https://d31uz8lwfmyn8g.cloudfront.net/Assets/logo-henry-white-lg.png><p>

# <h1 align=center> **PROYECTO INDIVIDUAL Nº1** </h1>

# <h1 align=center>**`Machine Learning Operations (MLOps)`**</h1>

<p align="center">
<img src="https://user-images.githubusercontent.com/67664604/217914153-1eb00e25-ac08-4dfa-aaf8-53c09038f082.png"  height=300>
</p>

<h1 align=center>¡Bienvenidos al primer proyecto individual de la etapa de labs! </h1>

En este proyecto, llevamos a cabo el rol de un Ingeniero MLOps en Steam, una plataforma de video juegos de nivel mundial. Nuestra tarea, crear un sistema de recomendación de videojuegos utilizando aprendizaje automático. Para ello, los datos necesitaron ser refinados y transformados para poder ser utilizados y así, desarrollar un Producto Mínimo Viable (MVP) y desplegarlo como una API RESTful.

<h1 align=center>Descripción del Problema</h1>

Como Científico de Datos en Steam, y detallando nuestra tarea en profundidad debemos crear un modelo de aprendizaje automático que para un sistema de recomendación de videojuegos. Recibimos los datos no procesados y en estado crudo, por lo cual debemos procesar los datos que tenemos para poder avanzar y concluir nuestra tarea. 

<h1 align=center>Información del Juego en Steam</h1>

En el proyecto, recibimos tres archivos JSON cada uno contiene datos únicos. 

users_items.json: Nos brinda datos de cada uno de los juegos que han sido jugados por los usuarios y por cuanto tiempo.

steam_games.json: Se refiere justamente a los juegos de Steam. Incluye datos del nombre del juego, número de identificación, año de lanzamiento, desarrollador y género. 

user_reviews.json: Nos brinda reseñas realizadas por los jugadores, el id de estos jugadores, el juego sobre el cual brindaron su opinión y la fecha.

<h1 align=center>Detalles sobre el trabajo</h1>
Limpieza y Transformación de Datos: 
En el inicio, comenzamos eliminando columnas que no son necesarias para nuestra tarea. La finalidad es es optimizar el rendimiento de la API. También deberemos desanidar datos para poder llegar a limpiar algunas columnas. Esta última tarea se lleva a cabo especialmente en users_items.json y user_reviews.json aunque el trabajo de limpieza y transformación de datos se lleva a cabo se lleva en mayor o menor medida en los tres archivos JSON recibidos. Finalmente, terminamos el proceso y obtenemos 3 archivos depurados: "ETL_Steam_games.ipynb", "ETL_User_review.ipynb", "ETL_user_items.ipynb". 

Análisis de Sentimiento: Se crea una nueva columna llamada 'sentiment_analysis', aplicando análisis de sentimiento de acuerdo a la reseña de los usuarios. La escala que se utiliza es: '0' para comentarios negativos, '1' para neutrales y '2' para positivos.

Análisis Exploratorio de Datos (EDA):
Se realiza ahora una exploración manual, un análisis exploratorio de los datos luego de alcanzar cada uno de los ETL. Allí investigaremos relaciones entre variables, podremos  identificar valores atípicos y hallar patrones interesantes dentro del conjunto de datos. Realizaremos análisis estadísticos y visualizaciones con gráficos para clarificar estas relaciones entre diferentes variables. "EDA"

Optimización del rendimiento y espacio:
Antes de desarrollar las funciones de la API, se llevó a cabo la creación de dataframes nuevos dataframes con la finalidad de optimizar las funciones, mejorar su rendimiento y disminuir el espacio. Finalmente, estos dataframes almacenan solo los datos fundamentales para las consultas de la API. "Dataframes Auxiliares

Desarrollo de la API:
Utilizaremos el framework FastAPI para exponer los datos de la empresa a través de endpoints RESTful.
Endpoints:
PlayTimeGenre(genero: str): Brinda el año de lanzamiento con más horas jugadas para el género consultado.

UserForGenre(genero: str): Brinda el usuario con más horas jugadas para el género consultado y una lista de acumulación de horas jugadas por año.

UsersRecommend(año: int): Devuelve el top 3 de juegos más recomendados por usuarios para el año solicitado.

UsersWorstDeveloper(año: int): Devuelve el top 3 de desarrolladoras con juegos menos recomendados por usuarios para el año solicitado.

Sentiment_analysis(empresa_desarrolladora: str): Devuelve un diccionario con el recuento de análisis de sentimiento para reseñas asociadas con el desarrollador de juegos especificado.

Creamos la carpeta Datasets: 
En la misma se encuentran los dataframes utilizados para cada funcion. Estos dataframes nos sirvieron para probar las funciones antes de avanzar con la ejecución de la API. 

Sistema de Recomendación: 
Implementamos un sistema de recomendación, en donde el sistema toma un item y nos recomienda cinco similares a este. Debido a los límites de memoria, utilizaremos sólo una muestra de los datos. 

Render: 
Realizamos la implementación en la nube seleccionando Render. Esta plataforma nos permite de manera sencilla dejar funcionando nuestra API en todo momento. Por lo tanto, luego de probar nuestra plataforma de manera local, deployamos nuestra API en Render, la misma se puede consultar en: https://g0391-pi-ml-ops.onrender.com

Video: 
Finalmente, en el siguiente video se puede observar una pequeña explicación del procedimiento realizado y de la API en Render. 

<h1 align=center>Tecnologías elegidas</h1>
En el desarrollo de este proyecto, aprovechamos varias tecnologías para llevar a cabo las distintas etapas del proceso:
Python, Pandas, Numpy, Matplotlib, Seaborn, FastAPI, Scikit-learn, Render.

