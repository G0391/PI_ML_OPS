import pandas as pd
import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq
from fastapi import FastAPI
from sklearn.metrics.pairwise import cosine_similarity

app = FastAPI()

df_PlayTimeGenre = pd.read_parquet("Datasets/df_PlayTimeGenre.parquet")
df_UserForGenre = pd.read_parquet("Datasets/df_UsersForGenre3.parquet")
df_UsersRecommend = pd.read_parquet("Datasets/df_UsersRecommend.parquet")
df_UsersWorstDeveloper = pd.read_parquet("Datasets/df_UsersWorstDeveloper_final.parquet")
df_Sentiment_Analysis = pd.read_parquet("Datasets/df_Sentiment_analysis.parquet")

"""## 1.PlaytimeGenre"""

@app.get("/PlayTimeGenre")
def PlayTimeGenre(genero:str):
    """
    La funcion devuelve el año con mas horas jugadas para el género
    """
    generos = df_PlayTimeGenre[df_PlayTimeGenre["main_genre"]== genero] #Filtramos en el dataframe el genero requerido#
    if generos.empty:  #Se nos informará si se encuentra vacío#
        return f"No se encontraron datos para el género {genero}"
    año_max = generos.loc[generos["playtime_hour"].idxmax()] #Primero identificamos la fila (indice) que tiene la máxima cantidad de horas jugadas para el género dado y posteriormente se selecciona esa fila a partir del indice
    result = {
        'Genero': genero,
        'Año con Más Horas Jugadas': int(año_max["release_year"]),
        'Total de Horas Jugadas': año_max["playtime_hour"]
    }

    return result

"""## 2.UserForGenre"""

@app.get("/UserForGenre")
def UserForGenre(genero: str):
    """
    La funcion devuelve el usuario con más horas jugadas en el género solicitado y una lista de la acumulación de horas jugadas por año.
    """
    generos2 = df_UserForGenre[df_UserForGenre["main_genre"]== genero]
    user_max = generos2.loc[generos2["playtime_hour"].idxmax()]["user_id"]
    horas_x_año = generos2.groupby(["year_posted"])["playtime_hour"].sum().reset_index()
    horas_lista = horas_x_año.rename(columns={"year_posted": "Año", "playtime_hour": "Horas"}).to_dict(orient="records")
    result2 = {
        "Genero": genero,
        "Usuario con Más Horas Jugadas": user_max,
        "Total de Horas Jugadas Por Año": horas_lista
    }
    return result2

"""## 3. UsersRecommend"""

@app.get("/UsersRecommend")
def UsersRecommend(anio:int):
    """
    Funcion que devuelve el top 3 de juegos MÁS recomendados por usuarios para el año dado.
    """
    df_año= df_UsersRecommend[df_UsersRecommend["year_posted"]== anio]
    if type(anio) != int:
        return {"Debes colocar el año en entero, Ejemplo:2012"}
    if anio < df_UsersRecommend["year_posted"].min() or anio > df_UsersRecommend["year_posted"].max():
        return {"Año no encontrado"}
    df_ordenado_recomendacion = df_año.sort_values(by="recommendation_count", ascending=False)
    top_3_juegos = df_ordenado_recomendacion.head(3)[["app_name","recommendation_count"]]
    result3 ={
        "Año": anio,
        "Top 3 Juegos Más Recomendados": top_3_juegos.to_dict(orient="records")
    }
    return result3

"""## 4. UsersWorstDeveloper"""

@app.get("/UsersWorstDeveloper")
def UsersWorstDeveloper(anio:int):
    """
    Funcion que devuelve el top 3 de desarrolladoras con juegos MENOS
    recomendados por usuarios para el año dado.
    """
    df_año2 = df_UsersWorstDeveloper[df_UsersWorstDeveloper["year_posted"]== anio]
    if type(anio) != int:
        return {"Debes colocar el año en entero, Ejemplo:2012"}
    if anio < df_UsersRecommend["year_posted"].min() or anio > df_UsersRecommend["year_posted"].max():
        return {"Año no encontrado "}
    df_ordenado_recomendacion2 = df_año2.sort_values(by="recommendation_count", ascending=False)
    top_3_developers = df_ordenado_recomendacion2.head(3)[["developer","recommendation_count"]]
    result4 = {
        'Año': anio,
        'Top 3 Desarrolladoras Menos Recomendadas': top_3_developers.rename(columns={"developer": "Desarrolladora", "recommendation_count": "Conteo Recomendacion"}).to_dict(orient="records")
    }
    return result4

"""## 5. sentiment_analysis"""

@app.get("/SentimentAnalysis")
def sentiment_analysis( desarrolladora : str ):
    """
    Funcion que devuelve un diccionario con el nombre de la desarrolladora como llave y una lista
    con la cantidad total de registros de reseñas de usuarios que se encuentren categorizados con
    un análisis de sentimiento como valor.
    """
    if type(desarrolladora) != str:
        return "Debes colocar un developer de tipo str, EJ:'07th Expansion'"
    if len(desarrolladora) == 0:
        return "Debes colocar un developer en tipo String"
    df_developer = df_Sentiment_Analysis[df_Sentiment_Analysis["developer"]== desarrolladora]
    sentiment_counts = df_developer.groupby("sentiment_analysis")["sentiment_analysis_count"].sum().to_dict()
    sentiment_dicc = {0: "Negativo", 1: "Neutral", 2: "Positivo"}
    sentiment_counts = {sentiment_dicc[key]: value for key, value in sentiment_counts.items()}
    result5 = {desarrolladora: sentiment_counts}
    return result5

"""## 6.Sistema de recomendacion de juegos"""

modelo_recomendacion = pd.read_csv("Datasets/df_modelo_recomendacion.csv")

def recomendacion_juego(id_juego):
    try:
        id_juego = int(id_juego)
        juego_seleccionado = modelo_recomendacion[modelo_recomendacion["id"] == id_juego]
        if juego_seleccionado.empty:
            return {"error": f"El juego con el ID '{id_juego}' no se encuentra."}
        indice_juego = juego_seleccionado.index[0]
        muestra = 3000
        df_muestra = modelo_recomendacion.sample(n=muestra, random_state=50)
        juego_features = modelo_recomendacion.iloc[indice_juego, 3:]
        muestra_features = df_muestra.iloc[:, 3:]
        similitud = cosine_similarity([juego_features], muestra_features)[0]
        recomendaciones = sorted(enumerate(similitud), key=lambda x: x[1], reverse=True)[:5]
        recomendaciones_indices = [i[0] for i in recomendaciones]
        recomendaciones_names = df_muestra["app_name"].iloc[recomendaciones_indices].tolist()

        return {"Juegos_similares": recomendaciones_names}

    except ValueError:
        return {"error": "El ID del juego debe ser un número entero válido."}

@app.get("/recomendar/{juego_id}")
def obtener_recomendaciones(juego_id: int):
    try:
        recomendaciones = recomendacion_juego(juego_id)
        return {"recomendaciones": recomendaciones}
    except Exception as e:
        return {"error": f"Error en la recomendación: {str(e)}"}

