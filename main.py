from fastapi import FastAPI, HTTPException
from typing import Optional
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


app = FastAPI()

df_PlayTimeGenre = pd.read_csv("./data/df_PlayTimeGenre.csv")
df_UserForGenre = pd.read_csv("./data/df_UserForGenre.csv")
df_UserRecommend = pd.read_csv("./data/df_UserRecommend.csv")
df_Sentiment_Analysis = pd.read_csv("./data/df_Sentiment_Analysis.csv")
df_ml = pd.read_csv("./data/df_MLOps.csv")


@app.get('/PlayTimeGenre')
def PlayTimeGenre(genero: str):
    """
    Obtener el año de lanzamiento con más horas jugadas para un género específico.

    Parameters:
    - genero (str): Género para filtrar el DataFrame.

    Returns:
    dict: Año de lanzamiento con más horas jugadas para el género dado.
    """
    filtro_genero = df_PlayTimeGenre['genres'].str.contains(genero, case=False, na=False)
    df_filtrado = df_PlayTimeGenre[filtro_genero]

    df_agrupado = df_filtrado.groupby('year')['playtime_forever'].sum().reset_index()
        
    df_agrupado['year'] = df_agrupado['year'].astype(int)
    anio_mayor_suma = int(df_agrupado.loc[df_agrupado['playtime_forever'].idxmax(), 'year'])
        
    respuesta = {f"Año de lanzamiento con más horas jugadas para el género {genero}": anio_mayor_suma}
    return respuesta
    
    
@app.get('/UserForGenre')
def UserForGenre(genero: str):
    filtro_genero = df_UserForGenre['genres'].str.contains(genero, case=False, na=False)
    df_filtrado = df_UserForGenre[filtro_genero]

    df_agrupado = df_filtrado.groupby(['user_id', 'year'])['playtime_forever'].sum().reset_index()

    idx_max_playtime = df_agrupado['playtime_forever'].idxmax()
    usuario_max_playtime = df_agrupado.loc[idx_max_playtime, 'user_id']

    df_usuario = df_agrupado[df_agrupado['user_id'] == usuario_max_playtime]

    resultado_final = [{'Año': int(row['year']), 'Horas': int(row['playtime_forever'])} for _, row in df_usuario.iterrows()]
    
    return {"Usuario con más horas jugadas para Género {}:".format(genero): usuario_max_playtime, "Horas jugadas": resultado_final}


@app.get('/UsersRecommend')
def UsersRecommend(año: int):
    
    df = df_UserRecommend[(df_UserRecommend['year_posted'] == año) & (df_UserRecommend['recommend'] == True)]

    top_juegos = df['title'].value_counts().head(3)

    resultado_final = [{"Puesto {}: {}".format(i+1, juego): recomendaciones} for i, (juego, recomendaciones) in enumerate(top_juegos.items())]

    return resultado_final


@app.get('/UserNotRecommend')
def UserNotRecommend(year: int):
    
    df = df_UserRecommend[(df_UserRecommend['year_posted'] == año) & (df_UserRecommend['recommend'] == False)]

    top_juegos = df['title'].value_counts().head(3)

    resultado_final = [{"Puesto {}: {}".format(i+1, juego): recomendaciones} for i, (juego, recomendaciones) in enumerate(top_juegos.items())]

    return resultado_final


@app.get('/Sentiment_Analysis')
def Sentiment_analysis(desarrollador: str):
    """
    Realiza un análisis de sentimiento para un desarrollador específico.

    Parameters:
    - desarrollador (str): Nombre del desarrollador.

    Returns:
    dict: Resultados del análisis de sentimiento.
    """
    desarrollador = desarrollador.lower()
    desarrollador_fila = df_Sentiment_Analysis[df_Sentiment_Analysis['Developer'] == desarrollador]

    negativo = int(desarrollador_fila['Negativo'].values[0])
    neutro = int(desarrollador_fila['Neutro'].values[0])
    positivo = int(desarrollador_fila['Positivo'].values[0])

    resultado = {
        desarrollador: {
            'Negative': negativo,
            'Neutral': neutro,
            'Positive': positivo
            }
        }

    return resultado

    
@app.get('/recomendacion_usuario')
def recomendacion_usuario(user_id :str):

    user_game_matrix = pd.crosstab(df_ml['user_id'], df_ml['title'])

    user_index = user_game_matrix.index.get_loc(user_id)
    cosine_similarities = cosine_similarity(user_game_matrix, user_game_matrix)

    similar_users = cosine_similarities[user_index]

    games_played = user_game_matrix.loc[user_id]
    unrated_games = games_played[games_played == 0].index

    recommendation_scores = user_game_matrix.loc[:, unrated_games].multiply(similar_users, axis=0).sum(axis=0)

    recommendations = recommendation_scores.sort_values(ascending=False).index.tolist()

    top_recommendations = recommendations[:5]

    return top_recommendations