<p align=center><img src=Steam.png><p>

# SISTEMA DE RECOMENDACIONES DE JUEGOS SOBRE LA PLATAFORMA STEAM

Este es mi primer desarrollo de proyecto personal en Data-Science del bootcamp de Henry en la etapa de Labs.




## Descripción de la consigna

Como Data-Scientist operando para la plataforma Steam de Juegos , se nos pide desarrollar un sistema de recomendaciones de videojuegos para usuarios. El mismo debe contar con distintos tipos de consultas a fin de brindar recomendaciones relevantes y del interes del usuario final.
## Desarrollo

>Ingenieria de Datos
    -Relizamos el ETL de los datos disponibles
    -Se le dio tratamiento a los datos, realizando las tranformaciones necesarias, quitando nulos y duplicados.

>Analisis exploratorio de Datos
    -Se dio tratamiento a los grupos de datos, identicando Outliers, valores faltantes y viendo las correlaciones de los mismos.
    -Se usaron varios modelos de analisis descriptivo con graficas de barras para su mejor comprension

>Sistema de recomendacion
    -Una vez realizados los pasos anteriores generamos el modelo de Machine learning para entrenar el sistema y generar una salida optimizada.
    -Se desarrollo la recomendacion de juego donde el input es un usuario y el output es una lista de juegos que se le recomienda a ese usuario, en general se explican como “A usuarios que son similares a tí también les gustó…”
    
    -Adicionalmente se crean las siguientes funciones para los endpoints que se consumirán en la API, segun lo requerido:

        + def PlayTimeGenre( genero : str ): Debe devolver año con mas horas jugadas para dicho género.
        Ejemplo de retorno: {"Año de lanzamiento con más horas jugadas para Género X" : 2013}

        def UserForGenre( genero : str ): Debe devolver el usuario que acumula más horas jugadas para el género dado y una lista de la acumulación de horas jugadas por año.
        Ejemplo de retorno: {"Usuario con más horas jugadas para Género X" : us213ndjss09sdf, "Horas jugadas":[{Año: 2013, Horas: 203}, {Año: 2012, Horas: 100}, {Año: 2011, Horas: 23}]}

        def UsersRecommend( año : int ): Devuelve el top 3 de juegos MÁS recomendados por usuarios para el año dado. (reviews.recommend = True y comentarios positivos/neutrales)
        Ejemplo de retorno: [{"Puesto 1" : X}, {"Puesto 2" : Y},{"Puesto 3" : Z}]

        def UsersNotRecommend( año : int ): Devuelve el top 3 de juegos MENOS recomendados por usuarios para el año dado. (reviews.recommend = False y comentarios negativos)
        Ejemplo de retorno: [{"Puesto 1" : X}, {"Puesto 2" : Y},{"Puesto 3" : Z}]

        def sentiment_analysis( año : int ): Según el año de lanzamiento, se devuelve una lista con la cantidad de registros de reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento.
        Ejemplo de retorno: {Negative = 182, Neutral = 120, Positive = 278}

>Se disponibilizan los datos a traves del FrameWok """FastApi""" y deployado a traves del servicio de Web service de Render para ser consumido.
Link
